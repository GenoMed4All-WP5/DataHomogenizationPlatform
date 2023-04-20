import orjson
import traceback
import uuid
import re

from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient
from datetime import datetime
from inputconnectors.FHIRConnection import FHIRConnection
from abstracts.AbstractMapper import AMapper
from extensions.DataHomogenizationPlatform.executors.utils.genetic_observation import Observation as Obs
from extensions.DataHomogenizationPlatform.mapping_tables.mds_mock_data_map_columns import mapping
from extensions.DataHomogenizationPlatform.executors.utils.fhir_templates import *
from extensions.DataHomogenizationPlatform.executors.utils.generic_methods import GenericMethods
from extensions.DataHomogenizationPlatform.mapping_tables import columns_names as cn
from customdataobjects import mapper_response


class mds_genetic_data_from_csv(AMapper):
    exists_index = None
    fhir_conn = None

    def __init__(self, config):
        self.config = config
        self.fhir_conn = FHIRConnection(config)
        self.suffix = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        fixed_item = {}

        for key, value in item.items():
            fixed_item[re.sub(' +', ' ', key)] = value

        '''
        Retriving data
        '''
        demographics_data = self.get_demographics_data(item, cn.demographics_data)
        genetic_data = self.get_oncogenetics_data(fixed_item)

        '''
        Creating FHIR resources based on the former data
        '''
        organization_id = self.create_organization()
        patient_id = self.create_patient(demographics_data, organization_id)
        # encounter_id = self.create_encounter(patient_id, organization_id, output)
        observations_list = self.create_observations(genetic_data, patient_id)
        diagnostic_report_id = self.create_diagnostic_report(output, genetic_data, patient_id, observations_list)

        return output

    def getId(self, headers):

        '''
            Retrieve the Location header and just take the resource id
        '''

        url = ""
        id = None

        if headers[0].status_code == 201:

            for header in headers[0].headers.raw:
                if header[0].decode('utf-8') == 'Location':
                    url = header[1].decode('utf-8')
                    break

            id = url.split("/")[6]

        return id

    def getObservationId(self, response):

        '''
            Retrieve the Location header and just take the resource id
        '''

        url = ''
        id = None

        if response.status_code == 201:
            for header in response.headers.raw:
                if header[0].decode('utf-8') == 'Location':
                    url = header[1].decode('utf-8')
                    break

            id = url.split("/")[6]

        return id

    def create_encounter(self, patient_id, organization_id, output):
        '''
        Creates an encounter between the patient whose id is provided and the healthcare provider based on the given
        organization id.
        '''

        id, encounter_json = self.create_fhir_encounter(patient_id, organization_id)
        output.append(encounter_json)

        return id

    def create_fhir_encounter(self, patient_id, organization_id):
        '''
        Creates an encounter JSON between the patient whose id is provided and the healthcare provider based on the given
        organization id. It returns both the encounter id and the json variable
        '''

        encounter_template = fhir_encounter_template

        id = str(uuid.uuid4())
        encounter_template["id"] = id
        encounter_template["subject"]["reference"] = f"Patient/{patient_id}"
        encounter_template["serviceProvider"]["reference"] = f"Organization/{organization_id}"

        return id, encounter_template

    def translate_gender(self, gender):
        if gender.upper() == "M":
            return "male"
        elif gender.upper() == "F":
            return "female"
        else:
            return "other"

    def create_organization(self):
        '''
        Looks for the organization on the FHIR server based on some collected parameters.
        If such organization does not exist, it will be created. Otherwise, it will simply return the existing id
        '''

        search_list = []
        organization_name = self.config.get("GENOMED4ALL").get("organization")

        search_parameters = {"name": organization_name}

        search_object = {"resource": "Organization", "parameters": search_parameters}
        search_list.append(search_object)

        responses = self.fhir_conn.execute_query(search_list)

        if len(responses) > 0 and responses[0].get("total") > 0:
            id = responses[0].get("entry")[0].get("resource").get("id")
        else:
            organization_json = self.create_fhir_organization(organization_name)
            output = self.fhir_conn.post(organization_json)

            id = self.getId(output)

            if id is None:
                raise Exception("")

        return id

    def create_fhir_organization(self, input_data):

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
            id = responses[0].get("entry")[0].get("resource").get("id")
        else:
            patient_json = self.create_fhir_patient(input_data, organization_id)
            output = self.fhir_conn.post(patient_json)

            id = self.getId(output)

        return id

    def create_fhir_patient(self, input_data, organization_id):
        patient_id = input_data["patient_id"]
        patient_data = fhir_patient_template

        patient_data["identifier"][0]["value"] = f'{organization_id}-{patient_id}'
        patient_data["identifier"][0]["assigner"]["display"] = self.config.get("GENOMED4ALL").get("organization")

        patient_data["gender"] = self.translate_gender(input_data["patient_gender"])

        patient_data["managingOrganization"]["reference"] = f"Organization/{organization_id}"
        patient_data["managingOrganization"]["display"] = self.config.get("GENOMED4ALL").get("organization")

        patient = Patient(**patient_data)
        try:
            patient_json = orjson.loads(patient.json())
        except:
            traceback.print_exc()

        return patient_json

    def create_observations(self, input_data, patient_id):
        observations = []
        for key, value in input_data.items():
            value = GenericMethods.convert_string_to_float(value)
            data = self.get_observation_template(patient_id)
            obs = Obs()

            try:
                obs_info = obs.get_observation_code(key, value, input_data)
            except:
                traceback.print_exc()

            if obs_info is not None:
                data.update(obs_info)
                try:
                    fhir_observation = Observation(**data)
                    observation_json = orjson.loads(fhir_observation.json())
                    observations.append(observation_json)
                except:
                    traceback.print_exc()

        responses = self.fhir_conn.post(observations)

        return responses

    def get_observation_template(self, patient_id):
        observation_id = str(uuid.uuid4())
        data = {
            "resourceType": "Observation",
            "id": observation_id,
            "meta": {
                "id": str(observation_id),
                "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            "identifier": [
                {
                    "use": "genomed4All",
                    "value": observation_id
                }
            ],
            "status": "final",
            "subject": {
                "reference": "Patient/" + patient_id
            }
        }
        return data

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

    def get_demographics_data(self, item, vocabulary):
        data = {}
        for each in vocabulary:
            data[each.get("variable_name", each.get("source_column"))] = item.get(each.get("source_column"), None)
        return data

    def get_oncogenetics_data(self, item):
        oncogenetics_data = {}

        oncogenetics_columns = dict(filter(lambda x: (x[1]["type"]) == "oncogenetics", mapping.items()))
        for key, value in oncogenetics_columns.items():
            try:
                oncogenetics_data[value.get("key")] = item[key]
            except:
                pass

        return oncogenetics_data
