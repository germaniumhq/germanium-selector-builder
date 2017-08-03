from germanium.static import *
import pkg_resources


def inject_into_current_document(error_messages=None):
    """
    Inject JS code into the document that allows picking
    the current element.

    :return:
    """
    error_happened = False
    error_messages = error_messages if error_messages else []

    script = pkg_resources.resource_string(__name__, "../js/find_element_script.js")
    if type(script) != 'str':  # it is bytes
        script = script.decode('utf-8')

    try:
        if not is_germaniumsb_injected():
            js(script)
    except Exception as e:
        print(e)
        error_messages.append(str(e))
        error_happened = True

    for iframe_element in Element('iframe').element_list():
        get_germanium().switch_to.frame(iframe_element)
        iframe_error_happened, iframe_error_messages = \
            inject_into_current_document(error_messages)

        error_happened |= iframe_error_happened

    return error_happened, error_messages


def start_picking_into_current_document(error_messages=None):
    error_happened = False
    error_messages = error_messages if error_messages else []

    try:
        if not js('return window["__germanium_picking_mode_enabled"];'):
            js('germaniumPickElement();')
    except Exception as e:
        print(e)
        error_messages.append(str(e))
        error_happened = True

    for iframe_element in Element('iframe').element_list():
        get_germanium().switch_to.frame(iframe_element)
        error_happened |= start_picking_into_current_document(error_messages)

    return error_happened, error_messages


def stop_picking_into_current_document(error_messages=None):
    error_happened = False
    error_messages = error_messages if error_messages else []

    try:
        if js('return window["__germanium_picking_mode_enabled"];'):
            js('germaniumStopPickingElement();')
    except Exception as e:
        print(e)
        error_messages.append(str(e))
        error_happened = True

    for iframe_element in Element('iframe').element_list():
        get_germanium().switch_to.frame(iframe_element)
        error_happened |= stop_picking_into_current_document(error_messages)

    return error_happened, error_messages


def is_germaniumsb_injected():
    return js('return window["__germanium_loaded"];')
