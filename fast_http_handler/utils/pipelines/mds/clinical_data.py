from main import Main


class clinical_data:

    def execute(self):
        id_path = "extensions/DataHomogenizationPlatform/profiles/mds_clinical_data_from_csv"
        sentence = ["--id", id_path]

        tags_my_main = Main()
        metrics = tags_my_main.main(sentence)
        return {"status": "Get Clinical features has been executed succesfully"}