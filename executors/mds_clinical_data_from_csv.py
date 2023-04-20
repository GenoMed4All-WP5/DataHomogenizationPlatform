import orjson
import traceback
import uuid

from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.observation import Observation
from fhir.resources.condition import Condition
from fhir.resources.patient import Patient
from datetime import datetime
from inputconnectors.FHIRConnection import FHIRConnection
from abstracts.AbstractMapper import AMapper
from extensions.DataHomogenizationPlatform.executors.utils.observation import Observation as Obs
from extensions.DataHomogenizationPlatform.executors.utils.condition import Condition as Cond
from extensions.DataHomogenizationPlatform.executors.utils.fhir_templates import *
from extensions.DataHomogenizationPlatform.executors.utils.generic_methods import GenericMethods
from extensions.DataHomogenizationPlatform.mapping_tables import columns_names as cn
from customdataobjects import mapper_response


class mds_clinical_data_from_csv(AMapper):
    exists_index = None
    fhir_conn = None

    def __init__(self, config):
        self.config = config
        self.fhir_conn = FHIRConnection(config)
        self.suffix = datetime.now().strftime("%Y%m%d%H%M%S")

    def execute(self, blockdata):
        output = []

        if type(blockdata) is list:
            for each in blockdata:
                data = self.process_item(each)
                output.extend(data)
        else:
            output = self.process_item(blockdata)

        return mapper_response.MapperResponse(data=output, metrics=mapper_response.BlockMetrics(0))

    def process_item(self, item):
        output = []

        '''
        Retriving data
        '''

        demographics_data = self.get_data(item, cn.demographics_data)
        clinical_data = self.get_data(item, cn.clinical_data)
        observation_data = self.get_data(item, cn.observation_data)
        conditions_data = self.get_data(item, cn.conditions_data)

        '''
        Creating FHIR resources based on the former data
        '''
        organization_id = self.create_organization()
        patient_id = self.create_patient(demographics_data, organization_id)
        observation_responses, observations = self.create_observations(observation_data, patient_id)
        condition = self.create_condition(conditions_data, patient_id)
        diagnostic_report_id = self.create_diagnostic_report(output, clinical_data, patient_id, observations)

        return output

    def create_organization(self):
        '''
        Looks for the organization on the FHIR server based on some collected parameters.
        If such organization does not exist, it will be created. Otherwise, it will simply return the existing id
        '''
        organization_name = self.config.get("GENOMED4ALL").get("organization")

        search_list = []
        search_parameters = {"name": organization_name}
        search_object = {"resource": "Organization", "parameters": search_parameters}
        search_list.append(search_object)

        responses = self.fhir_conn.execute_query(search_list)

        if len(responses) > 0 and responses[0].get("total") > 0:
            organization_id = responses[0].get("entry")[0].get("resource").get("id")
        else:
            organization_json = self.create_fhir_organization()
            output = self.fhir_conn.post(organization_json)

            organization_id = GenericMethods.get_fhir_id_from_headers(output)

            if organization_id is None:
                raise Exception("Error when creating organization")

        return organization_id

    def create_fhir_organization(self):

        organization_template = fhir_organization_template
        organization_template["name"] = self.config.get("GENOMED4ALL").get("organization")

        return organization_template

    def create_patient(self, input_data, organization_id):
        patient_id = input_data["patient_id"]

        search_list = []
        search_parameters = {"identifier": f'{organization_id}-{patient_id}'}
        search_object = {"resource": "Patient", "parameters": search_parameters}
        search_list.append(search_object)

        responses = self.fhir_conn.execute_query(search_list)

        if len(responses) > 0 and responses[0].get("total") > 0:
            patient_id = responses[0].get("entry")[0].get("resource").get("id")
        else:
            patient_json = self.create_fhir_patient(input_data, organization_id)
            output = self.fhir_conn.post(patient_json)

            patient_id = GenericMethods.get_fhir_id_from_headers(output)

        return patient_id

    def create_fhir_patient(self, input_data, organization_id):
        patient_id = input_data["patient_id"]
        patient_data = fhir_patient_template

        patient_data["identifier"][0]["value"] = f'{organization_id}-{patient_id}'
        patient_data["identifier"][0]["assigner"]["display"] = self.config.get("GENOMED4ALL").get("organization")

        patient_data["gender"] = GenericMethods.translate_gender_based_on_number(input_data["patient_gender"])

        patient_data["managingOrganization"]["reference"] = f"Organization/{organization_id}"
        patient_data["managingOrganization"]["display"] = self.config.get("GENOMED4ALL").get("organization")

        patient = Patient(**patient_data)
        try:
            patient_json = orjson.loads(patient.json())
        except:
            traceback.print_exc()

        return patient_json

    def create_condition(self, clinical_data, patient_id):

        condition_data = fhir_condition_template
        conditions = []

        subject = {
            "reference": f"Patient/{patient_id}"
        }

        for key, value in clinical_data.items():
            try:
                if int(value) > 0:
                    condition = Cond()

                    try:
                        condition_info = condition.get_condition_code(key, value, clinical_data)
                    except:
                        traceback.print_exc()

                    if condition_info is not None:
                        condition_data.update(condition_info)
                        condition_data["subject"] = subject
                        cond_code = condition_data["code"]["coding"][1]["code"]
                        condition_data["id"] = f"{patient_id}-{cond_code}"
                        condition_data["identifier"][0]["value"] = f"{patient_id}-{cond_code}"
                        try:
                            fhir_condition = Condition(**condition_data)
                            condition_json = orjson.loads(fhir_condition.json())
                            conditions.append(condition_json)
                        except:
                            traceback.print_exc()
            except:
                print(f'Column {key} cannot be processed due the value format is the expected one')

        responses = self.fhir_conn.post(conditions)

        return responses

    def create_observations(self, input_data, patient_id):
        observations = []
        for key, value in input_data.items():
            value = GenericMethods.convert_string_to_float(value)
            data = self.get_observation_template()
            obs = Obs()

            try:
                obs_info = obs.get_observation_code(key, value, input_data)
            except:
                traceback.print_exc()

            if obs_info is not None:
                data.update(obs_info)
                omopConceptID = data.get("code").get("coding")[1].get("code")
                obs_value = data.get("valueQuantity").get("value")
                data["id"] = f"{patient_id}-{omopConceptID}"
                data["identifier"][0]["value"] = f"{patient_id}-{omopConceptID}"
                data["subject"]["reference"] = f"Patient/{patient_id}"

                try:
                    fhir_observation = Observation(**data)
                    observation_json = orjson.loads(fhir_observation.json())
                    observations.append(observation_json)
                except:
                    traceback.print_exc()

        responses = self.fhir_conn.post(observations)

        return responses, observations

    def get_observation_template(self):
        return fhir_observation_template

    def create_diagnostic_report(self, output, clinical_data, patient_id, observations):

        search_list = []

        search_parameters = {"patient": patient_id}

        search_object = {"resource": "DiagnosticReport", "parameters": search_parameters}
        search_list.append(search_object)

        responses = self.fhir_conn.execute_query(search_list)

        if len(responses) > 0 and responses[0].get("total") > 0:
            diagnostic_report_id = responses[0].get("entry")[0].get("resource").get("id")
        else:
            diagnostic_report_id = str(uuid.uuid4())
            data = fhir_diagnostic_report_template
            data["id"] = diagnostic_report_id
            data["meta"]["id"] = str(diagnostic_report_id)
            data["meta"]["lastUpdated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            data["code"]["coding"][0]["code"] = self.config.get("GENOMED4ALL").get("use_case_snomed_code")
            data["code"]["coding"][1]["code"] = self.config.get("GENOMED4ALL").get("use_case_omop_code")
            data["subject"]["reference"] = "Patient/" + patient_id

            result = []
            for each in observations:
                ref = {
                    "reference": "Observation/" + each["id"]
                }
                result.append(ref)

            if result is not None:
                data["result"] = result
                try:
                    diagnostic_report = DiagnosticReport(**data)
                    diagnostic_json = orjson.loads(diagnostic_report.json())
                    output.append(diagnostic_json)
                except:
                    traceback.print_exc()
        return output

    def get_data(self, item, vocabulary):
        data = {}
        for each in vocabulary:
            data[each.get("variable_name", each.get("source_column"))] = item.get(each.get("source_column"), None)
        return data
