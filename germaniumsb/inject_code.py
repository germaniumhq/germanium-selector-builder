from germanium.static import *
import pkg_resources


def inject_into_current_document():
    """
    Inject JS code into the document that allows picking
    the current element.

    :return:
    """
    script = pkg_resources.resource_string(__name__, "../js/find_element_script.js")
    if type(script) != 'str':  # it is bytes
        script = script.decode('utf-8')

    def inject_into_document():
        if not is_germaniumsb_injected():
            js(script)

    return run_in_all_iframes(inject_into_document)


def start_picking_into_current_document():
    def start_picking_element():
        if not js('return window["__germanium_picking_mode_enabled"];'):
            js('germaniumPickElement();')

    return run_in_all_iframes(start_picking_element)


def stop_picking_into_current_document():
    def stop_picking_element():
        if js('return window["__germanium_picking_mode_enabled"];'):
            js('germaniumStopPickingElement();')

    return run_in_all_iframes(stop_picking_element)


def is_germaniumsb_injected():
    return js('return window["__germanium_loaded"];')


def run_in_all_iframes(code, error_messages=None, checked_frames=None):
    error_happened = False
    error_messages = error_messages if error_messages is not None else []
    checked_frames = checked_frames if checked_frames is not None else set()

    result = None

    try:
        result = code()
    except Exception as e:
        print(e)
        error_messages.append(str(e))
        error_happened = True

    for iframe_element in Element('iframe').element_list():
        if iframe_element in checked_frames:
            continue

        checked_frames.add(iframe_element)

        try:
            get_germanium().switch_to.frame(iframe_element)
        except Exception:
            # it's ok to have switching failing if the iframes are being
            # switcharoeed
            continue

        iframe_result, iframe_error_happened, iframe_error_messages = \
            run_in_all_iframes(code, error_messages, checked_frames)

        error_happened |= iframe_error_happened

        if iframe_result and not result:
            result = iframe_result

    return result, error_happened, error_messages
