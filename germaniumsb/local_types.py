from typing import Callable, Tuple, Optional, List


class SelectorCallResult(object):
    pickCount: Optional[int]
    foundSelector: Optional[str]

    def __init__(self,
                 pickCount: Optional[int],
                 foundSelector: Optional[str]) -> None:
        """
        Initialization.
        """
        self.pickCount = pickCount
        self.foundSelector = foundSelector


ResultEvaluator = Callable[[SelectorCallResult], Tuple[SelectorCallResult, bool]]

ProcessingCall = Tuple[SelectorCallResult, bool, bool, List[str]]
