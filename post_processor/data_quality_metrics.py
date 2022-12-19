from abstracts.AbstractPostProcessor import APostProcessor


class data_quality_metrics(APostProcessor):
    def __init__(self, config):
        self.config = config

    def execute(self, data):
        metrics = {}
        for each in data:
            type = each.get("resourceType")
            if type not in metrics.keys():
                metrics[type] = 1
            else:
                count = metrics[type]
                metrics[type] = count + 1
        print(metrics)
        print("Data Quality Metrics")
