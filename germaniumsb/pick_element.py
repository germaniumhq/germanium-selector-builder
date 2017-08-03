from germanium.static import *


def get_picked_element(checked_frames=None):
    """
    Finds if any element was selected in the browser.

    :return:
    """
    checked_frames = checked_frames if checked_frames is not None else set()

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
        if iframe_element in checked_frames:
            continue

        checked_frames.add(iframe_element)

        get_germanium().switch_to.frame(iframe_element)
        element = get_picked_element(checked_frames)
        if element:
            return element

    return None
