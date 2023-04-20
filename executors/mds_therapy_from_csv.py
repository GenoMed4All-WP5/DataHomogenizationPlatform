import orjson
import traceback
import uuid

from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.observation import Observation
from fhir.resources.condition import Condition
from fhir.resources.patient import Patient
from datetime import datetime

from inputconnectors.FHIRConnection import FHIRConnection
# from customdataobjects import fhir_queries

from abstracts.AbstractMapper import AMapper
from extensions.DataHomogenizationPlatform.executors.utils.observation import Observation as Obs
from extensions.DataHomogenizationPlatform.executors.utils.condition import Condition as Cond
from extensions.DataHomogenizationPlatform.executors.utils.procedure import Procedure as Proc
from extensions.DataHomogenizationPlatform.mapping_tables.mds_mock_data_map_columns import mapping
from extensions.DataHomogenizationPlatform.executors.utils.fhir_templates import *
from customdataobjects import mapper_response
from pipeline import Constants

from json.encoder import JSONEncoder


class mds_therapy_from_csv(AMapper):
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
        # return mapper_response.MapperResponse(data=output)
        # return output
        # return output[0]

        # return mapper_response.MapperResponse(data=output[0], metrics=mapper_response.BlockMetrics(0))
        # return mapper_response.MapperResponse(data=output)
        # return [output]
        # return output

    def process_item(self, item):
        output = []

        '''
        Retriving data
        '''

        therapy_data = self.get_therapy_data(item)

        '''
        Creating FHIR resources based on the former data
        '''

        # TODO: go through the retrieved therapy data and create the necessary FHIR resources depending on the kind of therapy

        procedure = self.create_procedure(therapy_data)
        medication_statement = self.create_medication_statement(therapy_data)
        observation_responses, observations = self.create_observations(observation_data, patient_id) # TODO: see what parameters are to be used


        """organization_id = self.create_organization()
        patient_id = self.create_patient(demographics_data, organization_id)
        condition = self.create_condition(conditions_data, patient_id)
        diagnostic_report_id = self.create_diagnostic_report(output, clinical_data, patient_id, observations)"""

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

    def translate_gender(self, gender):
        if gender.upper() == "M":
            return "male"
        elif gender.upper() == "F":
            return "female"
        else:
            return "other"

    def translate_gender_basedOn_number(self, gender):
        return {1: 'male', 2: 'female'}.get(gender, 'other')

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
            organization_json = self.create_fhir_organization()
            output = self.fhir_conn.post(organization_json)

            id = self.getId(output)

            if id is None:
                raise Exception("Error when creating organization")

        return id

    def create_fhir_organization(self):

        organization_template = fhir_organization_template
        organization_template["name"] = self.config.get("GENOMED4ALL").get("organization")

        return organization_template

    def create_procedure(self, input_data):

        procedure_data = fhir_procedure_template

        for _, value in input_data.items():
            procedure = Proc()

            try:
                condition_info = procedure.get_procedure_code(value, input_data)
            except:
                traceback.print_exc()

    def create_medication_statement(self, input_data):
        pass

    def create_patient(self, input_data, organization_id):

        patient_id = input_data["patient_id"]
        search_list = []

        search_parameters = {"identifier": f'{organization_id}-{patient_id}-{self.suffix}'}

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

        patient_data["identifier"][0]["value"] = f'{organization_id}-{patient_id}-{self.suffix}'
        patient_data["identifier"][0]["assigner"]["display"] = self.config.get("GENOMED4ALL").get("organization")

        patient_data["gender"] = self.translate_gender_basedOn_number(input_data["patient_gender"])

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
                try:
                    fhir_condition = Condition(**condition_data)
                    condition_json = orjson.loads(fhir_condition.json())
                    conditions.append(condition_json)
                except:
                    traceback.print_exc()

        responses = self.fhir_conn.post(conditions)

        return responses


    def create_specimen(self, output, input_data):
        data = {
                "resourceType": "Specimen",
                "identifier": [
                    {
                        "system": "http://molit.eu/fhir/genomics/NamingSystem/cegat/tissueID",
                        "value": "UNKNOWN"
                    }
                ],
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0487",
                            "code": "TUMOR",
                            "display": "Tumor"
                        }
                    ]
                },
                "subject": {
                    "reference": "urn:uuid:f7a438e6-f484-453d-97e8-aa4d51008648"
                },
                "collection": {
                    "method": {
                        "coding": [
                            {
                                "system": "http://molit.eu/fhir/IG_TODO",
                                "code": "Biopsy",
                                "display": "Biopsie"
                            }
                        ]
                    },
                    "bodySite": {
                        "coding": [
                            {
                                "system": "http://example.org/fhir/sid/icd-9-cm",
                                "code": "C16.0"
                            }
                        ]
                    }
                }
            }

        return output

    def create_molecular_sequence(self, output, input_data):
        data = {
            "fullUrl": "urn:uuid:8200dab6-18a2-4550-b913-a7db480c0804",
            "resource": {
                "resourceType": "MolecularSequence",
                "type": "dna",
                "coordinateSystem": 0,
                "patient": {
                    "reference": "Patient/119",
                    "display": "Mary Chalmers"
                },
                "specimen": {
                    "reference": "Specimen/120",
                    "display": "buccal swab from Mary Chalmers"
                },
                "referenceSeq": {
                    "referenceSeqId": {
                        "coding": [
                            {
                                "system": "http://www.ebi.ac.uk/ipd/imgt/hla",
                                "version": "3.23",
                                "code": "HLA00001"
                            }
                        ],
                        "text": "HLA-A*01:01:01:01"
                    },
                    "windowStart": 503,
                    "windowEnd": 773
                },
                "observedSeq": "GCTCCCACTCCATGAGGTATTTCTTCACATCCGTGTCCCGGCCCGGCCGCGGGGAGCCCCGCTTCATCGCCGTGGGCTACGTGGACGACACGCAGTTCGTGCGGTTCGACAGCGACGCCGCGAGCCAGAAGATGGAGCCGCGGGCGCCGTGGATAGAGCAGGAGGGGCCGGAGTATTGGGACCAGGAGACACGGAATATGAAGGCCCACTCACAGACTGACCGAGCGAACCTGGGGACCCTGCGCGGCTACTACAACCAGAGCGAGGACG"
            },
            "request": {
                "method": "POST",
                "url": "MolecularSequence"
            }
        }
        return output

    def convert_string_to_float(self, value):

        '''
        Auxiliary method to read a decimal number containing a comma and convert it into a float variable
        '''
        if isinstance(value, str):
            if ',' in value:
                try:
                    value = float(value.replace(',', ''))
                    return value
                except ValueError:
                    print("Error: Unable to convert string to float")
            else:
                return float(value)

        return value

    def create_observations(self, input_data, patient_id):

        observations = []

        for key, value in input_data.items():
            value = self.convert_string_to_float(value)
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

    def add_index_and_type(self, fhir_resource_data, fhir_resource_type):
        # only for ELK Output connector
        fhir_resource_json = orjson.loads(fhir_resource_data.json())
        if self.config.get("OUT").get("otype") == "ELK":
            pass
            #fhir_resource_json["_index"] = self.config.get("GENOMED4ALL").get("tenant") + "-" + fhir_resource_type
            #fhir_resource_json["_odoctype"] = "_doc"
        return fhir_resource_json

    def create_diagnostic_report(self, output, clinical_data, patient_id, observations):

        search_list = []

        search_parameters = {"id": patient_id}

        search_object = {"resource": "DiagnosticReport", "parameters": search_parameters}
        search_list.append(search_object)

        responses = self.fhir_conn.execute_query(search_list)

        if len(responses) > 0 and responses[0].get("total") > 0:
            id = responses[0].get("entry")[0].get("resource").get("id")
        else:
            id = str(uuid.uuid4())
            data = {
                "resourceType": "DiagnosticReport",
                "id": id,
                "meta": {
                    "profile": [
                        "http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/genomics-report"
                    ],
                    "id": str(id),
                    "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                "status": "final",
                "category": [{
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                        "code": "GE"
                    }
                    ]
                }
                ],
                "code": {
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": self.config.get("GENOMED4ALL").get("use_case_snomed_code")
                    },
                        {
                            "system": "http://www.ohdsi.org/omop",
                            "code": self.config.get("GENOMED4ALL").get("use_case_omop_code")
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/" + patient_id
                }
            }

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
                    diagnostic_json = self.add_index_and_type(diagnostic_report, "diagnosticreport")
                    output.append(diagnostic_json)
                except:
                    traceback.print_exc()
        return output

    def get_therapy_data(self, item):
        therapy_data = {}
        try:
            therapy_data["euromds_id"] = item["EUROMDS_ID"]
        except:
            therapy_data["euromds_id"] = None
        try:
            therapy_data["t1_time"] = item["T1_time"]
        except:
            therapy_data["t1_time"] = None
        try:
            therapy_data["t1_type"] = item["T1_type"]
        except:
            therapy_data["t1_type"] = None
        try:
            therapy_data["t2_time"] = item["T2_time"]
        except:
            therapy_data["t2_time"] = None
        try:
            therapy_data["t2_type"] = item["T2_type"]
        except:
            therapy_data["t2_type"] = None
        try:
            therapy_data["t3_time"] = item["T3_time"]
        except:
            therapy_data["t3_time"] = None
        try:
            therapy_data["t3_type"] = item["T3_type"]
        except:
            therapy_data["t3_type"] = None
        try:
            therapy_data["t4_time"] = item["T4_time"]
        except:
            therapy_data["t4_time"] = None
        try:
            therapy_data["t4_type"] = item["T4_type"]
        except:
            therapy_data["t4_type"] = None

        return therapy_data

    def get_demographics_data(self, item):
        demographics_data = {}
        try:
            demographics_data["patient_id"] = item["Patient ID"]
        except:
            demographics_data["patient_id"] = None
        try:
            demographics_data["patient_gender"] = item["Gender"]
        except:
            demographics_data["patient_gender"] = None

        return demographics_data

    def get_clinical_data(self, item):
        clinical_data = {}
        try:
            clinical_data["del5q"] = item["del5q"]
        except:
            clinical_data["del5q"] = None
        try:
            clinical_data["Lossofchr5ordel5qPLUSother"] = item["Lossofchr5ordel5qPLUSother"]
        except:
            clinical_data["Lossofchr5ordel5qPLUSother"] = None
        try:
            clinical_data["Lossofchr7ordel7q"] = item["Lossofchr7ordel7q"]
        except:
            clinical_data["Lossofchr7ordel7q"] = None
        try:
            clinical_data["Gainofchr8"] = item["Gainofchr8"]
        except:
            clinical_data["Gainofchr8"] = None
        try:
            clinical_data["Lossofchr9ordel9q"] = item["Lossofchr9ordel9q"]
        except:
            clinical_data["Lossofchr9ordel9q"] = None
        try:
            clinical_data["Lossofchr11ordel11q"] = item["Lossofchr11ordel11q"]
        except:
            clinical_data["Lossofchr11ordel11q"] = None
        try:
            clinical_data["Lossofchr12ordel12port12p"] = item["Lossofchr12ordel12port12p"]
        except:
            clinical_data["Lossofchr12ordel12port12p"] = None
        try:
            clinical_data["Lossofchr13ordel13q"] = item["Lossofchr13ordel13q"]
        except:
            clinical_data["Lossofchr13ordel13q"] = None
        try:
            clinical_data["Isochr17qort17p"] = item["Isochr17qort17p"]
        except:
            clinical_data["Isochr17qort17p"] = None
        try:
            clinical_data["Lossofchr20ordel20q"] = item["Lossofchr20ordel20q"]
        except:
            clinical_data["Lossofchr20ordel20q"] = None
        try:
            clinical_data["LossofchrY"] = item["LossofchrY"]
        except:
            clinical_data["LossofchrY"] = None
        try:
            clinical_data["idicXq13"] = item["idicXq13"]
        except:
            clinical_data["idicXq13"] = None
        try:
            clinical_data["AOD"] = item["AOD"]
        except:
            clinical_data["AOD"] = None
        try:
            clinical_data["RS"] = item["RS"]
        except:
            clinical_data["RS"] = None
        try:
            clinical_data["Neutrophils"] = item["Neutrophils"]
        except:
            clinical_data["Neutrophils"] = None
        try:
            clinical_data["Hemoglobin"] = item["Hemoglobin"]
        except:
            clinical_data["Hemoglobin"] = None
        try:
            clinical_data["Platelets"] = item["Platelets"]
        except:
            clinical_data["Platelets"] = None
        try:
            clinical_data["LDH"] = item["LDH"]
        except:
            clinical_data["LDH"] = None
        try:
            clinical_data["Ferritin"] = item["Ferritin"]
        except:
            clinical_data["Ferritin"] = None
        try:
            clinical_data["BMB"] = item["BMB"]
        except:
            clinical_data["BMB"] = None
        try:
            clinical_data["BMMD"] = item["BMMD"]
        except:
            clinical_data["BMMD"] = None
        try:
            clinical_data["BMF"] = item["BMF"]
        except:
            clinical_data["BMF"] = None

        return clinical_data

    def get_observation_data(self, item):

        observation_data = {}

        try:
            observation_data["Neutrophils"] = item["Neutrophils"]
        except:
            observation_data["Neutrophils"] = None
        try:
            observation_data["Hemoglobin"] = item["Hemoglobin"]
        except:
            observation_data["Hemoglobin"] = None
        try:
            observation_data["Platelets"] = item["Platelets"]
        except:
            observation_data["Platelets"] = None
        try:
            observation_data["LDH"] = item["LDH"]
        except:
            observation_data["LDH"] = None
        try:
            observation_data["Ferritin"] = item["Ferritin"]
        except:
            observation_data["Ferritin"] = None

        return observation_data

    def get_conditions_data(self, item):
        conditions_data = {}
        try:
            conditions_data["BMMD"] = item["BMMD"]
        except:
            conditions_data["BMMD"] = None
        try:
            conditions_data["BMF"] = item["BMF"]
        except:
            conditions_data["BMF"] = None
        try:
            conditions_data["del5q"] = item["del5q"]
        except:
            conditions_data["del5q"] = None
        try:
            conditions_data["Lossofchr5ordel5qPLUSother"] = item["Lossofchr5ordel5qPLUSother"]
        except:
            conditions_data["Lossofchr5ordel5qPLUSother"] = None
        try:
            conditions_data["Lossofchr7ordel7q"] = item["Lossofchr7ordel7q"]
        except:
            conditions_data["Lossofchr7ordel7q"] = None
        try:
            conditions_data["Lossofchr13ordel13q"] = item["Lossofchr13ordel13q"]
        except:
            conditions_data["Lossofchr13ordel13q"] = None
        try:
            conditions_data["Lossofchr11ordel11q"] = item["Lossofchr11ordel11q"]
        except:
            conditions_data["Lossofchr11ordel11q"] = None
        try:
            conditions_data["Gainofchr8"] = item["Gainofchr8"]
        except:
            conditions_data["Gainofchr8"] = None
        try:
            conditions_data["Lossofchr9ordel9q"] = item["Lossofchr9ordel9q"]
        except:
            conditions_data["Lossofchr9ordel9q"] = None
        try:
            conditions_data["Isochr17qort17p"] = item["Isochr17qort17p"]
        except:
            conditions_data["Isochr17qort17p"] = None
        try:
            conditions_data["Lossofchr12ordel12port12p"] = item["Lossofchr12ordel12port12p"]
        except:
            conditions_data["Lossofchr12ordel12port12p"] = None
        try:
            conditions_data["Lossofchr20ordel20q"] = item["Lossofchr20ordel20q"]
        except:
            conditions_data["Lossofchr20ordel20q"] = None
        try:
            conditions_data["LossofchrY"] = item["LossofchrY"]
        except:
            conditions_data["LossofchrY"] = None

        return conditions_data

    def get_clinical_and_hematological_data(self, item):
        clinical_and_hematological_data = {}

        try:
            clinical_and_hematological_data["who_subtype"] = item["WHO 2016 subtype"]
        except:
            clinical_and_hematological_data["who_subtype"] = None

        try:
            clinical_and_hematological_data["aml_origin"] = item["AML origin (yes/no)"]
        except:
            clinical_and_hematological_data["aml_origin"] = None

        try:
            clinical_and_hematological_data["macro"] = item["MACRO (1=SLD,5Q-/2=MLD/3=EB1/4=EB2)"]
        except:
            clinical_and_hematological_data["macro"] = None

        try:
            clinical_and_hematological_data["rs_2"] = item["RS >2% (yes/no)"]
        except:
            clinical_and_hematological_data["rs_2"] = None

        try:
            clinical_and_hematological_data["Leukocytes_10_9L"] = item["Leukocytes (10 9/L) in viola le leucocitosi su cui pensare"]
        except:
            clinical_and_hematological_data["Leukocytes_10_9L"] = None

        try:
            clinical_and_hematological_data["Leukocytosis30"] = item["Leukocytosis30"]
        except:
            clinical_and_hematological_data["Leukocytosis30"] = None

        try:
            clinical_and_hematological_data["Neutrophils_10_9L"] = item["Neutrophils  (10 9/L)"]
        except:
            clinical_and_hematological_data["Neutrophils_10_9L"] = None

        try:
            clinical_and_hematological_data["Neutrophils_IPSSR"] = item["Neutrophils  IPSSR value (>0,8=0/<0,8=0,5)"]
        except:
            clinical_and_hematological_data["Neutrophils_IPSSR"] = None

        try:
            clinical_and_hematological_data["Monocytes_10_9L"] = item["Monocytes (10 9/L)"]
        except:
            clinical_and_hematological_data["Monocytes_10_9L"] = None

        try:
            clinical_and_hematological_data["Hemoglobin_g_L"] = item["Hemoglobin (g/L)"]
        except:
            clinical_and_hematological_data["Hemoglobin_g_L"] = None

        try:
            clinical_and_hematological_data["Hemoglobin_IPSSR"] = item["Hemoglobin IPSSR value (>100=0/80-100=1/<80=1,5)"]
        except:
            clinical_and_hematological_data["Hemoglobin_IPSSR"] = None

        try:
            clinical_and_hematological_data["Platelets_10_9L"] = item["Platelets (10 9/L)"]
        except:
            clinical_and_hematological_data["Platelets_10_9L"] = None

        try:
            clinical_and_hematological_data["Platelets_IPSSR"] = item["Platelets IPSSR value (>100=0/50-100=0,5/<50=1)"]
        except:
            clinical_and_hematological_data["Platelets_IPSSR"] = None

        try:
            clinical_and_hematological_data["aml_origin"] = item["2-3 cytopenias IPSS value (no=0/yes=0,5)"]
        except:
            clinical_and_hematological_data["aml_origin"] = None

        try:
            clinical_and_hematological_data["ldh_u_l"] = item["LDH (U/L)"]
        except:
            clinical_and_hematological_data["ldh_u_l"] = None

        try:
            clinical_and_hematological_data["Ferritin_ng_ml"] = item["Ferritin (ng/ml)"]
        except:
            clinical_and_hematological_data["Ferritin_ng_ml"] = None

        try:
            clinical_and_hematological_data["bone_marrow_blasts"] = item["% bone marrow blasts"]
        except:
            clinical_and_hematological_data["bone_marrow_blasts"] = None

        try:
            clinical_and_hematological_data["BM_blasts_IPSS_value"] = item["BM blasts IPSS value (<5=0/5-10=0,5/11-20=1,5/>20=2)"]
        except:
            clinical_and_hematological_data["BM_blasts_IPSS_value"] = None

        try:
            clinical_and_hematological_data["BM_blasts_IPSSR_value"] = item["BM blasts IPSSR value (<2=0/3-<5=1/5-10=2/>10=3)"]
        except:
            clinical_and_hematological_data["BM_blasts_IPSSR_value"] = None

        try:
            clinical_and_hematological_data["bone_marrow_ring_sideroblasts"] = item["% bone marrow ring sideroblasts"]
        except:
            clinical_and_hematological_data["bone_marrow_ring_sideroblasts"] = None

        try:
            clinical_and_hematological_data["bone_marrow_multilineage_dysplasia"] = item["bone marrow multilineage dysplasia (yes/no)"]
        except:
            clinical_and_hematological_data["bone_marrow_multilineage_dysplasia"] = None

        try:
            clinical_and_hematological_data["bone_marrow_fibrosis"] = item["bone marrow fibrosis (yes/no)"]
        except:
            clinical_and_hematological_data["bone_marrow_fibrosis"] = None

        return clinical_and_hematological_data

    def get_cytogenetics_data(self, item):
        cytogenetics_data = {}

        try:
            cytogenetics_data["Cytogenetics_ISCN"] = item["Cytogenetics (ISCN)"]
        except:
            cytogenetics_data["Cytogenetics_ISCN"] = None

        try:
            cytogenetics_data["n_alterazioni_citogenetiche"] = item["n alterazioni citogenetiche"]
        except:
            cytogenetics_data["n_alterazioni_citogenetiche"] = None

        try:
            cytogenetics_data["gt3_abnormalities"] = item[">3 abnormalities (yes=1/no=0)"]
        except:
            cytogenetics_data["gt3_abnormalities"] = None

        try:
            cytogenetics_data["del_5q"] = item["del(5q) (yes=1/no=0)"]
        except:
            cytogenetics_data["del_5q"] = None

        try:
            cytogenetics_data["Loss_of_chr_5"] = item["Loss of chr 5 or del(5q)+other (yes=1/no=0)"]
        except:
            cytogenetics_data["Loss_of_chr_5"] = None

        try:
            cytogenetics_data["Loss_of_chr_7"] = item["Loss of chr 7 or del(7q) (yes=1/no=0)"]
        except:
            cytogenetics_data["Loss_of_chr_7"] = None

        try:
            cytogenetics_data["Gain_of_chr_8"] = item["Gain of chr 8 (yes=1/no=0)"]
        except:
            cytogenetics_data["Gain_of_chr_8"] = None

        try:
            cytogenetics_data["Loss_of_chr_9"] = item["Loss of chr 9 or del(9q) (yes=1/no=0)"]
        except:
            cytogenetics_data["Loss_of_chr_9"] = None

        try:
            cytogenetics_data["Loss_of_chr_11"] = item["Loss of chr 11 or del(11q) (yes=1/no=0)"]
        except:
            cytogenetics_data["Loss_of_chr_11"] = None

        try:
            cytogenetics_data["Loss_of_chr_12"] = item["Loss of chr 12 or del(12p) or t(12p) (yes=1/no=0)"]
        except:
            cytogenetics_data["Loss_of_chr_12"] = None

        try:
            cytogenetics_data["Loss_of_chr_13"] = item["Loss of chr 13 or del(13q) (yes=1/no=0)"]
        except:
            cytogenetics_data["Loss_of_chr_13"] = None

        try:
            cytogenetics_data["Isochr_17q"] = item["Isochr 17q or t(17p) (yes=1/no=0)"]
        except:
            cytogenetics_data["Isochr_17q"] = None

        try:
            cytogenetics_data["Loss_of_chr_20"] = item["Loss of chr 20 or del(20q) (yes=1/no=0)"]
        except:
            cytogenetics_data["Loss_of_chr_20"] = None

        try:
            cytogenetics_data["Loss_of_chr_Y"] = item["Loss of chr Y (yes=1/no=0)"]
        except:
            cytogenetics_data["Loss_of_chr_Y"] = None

        try:
            cytogenetics_data["idic(X)(q13)"] = item["idic(X)(q13) (yes=1/no=0)"]
        except:
            cytogenetics_data["idic(X)(q13)"] = None

        return cytogenetics_data

    def get_outcome_data(self, item):
        pass

    def get_oncogenetics_data(self, item):
        oncogenetics_data = {}

        oncogenetics_columns = dict(filter(lambda x: (x[1]["type"]) == "oncogenetics", mapping.items()))
        for key, value in oncogenetics_columns.items():
            try:
                oncogenetics_data[value.get("key")] = item[key]
            except:
                pass

        return oncogenetics_data

