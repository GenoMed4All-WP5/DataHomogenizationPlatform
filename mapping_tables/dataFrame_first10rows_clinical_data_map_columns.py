from extensions.DataHomogenizationPlatform.mapping_tables.observationMapping import *

mapping = {"Neutrophils": {"key": "Neutrophils", "type": "hematological", "function": get_neutrophils_code},
           "Hemoglobin": {"key": "Hemoglobin", "type": "hematological", "function": get_hemoglobin_code},
           "Platelets": {"key": "Platelets", "type": "hematological", "function": get_platelets_code},
           "LDH": {"key": "LDH", "type": "hematological", "function": get_ldh_code},
           "Ferritin": {"key": "Ferritin", "type": "hematological", "function": get_ferritin_code}
           }
