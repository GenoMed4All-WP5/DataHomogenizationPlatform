import uuid

from abstracts.AbstractMapper import AMapper
from config.config import Config
from inputconnectors.ELKConnection import ELKConnection


class vcf_file_to_fhir(AMapper):
    exists_index = None
    esConn = None

    def __init__(self):
        if self.esConn is None:
            self.esConn = ELKConnection()
            context = {"curl": Config.config["ourl"]}
            self.esConn.connect(context)

    def execute(self, item):
        output = []
        results = []
        diagnostic_report = {}
        id_list = {}

        for key, value in item.items():
            if key != "contained" and key != "results":
                diagnostic_report[key] = value
            elif key == "contained":
                for resource in value:
                    old_id = resource["id"]
                    resource_type = resource["resourceType"]
                    resource_index = (Config.config["genomed4all.tenant"] + "-" + resource_type).lower()
                    resource_doctype = "_doc"
                    id = str(uuid.uuid4())
                    id_list[old_id] = {"id": id, "resourceType": resource_type, "reference": resource_type + "/" + id}
                    resource["id"] = id
                    resource["_index"] = resource_index
                    resource["_odoctype"] = resource_doctype
                    results.append({"reference": resource_type + '/' + id})
                    output.append(resource)
            else:
                pass

        output_len = range(len(output))
        for iterator in output_len:
            if "derivedFrom" in output[iterator]:
                derivedFrom_array_len = range(len(output[iterator]["derivedFrom"]))
                for derivedFrom_iterator in derivedFrom_array_len:
                    reference_value = output[iterator]["derivedFrom"][derivedFrom_iterator]["reference"]
                    if reference_value[1:] in id_list:
                        output[iterator]["derivedFrom"][derivedFrom_iterator]["reference"] = id_list[reference_value[1:]]["reference"]

        if results is not None:
            diagnostic_report["result"] = results
        output.append(diagnostic_report)

        return output