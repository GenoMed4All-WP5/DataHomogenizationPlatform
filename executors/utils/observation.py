from extensions.Genomed4All.mapping_tables.observationMapping import *
from extensions.Genomed4All.mapping_tables.mds_mock_data_map_columns import mapping


class Observation:

    code_dict = {"Hemoglobin_g_L": get_hemoglobin_code,
                 "SF3B1 result": get_oncogenetics_code}

    def get_observation_code(self, observation_type, observation_value, data):
        if observation_type in mapping.keys() and 'function' in mapping.get(observation_type).keys():
            print(mapping.get(observation_type))
            return mapping.get(observation_type).get('function')(observation_type, observation_value, data)
        else:
            return None
