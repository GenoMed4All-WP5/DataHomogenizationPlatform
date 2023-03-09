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



'''data = {
            "resourceType": "Patient",
            "id": id,
            "meta": {
                "id": str(id),
                "lastUpdated": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            },
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
                    "value": input_data["patient_id"],
                    "period": {
                        "start": "1899-12-31T00:00:00+01:00"
                    },
                    "assigner": {
                        "display": self.config.get("GENOMED4ALL").get("organization")
                    }
                }
            ],
            "gender": self.translate_gender(input_data["patient_gender"]),
            "managingOrganization": {
                "reference": "Organization/" + str(organization_id)
            }
        }'''