from extensions.DataHomogenizationPlatform.mapping_tables.observationMapping import *

mapping = {"SF3B1 result": {"key": "SF3B1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "SF3B1 n. mutations": {"key": "SF3B1 n. mutations", "type": "oncogenetics"},
           "SF3B1 load": {"key": "SF3B1 load", "type": "oncogenetics"},
           "ASXL1 result": {"key": "ASXL1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "ASXL1 n. mutations": {"key": "ASXL1 n. mutations", "type": "oncogenetics"},
           "ASXL1 load": {"key": "ASXL1 load", "type": "oncogenetics"},
           "ATRX result": {"key": "ATRX result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "ATRX n. mutations": {"key": "ATRX n. mutations", "type": "oncogenetics"},
           "ATRX load": {"key": "ATRX load", "type": "oncogenetics"},
           "BCOR result": {"key": "BCOR result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "BCOR n. mutations": {"key": "BCOR n. mutations", "type": "oncogenetics"},
           "BCOR load": {"key": "BCOR load", "type": "oncogenetics"},
           "BCORL1 result": {"key": "BCORL1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "BCORL1 n. mutations": {"key": "BCORL1 n. mutations", "type": "oncogenetics"},
           "BCORL1 load": {"key": "BCORL1 load", "type": "oncogenetics"},
           "BRAF result": {"key": "BRAF result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "BRAF n. mutations": {"key": "BRAF n. mutations", "type": "oncogenetics"},
           "BRAF load": {"key": "BRAF load", "type": "oncogenetics"},
           "CBL result": {"key": "CBL result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "CBL n. mutations": {"key": "CBL n. mutations", "type": "oncogenetics"},
           "CBL load": {"key": "CBL load", "type": "oncogenetics"},
           "CBLB result": {"key": "CBLB result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "CBLB n. mutations": {"key": "CBLB n. mutations", "type": "oncogenetics"},
           "CBLB load": {"key": "CBLB load", "type": "oncogenetics"},
           "CEBPA result": {"key": "CEBPA result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "CEBPA n. mutations": {"key": "CEBPA n. mutations", "type": "oncogenetics"},
           "CEBPA load": {"key": "CEBPA load", "type": "oncogenetics"},
           "DNMT3A result": {"key": "DNMT3A result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "DNMT3A n. mutations": {"key": "DNMT3A n. mutations", "type": "oncogenetics"},
           "DNMT3A load": {"key": "DNMT3A load", "type": "oncogenetics"},
           "ETV6 result": {"key": "ETV6 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "ETV6 n. mutations": {"key": "ETV6 n. mutations", "type": "oncogenetics"},
           "ETV6 load": {"key": "ETV6 load", "type": "oncogenetics"},
           "EZH2 result": {"key": "EZH2 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "EZH2 n. mutations": {"key": "EZH2 n. mutations", "type": "oncogenetics"},
           "EZH2 load": {"key": "EZH2 load", "type": "oncogenetics"},
           "FBXW7 result": {"key": "FBXW7 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "FBXW7 n. mutations": {"key": "FBXW7 n. mutations", "type": "oncogenetics"},
           "FBXW7 load": {"key": "FBXW7 load", "type": "oncogenetics"},
           "FLT3 result": {"key": "FLT3 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "FLT3 n. mutations": {"key": "FLT3 n. mutations", "type": "oncogenetics"},
           "FLT3 load": {"key": "FLT3 load", "type": "oncogenetics"},
           "GATA2 result": {"key": "GATA2 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "GATA2 n. mutations": {"key": "GATA2 n. mutations", "type": "oncogenetics"},
           "GATA2 load": {"key": "GATA2 load", "type": "oncogenetics"},
           "GNAS result": {"key": "GNAS result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "GNAS n. mutations": {"key": "GNAS n. mutations", "type": "oncogenetics"},
           "GNAS load": {"key": "GNAS load", "type": "oncogenetics"},
           "GNB1 result": {"key": "GNB1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "GNB1 n. mutations": {"key": "GNB1 n. mutations", "type": "oncogenetics"},
           "GNB1 load": {"key": "GNB1 load", "type": "oncogenetics"},
           "IDH1 result": {"key": "IDH1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "IDH1 n. mutations": {"key": "IDH1 n. mutations", "type": "oncogenetics"},
           "IDH1 load": {"key": "IDH1 load", "type": "oncogenetics"},
           "IDH2 result": {"key": "IDH2 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "IDH2 n. mutations": {"key": "IDH2 n. mutations", "type": "oncogenetics"},
           "IDH2 load": {"key": "IDH2 load", "type": "oncogenetics"},
           "JAK2 result": {"key": "JAK2 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "JAK2 n. mutations": {"key": "JAK2 n. mutations", "type": "oncogenetics"},
           "JAK2 load": {"key": "JAK2 load", "type": "oncogenetics"},
           "KIT result": {"key": "KIT result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "KIT n. mutations": {"key": "KIT n. mutations", "type": "oncogenetics"},
           "KIT load": {"key": "KIT load", "type": "oncogenetics"},
           "KRAS result": {"key": "KRAS result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "KRAS n. mutations": {"key": "KRAS n. mutations", "type": "oncogenetics"},
           "KRAS load": {"key": "KRAS load", "type": "oncogenetics"},
           "MPL result": {"key": "MPL result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "MPL n. mutations": {"key": "MPL n. mutations", "type": "oncogenetics"},
           "MPL load": {"key": "MPL load", "type": "oncogenetics"},
           "NF1 result": {"key": "NF1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "NF1 n. mutations": {"key": "NF1 n. mutations", "type": "oncogenetics"},
           "NF1 load": {"key": "NF1 load", "type": "oncogenetics"},
           "NOTCH1 result": {"key": "NOTCH1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "NOTCH1 n. mutations": {"key": "NOTCH1 n. mutations", "type": "oncogenetics"},
           "NOTCH1 load": {"key": "NOTCH1 load", "type": "oncogenetics"},
           "NPM1 result": {"key": "NPM1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "NPM1 n. mutations": {"key": "NPM1 n. mutations", "type": "oncogenetics"},
           "NPM1 load": {"key": "NPM1 load", "type": "oncogenetics"},
           "NRAS result": {"key": "NRAS result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "NRAS n. mutations": {"key": "NRAS n. mutations", "type": "oncogenetics"},
           "NRAS load": {"key": "NRAS load", "type": "oncogenetics"},
           "PHF6 result": {"key": "PHF6 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "PHF6 n. mutations": {"key": "PHF6 n. mutations", "type": "oncogenetics"},
           "PHF6 load": {"key": "PHF6 load", "type": "oncogenetics"},
           "PIGA result": {"key": "PIGA result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "PIGA n. mutations": {"key": "PIGA n. mutations", "type": "oncogenetics"},
           "PIGA load": {"key": "PIGA load", "type": "oncogenetics"},
           "PRPF40B result": {"key": "PRPF40B result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "PRPF40B n. mutations": {"key": "PRPF40B n. mutations", "type": "oncogenetics"},
           "PRPF40B load": {"key": "PRPF40B load", "type": "oncogenetics"},
           "PTPN11 result": {"key": "PTPN11 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "PTPN11 n. mutations": {"key": "PTPN11 n. mutations", "type": "oncogenetics"},
           "PTPN11 load": {"key": "PTPN11 load", "type": "oncogenetics"},
           "RAD21 result": {"key": "RAD21 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "RAD21 n. mutations": {"key": "RAD21 n. mutations", "type": "oncogenetics"},
           "RAD21 load": {"key": "RAD21 load", "type": "oncogenetics"},
           "RUNX1 (AML1) result": {"key": "RUNX1 (AML1) result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "RUNX1 (AML1) n. mutations": {"key": "RUNX1 (AML1) n. mutations", "type": "oncogenetics"},
           "RUNX1 (AML1) load": {"key": "RUNX1 (AML1) load", "type": "oncogenetics"},
           "SMC1A result": {"key": "SMC1A result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "SMC1A n. mutations": {"key": "SMC1A n. mutations", "type": "oncogenetics"},
           "SMC1A load": {"key": "SMC1A load", "type": "oncogenetics"},
           "SMC3 result": {"key": "SMC3 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "SMC3 n. mutations": {"key": "SMC3 n. mutations", "type": "oncogenetics"},
           "SMC3 load": {"key": "SMC3 load", "type": "oncogenetics"},
           "SRSF2 result": {"key": "SRSF2 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "SRSF2 n. mutations": {"key": "SRSF2 n. mutations", "type": "oncogenetics"},
           "SRSF2 load": {"key": "SRSF2 load", "type": "oncogenetics"},
           "STAG2 result": {"key": "STAG2 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "STAG2 n. mutations": {"key": "STAG2 n. mutations", "type": "oncogenetics"},
           "STAG2 load": {"key": "STAG2 load", "type": "oncogenetics"},
           "TET2 result": {"key": "TET2 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "TET2 n. mutations": {"key": "TET2 n. mutations", "type": "oncogenetics"},
           "TET2 load": {"key": "TET2 load", "type": "oncogenetics"},
           "TP53 result": {"key": "TP53 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "TP53 n. mutations": {"key": "TP53 n. mutations", "type": "oncogenetics"},
           "TP53 load": {"key": "TP53 load", "type": "oncogenetics"},
           "U2AF1 result": {"key": "U2AF1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "U2AF1 n. mutations": {"key": "U2AF1 n. mutations", "type": "oncogenetics"},
           "U2AF1 load": {"key": "U2AF1 load", "type": "oncogenetics"},
           "UTX (KDM6A) result": {"key": "UTX (KDM6A) result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "UTX (KDM6A) n. mutations": {"key": "UTX (KDM6A) n. mutations", "type": "oncogenetics"},
           "UTX (KDM6A) load": {"key": "UTX (KDM6A) load", "type": "oncogenetics"},
           "WT1 result": {"key": "WT1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "WT1 n. mutations": {"key": "WT1 n. mutations", "type": "oncogenetics"},
           "WT1 load": {"key": "WT1 load", "type": "oncogenetics"},
           "ZRSR2 result": {"key": "ZRSR2 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "ZRSR2 n. mutations": {"key": "ZRSR2 n. mutations", "type": "oncogenetics"},
           "ZRSR2 load": {"key": "ZRSR2 load", "type": "oncogenetics"},
           "CSF3R result": {"key": "CSF3R result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "CSF3R n. mutations": {"key": "CSF3R n. mutations", "type": "oncogenetics"},
           "CSF3R load": {"key": "CSF3R load", "type": "oncogenetics"},
           "SETBP1 result": {"key": "SETBP1 result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "SETBP1 n. mutations": {"key": "SETBP1 n. mutations", "type": "oncogenetics"},
           "SETBP1 load": {"key": "SETBP1 load", "type": "oncogenetics"},
           "CALR result": {"key": "CALR result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "CALR n. mutations": {"key": "CALR n. mutations", "type": "oncogenetics"},
           "CALR load": {"key": "CALR load", "type": "oncogenetics"},
           "PPM1D result": {"key": "PPM1D result", "type": "oncogenetics", "function": get_oncogenetics_code},
           "PPM1D n. mutations": {"key": "PPM1D n. mutations", "type": "oncogenetics"},
           "PPM1D load": {"key": "PPM1D load", "type": "oncogenetics"},
           "Hemoglobin_g_L": {"key": "Hemoglobin_g_L", "type": "hematological", "function": get_hemoglobin_code}
           }
