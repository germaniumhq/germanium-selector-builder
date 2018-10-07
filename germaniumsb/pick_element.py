from typing import Any, Dict, Tuple, Optional

from germanium.static import js

from germaniumsb.inject_code import run_in_all_iframes
from germaniumsb.local_types import ProcessingCall, SelectorCallResult


def get_picked_element() -> ProcessingCall:
    """
    Finds if any element was selected in the browser.

    :return:
    """
    result = SelectorCallResult(
        foundSelector=None,
        pickCount=10000)

    def fetch_element() -> SelectorCallResult:
        element: Dict[str, Any] = js('var resultData = window["germaniumGetPickedElement"] && window["germaniumGetPickedElement"](); '
                                     'return resultData;')

        if not element or 'foundSelector' not in element:
            raise Exception(f"Unable to get element (was {element}) or no 'foundSelector' field present.")

        return SelectorCallResult(
            pickCount=element["pickCount"] if "pickCount" in element else 0,
            foundSelector=element["foundSelector"]
        )

    def result_evaluator(call_result: Optional[SelectorCallResult]) -> Tuple[Optional[SelectorCallResult], bool]:
        """
        Evaluates if the call to find a query actually found an element, since
        the JSON data might have missing fields, that will explode in the UI.
        """
        assert call_result

        if result.pickCount > call_result.pickCount:
            result.pickCount = call_result.pickCount

        if call_result.foundSelector:
            result.foundSelector = call_result.foundSelector
            return result, True

        return result, False

    return run_in_all_iframes(fetch_element, result_evaluator)
