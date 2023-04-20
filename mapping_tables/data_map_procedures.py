from extensions.DataHomogenizationPlatform.mapping_tables.conditionMapping import *

mapping = {"BMMD": {"key": "BMMD", "type": "hematological", "function": get_bmmd_code},
           "BMF": {"key": "BMF", "type": "hematological", "function": get_bmf_code},
           "del5q": {"key": "del5q", "type": "hematological", "function": get_del5q_code},
           "Lossofchr5ordel5qPLUSother": {"key": "Lossofchr5ordel5qPLUSother", "type": "hematological", "function": get_lossOfChr5Ordel5qPLUSother_code},
           "Lossofchr7ordel7q": {"key": "Lossofchr7ordel7q", "type": "hematological", "function": get_Lossofchr7ordel7q_code},
           "Lossofchr13ordel13q": {"key": "Lossofchr13ordel13q", "type": "hematological", "function": get_Lossofchr13ordel13q_code},
           "Lossofchr11ordel11q": {"key": "Lossofchr11ordel11q", "type": "hematological", "function": get_Lossofchr11ordel11q_code},
           "Gainofchr8": {"key": "Gainofchr8", "type": "hematological", "function": get_Gainofchr8_code},
           "Lossofchr9ordel9q": {"key": "Lossofchr9ordel9q", "type": "hematological", "function": get_Lossofchr9ordel9q_code},
           "Lossofchr12ordel12port12p": {"key": "Lossofchr12ordel12port12p", "type": "hematological", "function": get_Lossofchr12ordel12port12p_code},
           "Lossofchr20ordel20q": {"key": "Lossofchr20ordel20q", "type": "hematological", "function": get_Lossofchr20ordel20q_code},
           "LossofchrY": {"key": "LossofchrY", "type": "hematological", "function": get_LossofchrY_code}
           }
