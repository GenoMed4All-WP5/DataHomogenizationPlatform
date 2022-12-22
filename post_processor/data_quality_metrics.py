from abstracts.AbstractPostProcessor import APostProcessor
# evidently 0.1.59.dev3
from evidently.tests import *
from evidently.test_suite import TestSuite
from evidently.metrics.base_metric import generate_column_metrics
from evidently.utils import NumpyEncoder
import json

class data_quality_metrics():
    def __init__(self, config):
        self.config = config

    def execute(self, data):
        # Parse desired tests from config
        columns = list(data.columns)
        tests = self.parse_test_conf(self.config, columns)

        # Create and execute Test Suite
        custom_data_quality_test = TestSuite(tests=tests)
        custom_data_quality_test.run(current_data=data, reference_data=None)

        # Convert tests output to json file
        tst_dic = custom_data_quality_test.as_dict()
        tst_json = json.loads(json.dumps(tst_dic, cls=NumpyEncoder))

        return(tst_json)

    def parse_test_conf(self, conf, columns):
        # Initialize tests output and dictionary of tests
        tests = []
        tests_dict = {'TestNumberOfRows': TestNumberOfRows(),
                      'TestNumberOfColumns': TestNumberOfColumns(),
                      'TestNumberOfNulls': TestNumberOfNulls(),
                      'TestNumberOfColumnsWithNulls': TestNumberOfColumnsWithNulls(),
                      'TestNumberOfRowsWithNulls': TestNumberOfRowsWithNulls(),
                      'TestColumnNumberOfNulls': generate_column_metrics(TestColumnNumberOfNulls, columns=columns),
                      'TestNumberOfConstantColumns': TestNumberOfConstantColumns(),
                      'TestNumberOfEmptyColumns': TestNumberOfEmptyColumns(),
                      }
        # Load tests included in cofig file
        for k, v in conf.items():
            if v == True:
                tests.append(tests_dict[k])
        return tests

# Example of config dict:
# config = {'TestNumberOfRows': True,
#           'TestNumberOfColumns': True,
#           'TestNumberOfNulls': True,
#           'TestNumberOfColumnsWithNulls': True,
#           'TestNumberOfRowsWithNulls': True,
#           'TestNumberOfConstantColumns': True,
#           'TestColumnNumberOfNulls': True,
#           'TestNumberOfEmptyColumns': True}

'''if __name__=="__main__":
    import pandas as pd
    import yaml
    data_path = "../data/transfusion_edited.csv"
    dataframe = pd.read_csv(data_path, sep=",")
    sampled_data = dataframe.sample(n=1000, replace=True)
    config_path = "../config/config.yaml"
    with open(config_path, 'r') as stream:
        config_dict = yaml.safe_load(stream)
    print(config_dict)
    post_pro = data_quality_metrics(config=config_dict)
    result = post_pro.execute(sampled_data)
    print(result)'''