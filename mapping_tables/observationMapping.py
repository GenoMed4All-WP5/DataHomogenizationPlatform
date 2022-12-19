import math


def get_hemoglobin_code(key, value, clinical_and_hematological_data):
    if value is not None and not math.isnan(value) and value != 'NA':
        basic_data = {"code":
            {"coding": [
                {
                    "system": "http://loinc.org",
                    "code": "718-7",
                    "display": "Hemoglobin [Mass/volume] in Blood"
                }
            ]
            },
            "valueQuantity": {
                "value": value,
                "unit": "g/L",
                "system": "http://unitsofmeasure.org",
                "code": "g/L"
            }
        }

        if "Hemoglobin_IPSSR" in clinical_and_hematological_data and clinical_and_hematological_data["Hemoglobin_IPSSR"] is not None and clinical_and_hematological_data["Hemoglobin_IPSSR"] != "NA":
            interpretation = clinical_and_hematological_data["Hemoglobin_IPSSR"]
            interpretation_display = "≥ 10 g/dL" if interpretation == 0 else "8 to 10 g/dL" if interpretation == 1 else "< 8 g/dL"
            basic_data["interpretation"] = [
                {
                    "coding": [
                        {
                            "system": "https://www.cibmtr.org/manuals/fim/1/en/topic/q123-126-transformation",
                            "code": interpretation,
                            "display": interpretation_display
                        }
                    ]
                }
            ]

        return basic_data
    else:
        return None


def get_oncogenetics_code(key, value, oncogenetics_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        '''import requests

        baseurl = "https://www.ncbi.nlm.nih.gov/search/all/?term="
        url = 'search/all/?'
        if key is not None and key != "":
            url = url + "&term=" + key.split()[0]

        response = requests.get(baseurl + url)'''

        mutation_key = key.split()[0] + " n. mutations"
        load_key = key.split()[0] + " load"

        extension_data = [{
            "url": "http://hl7.org/fhir/StructureDefinition/observation-geneticsGene",
            "valueCodeableConcept": {
                "coding": [
                    {
                        "system": "https://www.ncbi.nlm.nih.gov/nuccore",
                        "code": key.split()[0],
                        "display": key.split()[0]
                    }
                ]
            }
        }
        ]

        component_data = [
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://genome4all.org",
                            "code": "n.mutation",
                            "display": "Number of mutations in that gene"
                        }
                    ]
                },
                "valueQuantity": {
                    "value": oncogenetics_data[mutation_key],
                    "unit": "mutation",
                    "system": "http://unitsofmeasure.org",
                    "code": "mutation"
                }
            },
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://genome4all.org",
                            "code": "load",
                            "display": "Total number of mutations per coding area of a tumour genome"
                        }
                    ]
                },
                "valueQuantity": {
                    "value": oncogenetics_data[load_key] if not math.isnan(oncogenetics_data[load_key]) else None,
                    "unit": "count",
                    "system": "http://unitsofmeasure.org",
                    "code": "count"
                }
            }
        ]

        basic_data = {"code": {"coding": [
            {
                "system": "https://www.ncbi.nlm.nih.gov/nuccore",
                "code": key.split()[0],
                "display": key.split()[0]
            }
        ]
        }, "valueQuantity": {
            "value": value,
            "unit": "0/1",
            "system": "http://unitsofmeasure.org",
            "code": "0/1"
        }, "extension": extension_data,
            "component": component_data}

        return basic_data
    else:
        return None
