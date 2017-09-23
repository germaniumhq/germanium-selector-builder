from germanium.static import *

from germaniumsb.inject_code import run_in_all_iframes


def get_picked_element():
    """
    Finds if any element was selected in the browser.

    :return:
    """
    result = {"foundSelector": None, "pickCount": 10000}

    def fetch_element():
        element = js('var resultData = window["germaniumGetPickedElement"] && window["germaniumGetPickedElement"](); '
                     'return resultData;')

        return element

    def result_evaluator(call_result):
        if result["pickCount"] > call_result["pickCount"]:
            result["pickCount"] = call_result["pickCount"]

        if call_result['foundSelector']:
            result['foundSelector'] = call_result['foundSelector']
            return result, True

        return result, False

    return run_in_all_iframes(fetch_element, result_evaluator)
