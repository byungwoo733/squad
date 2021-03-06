import json
import math
from statistics import mean


from squad.core.utils import parse_name


test_result_mapping = {'pass': True, 'fail': False}


def parse_test_result(value):
    v = value.lower()
    return test_result_mapping.get(v, None)


class JSONTestDataParser(object):
    """
    Parser for test data as JSON string
    """

    @staticmethod
    def __call__(test_data):
        if test_data is None or test_data == '':
            return []

        input_data = json.loads(test_data)
        data = []
        for key, value in input_data.items():
            group_name, test_name = parse_name(key)
            data.append({
                "group_name": group_name,
                "test_name": test_name,
                "pass": parse_test_result(value),
            })
        return data


def parse_metric(value):
    if isinstance(value, list):
        return mean(value), value
    else:
        value = float(value)
        return value, [value]


class JSONMetricDataParser(object):
    """
    Parser for JSON metric data
    """

    @staticmethod
    def __call__(json_text):
        if json_text is None or json_text == '':
            return []

        input_data = json.loads(json_text)
        data = []

        for key, value in input_data.items():
            group_name, name = parse_name(key)
            result, measurements = parse_metric(value)
            if result and not (math.isnan(result) or math.isinf(result)):
                data.append({
                    "name": name,
                    "group_name": group_name,
                    "result": result,
                    "measurements": measurements,
                })

        return data
