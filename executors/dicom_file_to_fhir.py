import base64
import json
import os

from PIL import Image
import io
from abstracts.AbstractMapper import AMapper
import numpy as np
from fhir.resources.media import Media
from fhir.resources.imagingstudy import ImagingStudy
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.attachment import Attachment
from fhir.resources.reference import Reference
from fhir.resources.identifier import Identifier

import uuid
from datetime import datetime
from extensions.DataHomogenizationPlatform.executors.utils.fhir_templates import *
import pydicom
from dateutil.parser import parse


class dicom_file_to_fhir(AMapper):

    def __init__(self, config):
        self.config = config
        self.image_height = 255
        self.image_weight = 255
        self.imaging_study_id = str(uuid.uuid4())

    def execute(self, item):
        output = []
        media = {}
        imaging_study = {}

        imaging_study = self.map_dicom_to_imaging_study(item)
        media = self.map_dicom_to_media(item)

        output = [imaging_study.json(), media.json()]
        return output

    def map_dicom_to_imaging_study(self, item):
        return self.create_imaging_study(item)

    def map_dicom_to_media(self, item):
        return self.create_media(item)

    def create_imaging_study(self, dicom_data):

        pydicom_image = dicom_data["pydicom_format"]
        data = fhir_imaging_study_template
        imaging_study_resource = ImagingStudy(**data)

        subject_reference = Reference.construct()
        subject_reference.reference = "Patient/" + pydicom_image.PatientID

        try:
            study_instance_uid = str(pydicom_image.StudyInstanceUID)
            identifier = Identifier.construct()
            identifier.system = "urn:dicom:uid"
            identifier.value = study_instance_uid
            imaging_study_resource.identifier = list()
            imaging_study_resource.identifier.append(identifier)
        except:
            pass

        accession_number = dicom_data.get("00800050", "Not provided")
        issuer = dicom_data.get("00800051", "Not provided")
        study_id = dicom_data.get("00200010", "Not provided")

        instance_started_datetime = parse(pydicom_image.InstanceCreationDate + " " + pydicom_image.InstanceCreationTime)

        study_started_datetime = parse(pydicom_image.StudyDate + " " + pydicom_image.StudyTime)

        based_on = dicom_data.get("00321064", "")

        referrer = dicom_data.get("00080090", "") + dicom_data.get("00080096", "")

        interpreter = dicom_data.get("00081060", "")

        number_of_instances = dicom_data.get("00201208", "")

        procedure_reference = dicom_data.get("00081032", "Not provided")
        procedure_code = dicom_data.get("00081032", "Not provided")

        try:
            location = dicom_data.get("00081040")
        except:
            location = dicom_data.get("00400243", "Not provided")

        reason_codeable = self.get_reason_codeable_concept(dicom_data)

        study_description = pydicom_image.StudyDescription

        series_uid = pydicom_image.SeriesInstanceUID
        series_number = pydicom_image.SeriesNumber
        series_modality = dicom_data.get("00080060", "Not provided")
        series_description = pydicom_image.SeriesDescription
        series_number_of_instances = dicom_data.get("00201209", "Not provided")
        series_body_site = dicom_data.get("00180015", "Not provided")
        series_laterality = dicom_data.get("00200060", "Not provided")
        series_specimen = dicom_data.get("00400551", "") + dicom_data.get("00400562", "")
        series_started = dicom_data.get("00080021", "") + dicom_data.get("00080031", "")
        # (0008, 1050) | (0008, 1052) | (0008, 1070) | (0008, 1072)
        series_performer = dicom_data.get("00081050", "Not provided")

        instance_uid = pydicom_image.SOPInstanceUID
        instance_sop_class = pydicom_image.SOPClassUID
        instance_number = pydicom_image.InstanceNumber

        #(0008,0008) | (0007,0080) | (0040,A043) + (0008,0104) | (0042,0010)
        instance_title = dicom_data.get("00080008", "Not provided")

        try:
            modality = Coding.construct()
            modality.system = "http://terminology.hl7.org/CodeSystem/media-modality"
            modality.code = pydicom_image.Modality

            imaging_study_resource.modality = CodeableConcept.construct()
            imaging_study_resource.modality.coding = list()
            imaging_study_resource.modality.coding.append(modality)
        except Exception as ex:
            pass

        output = imaging_study_resource

        return output

    def create_media(self, dicom_data):

        template = fhir_media_template

        template["height"] = self.image_height
        template["width"] = self.image_weight

        image_id = str(uuid.uuid4())

        template["id"] = image_id

        media_resource = Media(**template)

        pydicom_image = dicom_data["pydicom_format"]

        try:
            modality = Coding.construct()
            modality.system = "http://terminology.hl7.org/CodeSystem/media-modality"
            modality.code = pydicom_image.Modality

            media_resource.modality = CodeableConcept.construct()
            media_resource.modality.coding = list()
            media_resource.modality.coding.append(modality)
        except Exception as ex:
            pass

        imaging_study_reference = Reference.construct()
        imaging_study_reference.reference = "ImagingStudy/" + self.imaging_study_id

        subject_reference = Reference.construct()
        subject_reference.reference = "Patient/" + pydicom_image.PatientID

        template["createdDateTime"] = pydicom_image.InstanceCreationDate + pydicom_image.InstanceCreationTime

        try:
            reason_codeable = self.get_reason_codeable_concept(dicom_data)

            media_resource.reasonCode = list()
            media_resource.reasonCode.append(reason_codeable)

        except:
            pass

        try:
            body_site = Coding.construct()
            body_site.system = ""
            body_site.code = dicom_data.get("00180015", "Not provided")
        except:
            pass

        img = dicom_data["scaled_image"]
        mgByteArr = io.BytesIO()
        img.thumbnail((self.image_height, self.image_weight))
        img.save(mgByteArr, format='JPEG')
        imgByteArr = mgByteArr.getvalue()
        thumb_string = (base64.b64encode(imgByteArr)).decode("utf-8")

        content = Attachment.construct()
        content.contentType = "image/dicom"
        content.creation = pydicom_image.InstanceCreationDate + pydicom_image.InstanceCreationTime
        content.data = thumb_string
        content.id = os.path.basename(pydicom_image.filename)

        media_resource.content = content

        img_file = open('C:\\Users\\vmateosresin\\PycharmProjects\\data\\output\\images\\' +
                        os.path.basename(pydicom_image.filename).split(".")[0] + ".jpeg", 'wb')
        img_file.write(imgByteArr)
        img_file.close()
        return media_resource

    def get_reason_codeable_concept(self, dicom_data):
        reason = Coding.construct()
        reason.system = ""
        reason.code = dicom_data.get("00401002", "Not provided")
        reason_codeable = CodeableConcept.construct()
        reason_codeable.coding = list()
        reason_codeable.coding.append(reason)
        return reason_codeable
