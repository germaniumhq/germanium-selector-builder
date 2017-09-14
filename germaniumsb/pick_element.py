from germanium.static import *

from germaniumsb.inject_code import run_in_all_iframes


def get_picked_element():
    """
    Finds if any element was selected in the browser.

    :return:
    """
    def fetch_element():
        element = js('var element = window["germaniumGetPickedElement"] && window["germaniumGetPickedElement"](); '
                     'return element;')

        return element

    return run_in_all_iframes(fetch_element)
