from typing import Callable, Tuple, List, Optional
from germaniumsb.local_types import \
    ResultEvaluator, \
    SelectorCall, \
    SelectorCallResult, \
    ProcessingCall

from germanium.static import Element, js, get_germanium
import pkg_resources


def inject_into_current_document() -> ProcessingCall:
    """
    Inject JS code into the document that allows picking
    the current element.

    :return:
    """
    script = pkg_resources.resource_string(__name__, "../js/main.js")
    if type(script) != 'str':  # it is bytes
        script = script.decode('utf-8')  # type: ignore

    def inject_into_document() -> Optional[SelectorCallResult]:
        if not is_germaniumsb_injected():
            js(script)
        
        return None

    return run_in_all_iframes(inject_into_document)


def start_picking_into_current_document(count) -> ProcessingCall:
    def start_picking_element() -> Optional[SelectorCallResult]:
        js('germaniumPickElement(%s);' % count)

        return None

    return run_in_all_iframes(start_picking_element)


def stop_picking_into_current_document() -> ProcessingCall:
    def stop_picking_element() -> Optional[SelectorCallResult]:
        js('germaniumStopPickingElement();')

        return None

    return run_in_all_iframes(stop_picking_element)


def is_germaniumsb_injected() -> bool:
    return js('return window["__germanium_loaded"];')


def run_in_all_iframes(code: SelectorCall, 
                       result_evaluator: ResultEvaluator=None) -> ProcessingCall:
    get_germanium().switch_to.default_content()

    def default_result_evaluator(result):
        return result, result

    if not result_evaluator:
        result_evaluator = default_result_evaluator

    return _run_in_all_iframes_internal(code, result_evaluator)


def _run_in_all_iframes_internal(
        code: SelectorCall,
        result_evaluator: ResultEvaluator,
        error_messages: List[str]=None,
        checked_frames=None) -> ProcessingCall:
    error_happened = False
    error_messages = error_messages if error_messages is not None else []
    checked_frames = checked_frames if checked_frames is not None else set()

    result = None
    result_found = False

    try:
        result = code()

        result, result_found = result_evaluator(result)

        if result_found:
            return result, result_found, error_happened, error_messages
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

        iframe_result, \
        iframe_result_found, \
        iframe_error_happened, \
        iframe_error_messages = \
            _run_in_all_iframes_internal(code,
                                         result_evaluator,
                                         error_messages,
                                         checked_frames)

        error_happened |= iframe_error_happened

        if iframe_result_found and not result_found:
            return iframe_result, \
                   iframe_result_found, \
                   error_happened, \
                   error_messages

    return result, result_found, error_happened, error_messages
