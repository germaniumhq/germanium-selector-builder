from typing import Callable, Tuple, Optional, List


class SelectorCallResult(object):
    def __init__(self,
                 pickCount: int,
                 foundSelector: Optional[str]=None) -> None:
        """
        Initialization.
        """
        self.pickCount: int = pickCount
        self.foundSelector: Optional[str] = foundSelector

SelectorCall = Callable[[], Optional[SelectorCallResult]]

ResultEvaluator = Callable[[Optional[SelectorCallResult]], Tuple[Optional[SelectorCallResult], bool]]

ProcessingCall = Tuple[Optional[SelectorCallResult], bool, bool, List[str]]
