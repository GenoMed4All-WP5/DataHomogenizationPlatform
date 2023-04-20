from main import Main


class feature_extraction:

    def execute(self):
        id_path = "extensions/DataHomogenizationPlatform/profiles/mds_feature_extraction"
        sentence = ["--id", id_path]

        tags_my_main = Main()
        metrics = tags_my_main.main(sentence)
        return {"status": "Export MDS features has been executed succesfully"}