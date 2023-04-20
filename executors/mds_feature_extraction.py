import csv

from inputconnectors.FHIRConnection import FHIRConnection
from abstracts.AbstractMapper import AMapper
from customdataobjects import mapper_response
from pipeline import FHIRExport
from pipeline import Constants


class mds_feature_extraction(AMapper):
    exists_index = None
    fhir_conn = None
    suffix = None
    organization_name = None
    next = None

    def __init__(self, config):
        self.config = config
        self.fhir_conn = FHIRConnection(config)
        # self.fhir_export = FHIRExport()

    def getId(self, resource):
        '''
        Returns only the id that belongs to that resource
        '''

        return resource.split("/")[1]

    def get_by_id(self, resource, resource_id):

        search_list = []

        search_parameters = {"_id": resource_id}

        search_object = {"resource": f"{resource}", "parameters": search_parameters}
        search_list.append(search_object)

        responses = self.fhir_conn.execute_query(search_list)

        return responses[0].get("entry")[0].get("resource")

    def get_by_patient(self, resources, patient_id):


        search_list = []

        search_parameters = {"patient": f"Patient/{patient_id}"}

        for each in resources:
            search_object = {"resource": each, "parameters": search_parameters}
            search_list.append(search_object)

        responses = self.fhir_conn.execute_query(search_list)

        return responses

    def csv_to_dict(self, csv_file):
        """
        Reads a CSV file and converts it to a dictionary.
        """
        # Open the CSV file for reading
        with open(csv_file, 'r') as csv_file:
            # Create a CSV reader object
            csv_reader = csv.DictReader(csv_file)

            # Create an empty dictionary to store the CSV data
            csv_data = {}

            # Loop through each row in the CSV file
            for row in csv_reader:
                # Extract the key and value from each row
                key = row.popitem()[1]
                value = row.popitem()[1]

                # Add the key-value pair to the dictionary
                csv_data[key] = value

        return csv_data

    def get_patient_source_id(self, patient):
        return patient.get("identifier")[0].get("value").split('-')[1]

    def execute(self, blockdata):
        output = []
        next_observation_page = None
        next_condition_page = None

        for each in blockdata:
            # Get Patient id
            patient_id = self.getId(each.get("resource").get("subject").get("reference"))

            # Get Patient from FHIR
            patient = self.get_by_id("Patient", patient_id)
            patient_source_id = self.get_patient_source_id(patient) if patient.get("identifier")[0].get("use") == "official" else patient_id

            # Get Observation from FHIR for each patient_id
            resources = ["Observation", "Condition"]
            list_of_resources = self.get_by_patient(resources, patient_id)

            observation_list = list_of_resources[0]
            condition_list = list_of_resources[1]

            # Get observations
            for link in observation_list.get("link"):
                if link.get("relation") == "next":
                    next_observation_page = link.get("url")

            observation_entries = []
            while observation_list.get("entry") is not None and len(observation_list.get("entry")) > 0:
                observation_entries.extend(observation_list.get("entry"))

                if next_observation_page is not None:
                    observation_list = self.fhir_conn.next(next_observation_page)  # Send the GET request to the FHIR API

                    next_observation_page = None
                    for link in observation_list.get("link"):
                        if link.get("relation") == "next":
                            next_observation_page = link.get("url")
                else:
                    observation_list = {}

            # Get conditions
            for link in condition_list.get("link"):
                if link.get("relation") == "next":
                    next_condition_page = link.get("url")

            condition_entries = []
            while condition_list.get("entry") is not None and len(condition_list.get("entry")) > 0:
                condition_entries.extend(condition_list.get("entry"))

                if next_condition_page is not None:
                    condition_list = self.fhir_conn.next(
                        next_condition_page)  # Send the GET request to the FHIR API

                    next_condition_page = None
                    for link in condition_list.get("link"):
                        if link.get("relation") == "next":
                            next_condition_page = link.get("url")
                else:
                    condition_list = {}

            patient_info = {"Patient_ID": patient_source_id}
            # patient_info = self.csv_to_dict("C:/Alejandro/BigDataAnalytics/Datos/template.csv")

            for i in observation_entries:
                    obs = i.get("resource")

                    if obs.get("component") is not None:
                        obs_mutations_key = obs.get("code").get("coding")[0].get("display") + " n. mutations"
                        obs_mutations_value = obs.get("component")[0].get("valueQuantity").get("value")

                        obs_load_key = obs.get("code").get("coding")[0].get("display") + " load"
                        obs_load_value = obs.get("component")[1].get("valueQuantity").get("value")

                        patient_info[obs_mutations_key] = str(obs_mutations_value)
                        patient_info[obs_load_key] = str(obs_load_value)
                    else:
                        obs_key = obs.get("code").get("coding")[0].get("display")
                        obs_value = obs.get("valueQuantity").get("value")
                        patient_info[obs_key] = str(obs_value)

            for i in condition_entries:
                    # print("Metiendo condiciones")
                    cond = i.get("resource")
                    cond_key = cond.get("bodySite")[0].get("text")
                    cond_value = int(1)
                    patient_info[cond_key] = cond_value

            output.append(patient_info)

        return mapper_response.MapperResponse(data=output)
