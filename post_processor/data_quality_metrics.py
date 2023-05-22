# evidently 0.1.59.dev3
from evidently.tests import *
from evidently.test_suite import TestSuite
from evidently.utils import NumpyEncoder
import json

class data_quality_metrics():
    def execute(self, data):
        # Define tests to perform
        tests = [TestNumberOfRows(), TestNumberOfColumns(), TestNumberOfNulls(), TestNumberOfColumnsWithNulls(),
                 TestNumberOfRowsWithNulls(), TestNumberOfConstantColumns(), TestNumberOfEmptyColumns()]
        # Create and execute Test Suite
        custom_data_quality_test = TestSuite(tests=tests)
        custom_data_quality_test.run(current_data=data, reference_data=None)

        # Convert tests output to json file
        tst_dic = custom_data_quality_test.as_dict()
        tst_json = json.loads(json.dumps(tst_dic, cls=NumpyEncoder))
        final_dict = {}
        tests_names = ['number_of_rows', 'number_of_columns', 'number_of_nulls', 'number_of_columns_with_nulls',
                       'number_of_rows_with_nulls', 'number_of_constant_columns', 'number_of_empty_columns']
        for i, test in enumerate(tst_json['tests']):
            if len(test['parameters']) == 0:
                final_dict[tests_names[i]] = 0
            else:
                final_dict[tests_names[i]] = test['parameters'][tests_names[i]]
        return(final_dict)


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
    post_pro = data_quality_metrics()
    result = post_pro.execute(sampled_data)
    print(result)'''