fhir_imaging_study_template = {
  "resourceType": "ImagingStudy",
  "id": "example",
  "status": "available",
  "subject": {
    "reference": "Patient/dicom"
  },
  "started": "2011-01-01T11:01:20+03:00",
  "numberOfSeries": 1,
  "numberOfInstances": 1,
  "series": [
    {
      "uid": "2.16.124.113543.6003.2588828330.45298.17418.2723805630",
      "number": 3,
      "modality": {
        "system": "http://dicom.nema.org/resources/ontology/DCM",
        "code": "CT"
      },
      "description": "CT Surview 180",
      "numberOfInstances": 1,
      "bodySite": {
        "system": "http://snomed.info/sct",
        "code": "67734004",
        "display": "Upper Trunk Structure"
      },
      "instance": [
        {
          "uid": "2.16.124.113543.6003.189642796.63084.16748.2599092903",
          "sopClass": {
            "system": "urn:ietf:rfc:3986",
            "code": "urn:oid:1.2.840.10008.5.1.4.1.1.2"
          },
          "number": 1
        }
      ]
    }
  ]
}

fhir_media_template = {
  "resourceType": "Media",
  "id": "example",
  "status": "completed",
  "type": {
    "coding": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/media-type",
        "code": "image",
        "display": "Image"
      }
    ]
  },
  "content": {
    "id": "a1",
    "contentType": "image/dicom",
    "data": "",
    "creation": "2009-09-03"
  }
}

fhir_patient_template = {
            "resourceType": "Patient",
            "identifier": [
                {
                    "use": "official",
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "PI"
                            }
                        ]
                    },
                    "system": "urn:oid:2.16.840.1.113883.2.9.3.12.4.1",
                    "period": {
                        "start": "1899-12-31T00:00:00+01:00"
                    },
                    "assigner": {
                        "display": "organization"
                    }
                }
            ],
            "managingOrganization": {
                "reference": "Organization"
            }
        }

fhir_organization_template = {
            "resourceType": "Organization",
            "type": [
                {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                            "code": "prov",
                            "display": "Healthcare Provider"
                        }
                    ]
                }
            ]
        }

fhir_encounter_template = {
            "resourceType": "Encounter",
            "status": "in-progress",
            "subject": {
                "reference": "Patient/example"
              },
            "serviceProvider": {
                "reference": "Organization/example"
              }
        }

fhir_condition_template = {
              "resourceType": "Condition",
              "id": "example-condition",
              "identifier": [{
                "use": "secondary",
                "value": "6323"
              }],
              "clinicalStatus": {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active",
                    "display": "Active"
                  }
                ]
              },
              "verificationStatus": {
                "coding": [
                  {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                    "code": "confirmed",
                    "display": "Confirmed"
                  }
                ]
              },
              "code": {
                "coding": [
                  {
                    "system": "http://snomed.info/sct",
                    "code": "195967001",
                    "display": "Fracture of forearm"
                  }
                ],
                "text": "Fractura de antebrazo"
              },
              "subject": {
                "reference": "Patient/example-patient"
              }
        }

fhir_observation_template = {
              "resourceType": "Observation",
              "id": "f001",
              "identifier": [{
                "use": "secondary",
                "value": "6323"
              }],
              "status": "final",
              "code": {
                "coding": [{
                  "system": "http://loinc.org",
                  "code": "15074-8",
                  "display": "Glucose [Moles/volume] in Blood"
                }]
              },
              "subject": {
                "reference": "Patient/f001"
              },
              "issued": "2013-04-03T15:30:10+01:00",
              "valueQuantity": {
                "value": 6.3,
                "unit": "mmol/l",
                "system": "http://unitsofmeasure.org",
                "code": "mmol/L"
              }
            }

fhir_procedure_template = {
              "resourceType": "Procedure",
              "id": "example-procedure",
              "status": "completed",
              "code": {
                "coding": [
                  {
                    "system": "http://snomed.info/sct",
                    "code": "387713003",
                    "display": "Appendectomy"
                  }
                ],
                "text": "Appendectomy"
              },
              "subject": {
                "reference": "Patient/example-patient"
              },
              "performedDateTime": "2023-04-18T10:30:00Z",
              "performer": [
                {
                  "actor": {
                    "reference": "Practitioner/example-practitioner"
                  },
                  "role": {
                    "coding": [
                      {
                        "system": "http://hl7.org/fhir/v3/ParticipationRole",
                        "code": "PPRF",
                        "display": "Primary Performed By"
                      }
                    ]
                  }
                }
              ],
              "location": {
                "reference": "Location/example-location"
              },
              "outcome": {
                "coding": [
                  {
                    "system": "http://hl7.org/fhir/procedure-outcome",
                    "code": "successful",
                    "display": "Successful"
                  }
                ]
              },
              "report": [
                {
                  "reference": "DiagnosticReport/example-report"
                }
              ],
              "note": [
                {
                  "text": "Patient had acute appendicitis"
                }
              ]
            }

fhir_medication_statement_template = {
              "resourceType": "MedicationStatement",
              "id": "example-medicationstatement",
              "status": "active",
              "medicationCodeableConcept": {
                "coding": [
                  {
                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                    "code": "1046202",
                    "display": "Atorvastatin 20mg tablet"
                  }
                ],
                "text": "Atorvastatin 20mg tablet"
              },
              "subject": {
                "reference": "Patient/example-patient"
              },
              "effectivePeriod": {
                "start": "2022-01-01",
                "end": "2023-04-18"
              },
              "note": [
                {
                  "text": "Patient takes one tablet daily in the evening"
                }
              ]
            }

fhir_diagnostic_report_template = {
                "resourceType": "DiagnosticReport",
                "id": "diagnostic_report_id",
                "meta": {
                    "profile": [
                        "http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/genomics-report"
                    ],
                    "id": "str(diagnostic_report_id)",
                    "lastUpdated": "datetima"
                },
                "status": "final",
                "category": [{
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/v2-0074",
                        "code": "GE"
                    }
                    ]
                }
                ],
                "code": {
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": 'self.config.get("GENOMED4ALL").get("use_case_snomed_code")'
                    },
                        {
                            "system": "http://www.ohdsi.org/omop",
                            "code": 'self.config.get("GENOMED4ALL").get("use_case_omop_code")'
                        }
                    ]
                },
                "subject": {
                    "reference": "Patient/" + 'patient_id'
                }
            }

fhir_identifier_template = {
                    "use": "official",
                    "type": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                "code": "PI"
                            }
                        ]
                    },
                    "system": "urn:oid:2.16.840.1.113883.2.9.3.12.4.1",
                    "period": {
                        "start": "1899-12-31T00:00:00+01:00"
                    },
                    "assigner": {
                        "display": "organization"
                    }
                }