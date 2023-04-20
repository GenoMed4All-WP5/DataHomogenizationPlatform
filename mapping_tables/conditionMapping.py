import math

def get_bmmd_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                    "coding": [
                      {
                        "system": "http://snomed.info/sct",
                        "code": "405717004"
                      },
                      {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "4228474"
                      }
                    ],
                    "text": "Bone marrow multilineage dysplasia"
                  },
            "category": [{
                    "coding": [
                      {
                        "system": "http://snomed.info/sct",
                        "code": "25723000"
                      }
                    ],
                    "text": "Dysplasia"
                  }],
            "bodySite": [
                    {
                      "coding": [
                        {
                          "system": "http://snomed.info/sct",
                          "code": "279729006"
                        }
                      ],
                      "text": "All bone marrow"
                    }
            ]
        }

        return data
    else:
        return None

def get_bmf_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "52967002"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "4097745"
                    }
                ],
                "text": "Bone marrow fibrosis"
            },
            "category": [{
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "127035006"
                    }
                ],
                "text": "Bone marrow disorder"
            }],
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "279729006"
                        }
                    ],
                    "text": "All bone marrow"
                }
            ]
        }

        return data
    else:
        return None

def get_del5q_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "726372008"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37118014"
                    }
                ],
                "text": "del(5q)"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "12399004"
                        }
                    ],
                    "text": "Chromosome pair 5"
                }
            ]
        }

        return data
    else:
        return None

def get_lossOfChr5Ordel5qPLUSother_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "726372008"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37118014"
                    }
                ],
                "text": "Loss of chr 5 or del(5q) + other"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "70488008"
                        }
                    ],
                    "text": "Chromosome pair 7"
                }
            ]
        }

        return data
    else:
        return None

def get_Lossofchr7ordel7q_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "726377002"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37111439"
                    }
                ],
                "text": "Loss of chr 7 or del(7q)"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "70488008"
                        }
                    ],
                    "text": "Chromosome pair 7"
                }
            ]
        }

        return data
    else:
        return None

def get_Lossofchr13ordel13q_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "726384005"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37111444"
                    }
                ],
                "text": "Loss of chr 13 or del(13q)"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "55401003"
                        }
                    ],
                    "text": "Chromosome pair 13"
                }
            ]
        }

        return data
    else:
        return None

def get_Lossofchr11ordel11q_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "726381002"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37117276"
                    }
                ],
                "text": "Loss of chr 11 or del(11q)"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "4037698"
                        }
                    ],
                    "text": "Chromosome pair 11"
                }
            ]
        }

        return data
    else:
        return None

def get_Gainofchr8_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://naaccr.org/naaccrxml",
                        "code": "melanoma_choroid@2861@010"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "35934506"
                    }
                ],
                "text": "Gain in chromosome 8q"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "77826001"
                        }
                    ],
                    "text": "Chromosome pair 8"
                }
            ]
        }

        return data
    else:
        return None

def get_Lossofchr9ordel9q_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "726379004"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37111441"
                    }
                ],
                "text": "Loss of chr 9 or del(9q)"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "13526007"
                        }
                    ],
                    "text": "Chromosome pair 9"
                }
            ]
        }

        return data
    else:
        return None

def get_Lossofchr12ordel12port12p_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "726381002"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37117276"
                    }
                ],
                "text": "Loss of chr 12 or del(12p)"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "17897000"
                        }
                    ],
                    "text": "Chromosome pair 12"
                }
            ]
        }

        return data
    else:
        return None

def get_Lossofchr20ordel20q_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "726395004"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37111454"
                    }
                ],
                "text": "Loss of chr 20 or del(20p)"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "25610001"
                        }
                    ],
                    "text": "Chromosome pair 20"
                }
            ]
        }

        return data
    else:
        return None

def get_LossofchrY_code(key, value, clinical_data):
    if value is not None and not math.isnan(value) and value != 'NA':

        data = {
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": "717158001"
                    },
                    {
                        "system": "http://www.ohdsi.org/omop",
                        "code": "37397119"
                    }
                ],
                "text": "Loss of chr Y"
            },
            "bodySite": [
                {
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "25610001"
                        }
                    ],
                    "text": "Chromosome Y"
                }
            ]
        }

        return data
    else:
        return None
