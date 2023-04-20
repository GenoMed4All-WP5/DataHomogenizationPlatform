from extensions.DataHomogenizationPlatform.mapping_tables.conditionMapping import *
from extensions.DataHomogenizationPlatform.mapping_tables.dataFrame_first10rows_clinical_data_map_conditions import mapping


class Condition:

    def get_condition_code(self, condition_type, condition_value, data):
        if condition_type in mapping.keys() and 'function' in mapping.get(condition_type).keys():
            print(mapping.get(condition_type))
            return mapping.get(condition_type).get('function')(condition_type, condition_value, data)
        else:
            return None