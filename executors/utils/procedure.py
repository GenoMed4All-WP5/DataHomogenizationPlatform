from extensions.DataHomogenizationPlatform.mapping_tables.conditionMapping import *
from extensions.DataHomogenizationPlatform.mapping_tables.dataFrame_first10rows_clinical_data_map_conditions import mapping


class Procedure:

    def get_procedure_code(self, procedure_type, data):
        if procedure_type in mapping.keys() and 'function' in mapping.get(procedure_type).keys():
            print(mapping.get(procedure_type))
            return mapping.get(procedure_type).get('function')(procedure_type, data)
        else:
            return None