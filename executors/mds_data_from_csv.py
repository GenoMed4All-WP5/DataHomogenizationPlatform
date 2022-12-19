import traceback
from datetime import datetime

import orjson
import uuid
from abstracts.AbstractMapper import AMapper

from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient

from extensions.Genomed4All.executors.utils.observation import Observation as Obs


class mds_data_from_csv(AMapper):
    exists_index = None
    '''esConn = None'''

    def __init__(self, config):
        self.config = config
        '''if self.esConn is None:
            self.esConn = ELKConnection()
            context = {"curl": config["ourl"]}
            self.esConn.connect(context)'''

    def execute(self, item):
        output = []

        for each in item:
            data = self.process_item(each)
            output.extend(data)
        return output

    def process_item(self, item):
        output = []

        demographics_data = self.get_demographics_data(item)
        clinical_and_hematological_data = self.get_clinical_and_hematological_data(item)
        cytogenetics_data = self.get_cytogenetics_data(item)
        outcome_data = self.get_outcome_data(item)
        oncogenetic_data = self.get_oncogenetics_data(item)

        patient_id = self.create_patient(output, demographics_data)
        #self.create_observations(output, clinical_and_hematological_data, demographics_data)
        self.create_observations(output, oncogenetic_data, patient_id)
        self.create_diagnostic_report(output, clinical_and_hematological_data, patient_id)

        return output

    def translate_gender(self, gender):
        if gender.upper() == "M":
            return "male"
        elif gender.upper() == "F":
            return "female"
        else:
            return "other"

    def create_patient(self, output, input_data):
        id = str(uuid.uuid4())
        data = {
                "resourceType": "Patient",
                "id": id,
                "meta": {
                    "id": str(id),
                    "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                },
                "identifier": [
                    {
                        "system": "http://genomed4All.com",
                        "value": input_data["patient_id"]
                    }
                ],
                "gender": self.translate_gender(input_data["patient_gender"]),
            }

        patient = Patient(**data)

        try:
            patient_json = self.add_index_and_type(patient, "patient")
        except:
            traceback.print_exc()

        output.append(patient_json)

        return id

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

    def create_observations(self, output, input_data, patient_id):
        for key, value in input_data.items():
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
                    observation_json = self.add_index_and_type(fhir_observation, "observation")
                    output.append(observation_json)
                except:
                    traceback.print_exc()

        return output

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
                "reference": "Patient\\" + patient_id
            }
        }
        return data

    def add_index_and_type(self, fhir_resource_data, fhir_resource_type):
        # only for ELK Output connector
        fhir_resource_json = orjson.loads(fhir_resource_data.json())
        if self.config.get("OUT").get("otype") == "ELK":
            fhir_resource_json["_index"] = self.config.get("GENOMED4ALL").get("tenant") + "-" + fhir_resource_type
            fhir_resource_json["_odoctype"] = "_doc"
        return fhir_resource_json

    def create_diagnostic_report(self, output, clinical_and_hematological_data, patient_id):
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
                    "system": "http://loinc.org",
                    "code": "81247-9",
                    "display": "Master HL7 genetic variant reporting panel"
                },
                    {
                        "system": "https://pubmed.ncbi.nlm.nih.gov/",
                        "code": clinical_and_hematological_data["who_subtype"],
                        "display": clinical_and_hematological_data["who_subtype"]
                    }
                ]
            },
            "category": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                            "code": "GE",
                            "display": "Genetics"
                        }
                    ]
                }
            ],
            "subject": {
                "reference": "Patient/" + patient_id
            }
        }

        result = []
        for each in output:
            ref = {
                "reference": each["resourceType"] + "/" + each["id"]
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

    def get_demographics_data(self, item):
        demographics_data = {}
        try:
            demographics_data["patient_id"] = item["Patient ID"]
        except:
            demographics_data["patient_id"] = None
        try:
            demographics_data["patient_gender"] = item["Gender (M/F)"]
        except:
            demographics_data["patient_gender"] = None
        try:
            demographics_data["age"] = item["Age at data collection (y)"]
        except:
            demographics_data["age"] = None

        return demographics_data

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

        from extensions.Genomed4All.mapping_tables.mds_mock_data_map_columns import mapping
        oncogenetics_columns = dict(filter(lambda x: (x[1]["type"]) == "oncogenetics", mapping.items()))
        for key, value in oncogenetics_columns.items():
            try:
                oncogenetics_data[value.get("key")] = item[key]
            except:
                pass

        return oncogenetics_data

