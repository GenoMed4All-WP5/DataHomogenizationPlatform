import math


def get_ferritin_code(key, value, clinical_data):

    if isinstance(value, (int, float)) and math.isnan(value):
        return None

    if value is not None and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "489004",
                        "display": "Ferritin"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "4176561",
                        "display": "Ferritin"
                    }
                ]
            },
            "valueQuantity": {
                "value": value,
                "unit": "ng/ml",
                "system": "http://unitsofmeasure.org"
            }
        }

        return data
    else:
        return None


def get_ldh_code(key, value, clinical_data):

    if isinstance(value, (int, float)) and math.isnan(value):
        return None

    if value is not None and value != 'NA':

        data = {
                "code": {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "250644007",
                            "display": "LDH"
                        },
                        {
                            "system": "http://www.ohdsi.org/omop",
                            "code": "4098519",
                            "display": "LDH"
                        }
                    ]
                },
                "valueQuantity": {
                    "value": value,
                    "unit": "[U]/L",
                    "system": "http://unitsofmeasure.org"
                }
        }

        return data
    else:
        return None


def get_platelets_code(key, value, clinical_data):
    if isinstance(value, (int, float)) and math.isnan(value):
        return None

    if value is not None and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "365632008",
                        "display": "Platelets"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "4273307",
                        "display": "Platelets"
                    }
                ]
            },
            "valueQuantity": {
                "value": value,
                "unit": "10*9/L",
                "system": "http://unitsofmeasure.org"
            }
        }

        return data
    else:
        return None


def get_neutrophils_code(key, value, clinical_data):
    if isinstance(value, (int, float)) and math.isnan(value):
        return None

    if value is not None and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "1022551000000104",
                        "display": "Neutrophils"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37393856",
                        "display": "Neutrophils"
                    }
                ]
            },
            "valueQuantity": {
                "value": value,
                "unit": "10*9/L",
                "system": "http://unitsofmeasure.org"
            }
        }

        return data
    else:
        return None


def get_hemoglobin_code(key, value, clinical_and_hematological_data):
    if isinstance(value, (int, float)) and math.isnan(value):
        return None

    if value is not None and value != 'NA':
        basic_data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "38082009",
                        "display": "Hemoglobin [Mass/volume] in Blood"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "4244232",
                        "display": "Hemoglobin [Mass/volume] in Blood"
                    }
                ]
            },
            "valueQuantity": {
                "value": value,
                "unit": "g/dl",
                "system": "http://unitsofmeasure.org"
            }
        }

        '''
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
        '''

        return basic_data
    else:
        return None


def convert_string_to_float(value):

    '''
    Auxiliary method to read a decimal number containing a comma and convert it into a float variable
    '''

    if isinstance(value, (int, float)) and math.isnan(value):
        return 0

    if isinstance(value, str):
        if ',' in value:
            try:
                value = float(value.replace(',', ''))
                return value
            except ValueError:
                print("Error: Unable to convert string to float")
        else:
            return float(value)

    return float(value)


def get_oncogenetics_code(key, value, oncogenetics_data):

    if isinstance(value, (int, float)) and math.isnan(value):
        return None

    if value is not None and value != 'NA':

        '''import requests

        baseurl = "https://www.ncbi.nlm.nih.gov/search/all/?term="
        url = 'search/all/?'
        if key is not None and key != "":
            url = url + "&term=" + key.split()[0]

        response = requests.get(baseurl + url)'''
        suffix = " " + key.split()[1] if key.split()[1][0] == '(' else ""

        mutation_key = key.split()[0] + suffix + " n. mutations"
        load_key = key.split()[0] + suffix + " load"

        try:
            # Attempt to access a key that does not exist
            mutation_value = oncogenetics_data[mutation_key]
        except KeyError as e:
            print("KeyError: {}".format(e))
            # Handle the KeyError exception here, e.g. provide a default value
            mutation_value = 0

        try:
            # Attempt to access a key that does not exist
            load_value = oncogenetics_data[load_key]
        except KeyError as e:
            print("KeyError: {}".format(e))
            # Handle the KeyError exception here, e.g. provide a default value
            load_value = 0

        print(f"Mutation key: {mutation_key}, Load key: {load_key}")

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
                    "value": convert_string_to_float(mutation_value),
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
                    "value": convert_string_to_float(load_value),
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
