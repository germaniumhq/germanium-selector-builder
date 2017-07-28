from germanium.static import *


def inject_into_current_document(error_messages=None):
    """
    Inject JS code into the document that allows picking
    the current element.

    :return:
    """
    error_happened = False
    error_messages = error_messages if error_messages else []

    find_element_script = ""

    try:
        if not js('return __germanium_loaded;'):
            js(find_element_script)
    except Exception as e:
        print(e)
        error_messages.append(str(e))
        error_happened = True

    for iframe_element in Element('iframe').element_list():
        get_germanium().switch_to.iframe(iframe_element)
        error_happened |= inject_into_current_document(error_messages)

    return error_happened, error_messages
