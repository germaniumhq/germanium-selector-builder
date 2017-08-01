from germanium.static import *


def get_picked_element():
    """
    Finds if any element was selected in the browser.

    :return:
    """
    try:
        get_germanium().switch_to.default_content()
        element = js('var element = window["__germanium_element"]; '
                     'window["__germanium_element"] = null; '
                     'return element;')
        if element:
            return element
    except Exception as e:
        print(e)

    for iframe_element in Element('iframe').element_list():
        get_germanium().switch_to.iframe(iframe_element)
        element = get_picked_element()
        if element:
            return element

    return None
