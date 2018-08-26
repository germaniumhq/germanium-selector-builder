from enum import Enum
from typing import Any, Dict, Optional, Callable
import uuid


class BrowserState(Enum):
    NOT_INITIALIZED = 'NOT_INITIALIZED'
    STOPPED = 'STOPPED'
    STARTED = 'STARTED'
    ERROR = 'ERROR'
    INJECTING_CODE = 'INJECTING_CODE'
    INJECTING_CODE_FAILED = 'INJECTING_CODE_FAILED'
    READY = 'READY'
    PICKING = 'PICKING'
    GENERATING_SELECTOR = 'GENERATING_SELECTOR'
    PAUSED = 'PAUSED'
    BROWSER_NOT_STARTED = 'BROWSER_NOT_STARTED'
    BROWSER_NOT_READY = 'BROWSER_NOT_READY'


STATE_INDEX = {
    'NOT_INITIALIZED': 0,
    'STOPPED': 1,
    'STARTED': 2,
    'ERROR': 3,
    'INJECTING_CODE': 4,
    'INJECTING_CODE_FAILED': 5,
    'READY': 6,
    'PICKING': 7,
    'GENERATING_SELECTOR': 8,
    'PAUSED': 9,
    'BROWSER_NOT_STARTED': 10,
    'BROWSER_NOT_READY': 11,
}


class BrowserStateChangeEvent(object):
    """
    Event that gets on all the before/after callbacks that are
    triggered on state changes.
    """

    def __init__(self,
                 previous_state: Optional[BrowserState],
                 target_state: BrowserState,
                 data: Any) -> None:
        """
        Create a new event.

        :param BrowserState previous_state: The state that the state machine is transitioning from.
        :param BrowserState target_state: The state that the state machine is transitioning to.
        :param object data: Optional data that is passed in the event.
        """
        self._previous_state = previous_state
        self._target_state = target_state
        self.data = data
        self._cancelled = False

    def cancel(self) -> None:
        """
        Cancel the current transition.
        """
        self._cancelled = True

    @property
    def cancelled(self) -> bool:
        """
        Is the current transition cancelled.
        :return:
        """
        return self._cancelled

    @property
    def previous_state(self) -> BrowserState:
        """
        The state from which we're transitioning.
        :return:
        """
        return self._previous_state

    @property
    def target_state(self) -> BrowserState:
        """
        Thestate towards we're transitioning.
        :return:
        """
        return self._target_state


class BrowserStateException(Exception):
    pass


transition_set: Dict[int, bool] = dict()
link_map: Dict[BrowserState, Dict[str, BrowserState]] = dict()


def register_transition(name: str, from_state: BrowserState, to_state: BrowserState) -> None:
    transition_set[STATE_INDEX[from_state.value] << 14 | STATE_INDEX[to_state.value]] = True

    if not name:
        return

    fromMap = link_map.get(from_state.value)

    if not fromMap:
        fromMap = link_map[from_state.value] = dict()

    fromMap[name] = to_state


register_transition('application_initialized', BrowserState.NOT_INITIALIZED, BrowserState.STOPPED)
register_transition('start_browser', BrowserState.STOPPED, BrowserState.STARTED)
register_transition('pick', BrowserState.STOPPED, BrowserState.BROWSER_NOT_STARTED)
register_transition('inject_code', BrowserState.STARTED, BrowserState.INJECTING_CODE)
register_transition('error', BrowserState.STARTED, BrowserState.ERROR)
register_transition('close_browser', BrowserState.STARTED, BrowserState.STOPPED)
register_transition('pick', BrowserState.STARTED, BrowserState.BROWSER_NOT_READY)
register_transition('close_browser', BrowserState.ERROR, BrowserState.STOPPED)
register_transition('error_processed', BrowserState.ERROR, BrowserState.STARTED)
register_transition('ready', BrowserState.INJECTING_CODE, BrowserState.READY)
register_transition('error_injecting_code', BrowserState.INJECTING_CODE, BrowserState.INJECTING_CODE_FAILED)
register_transition('error', BrowserState.INJECTING_CODE, BrowserState.ERROR)
register_transition('close_browser', BrowserState.INJECTING_CODE, BrowserState.STOPPED)
register_transition('pick', BrowserState.INJECTING_CODE, BrowserState.BROWSER_NOT_READY)
register_transition('ready', BrowserState.INJECTING_CODE_FAILED, BrowserState.READY)
register_transition('error_processed', BrowserState.INJECTING_CODE_FAILED, BrowserState.READY)
register_transition('close_browser', BrowserState.INJECTING_CODE_FAILED, BrowserState.STOPPED)
register_transition('pick', BrowserState.READY, BrowserState.PICKING)
register_transition('generate_selector', BrowserState.READY, BrowserState.GENERATING_SELECTOR)
register_transition('error', BrowserState.READY, BrowserState.ERROR)
register_transition('close_browser', BrowserState.READY, BrowserState.STOPPED)
register_transition('inject_code', BrowserState.READY, BrowserState.INJECTING_CODE)
register_transition('toggle_pause', BrowserState.READY, BrowserState.PAUSED)
register_transition('generate_selector', BrowserState.PICKING, BrowserState.GENERATING_SELECTOR)
register_transition('cancel_pick', BrowserState.PICKING, BrowserState.READY)
register_transition('error', BrowserState.PICKING, BrowserState.ERROR)
register_transition('close_browser', BrowserState.PICKING, BrowserState.STOPPED)
register_transition('toggle_pause', BrowserState.PICKING, BrowserState.PAUSED)
register_transition('toggle_pause', BrowserState.PAUSED, BrowserState.READY)
register_transition('close_browser', BrowserState.PAUSED, BrowserState.STOPPED)
register_transition('ready', BrowserState.GENERATING_SELECTOR, BrowserState.READY)
register_transition('error', BrowserState.GENERATING_SELECTOR, BrowserState.ERROR)
register_transition('close_browser', BrowserState.GENERATING_SELECTOR, BrowserState.STOPPED)
register_transition('error_processed', BrowserState.BROWSER_NOT_STARTED, BrowserState.STOPPED)
register_transition('error_processed', BrowserState.BROWSER_NOT_READY, BrowserState.STARTED)


ChangeStateEventListener = Callable[[BrowserStateChangeEvent], Optional[BrowserState]]


class BrowserStateMachine(object):
    def __init__(self, initial_state: Optional[BrowserState]=None) -> None:
        self._transition_listeners: Dict[str, EventListener] = dict()
        self._data_listeners: Dict[str, EventListener] = dict()
        self._initial_state = initial_state or BrowserState.NOT_INITIALIZED

        self._transition_listeners['NOT_INITIALIZED'] = EventListener()
        self._transition_listeners['STOPPED'] = EventListener()
        self._transition_listeners['STARTED'] = EventListener()
        self._transition_listeners['ERROR'] = EventListener()
        self._transition_listeners['INJECTING_CODE'] = EventListener()
        self._transition_listeners['INJECTING_CODE_FAILED'] = EventListener()
        self._transition_listeners['READY'] = EventListener()
        self._transition_listeners['PICKING'] = EventListener()
        self._transition_listeners['GENERATING_SELECTOR'] = EventListener()
        self._transition_listeners['PAUSED'] = EventListener()
        self._transition_listeners['BROWSER_NOT_STARTED'] = EventListener()
        self._transition_listeners['BROWSER_NOT_READY'] = EventListener()
        self._data_listeners['NOT_INITIALIZED'] = EventListener()
        self._data_listeners['STOPPED'] = EventListener()
        self._data_listeners['STARTED'] = EventListener()
        self._data_listeners['ERROR'] = EventListener()
        self._data_listeners['INJECTING_CODE'] = EventListener()
        self._data_listeners['INJECTING_CODE_FAILED'] = EventListener()
        self._data_listeners['READY'] = EventListener()
        self._data_listeners['PICKING'] = EventListener()
        self._data_listeners['GENERATING_SELECTOR'] = EventListener()
        self._data_listeners['PAUSED'] = EventListener()
        self._data_listeners['BROWSER_NOT_STARTED'] = EventListener()
        self._data_listeners['BROWSER_NOT_READY'] = EventListener()
        self._currentState = None  # type: Optional[BrowserState]
        self._current_change_state_event = None  # type: Optional[BrowserStateChangeEvent]

    @property
    def state(self) -> BrowserState:
        self._ensure_state_machine_initialized()
        return self._currentState

    def application_initialized(self, data: Any=None) -> BrowserState:
        return self.transition("application_initialized", data)

    def start_browser(self, data: Any=None) -> BrowserState:
        return self.transition("start_browser", data)

    def pick(self, data: Any=None) -> BrowserState:
        return self.transition("pick", data)

    def inject_code(self, data: Any=None) -> BrowserState:
        return self.transition("inject_code", data)

    def error(self, data: Any=None) -> BrowserState:
        return self.transition("error", data)

    def close_browser(self, data: Any=None) -> BrowserState:
        return self.transition("close_browser", data)

    def error_processed(self, data: Any=None) -> BrowserState:
        return self.transition("error_processed", data)

    def ready(self, data: Any=None) -> BrowserState:
        return self.transition("ready", data)

    def error_injecting_code(self, data: Any=None) -> BrowserState:
        return self.transition("error_injecting_code", data)

    def generate_selector(self, data: Any=None) -> BrowserState:
        return self.transition("generate_selector", data)

    def toggle_pause(self, data: Any=None) -> BrowserState:
        return self.transition("toggle_pause", data)

    def cancel_pick(self, data: Any=None) -> BrowserState:
        return self.transition("cancel_pick", data)

    def _ensure_state_machine_initialized(self) -> None:
        if not self._currentState:
            self._change_state_impl(self._initial_state, None)

    def changeState(self, targetState: BrowserState, data: Any=None) -> BrowserState:
        self._ensure_state_machine_initialized()
        return self._change_state_impl(targetState, data)

    def _change_state_impl(self, targetState: BrowserState, data: Any=None) -> BrowserState:
        if not targetState:
            raise Exception("No target state specified. Can not change the state.")

        # this also ignores the fact that maybe there is no transition
        # into the same state.
        if targetState == self._currentState:
            return targetState

        state_change_event: BrowserStateChangeEvent = BrowserStateChangeEvent(self._currentState, targetState, data)

        if self._currentState and \
                not transition_set.get(STATE_INDEX[self._currentState.value] << 14 | STATE_INDEX[targetState.value]):
            print("No transition exists between %s -> %s." % (self._currentState.value, targetState.value))
            return self._currentState

        if self._current_change_state_event:
            raise BrowserStateException(
                "The BrowserStateMachine is already in a changeState (%s -> %s). "
                "Transitioning the state machine (%s -> %s) in `before` events is not supported." % (
                    self._current_change_state_event.previous_state.value,
                    self._current_change_state_event.target_state.value,
                    self._currentState.value,
                    targetState.value
                ))

        self._current_change_state_event = state_change_event

        if state_change_event.previous_state:
            self._transition_listeners[state_change_event.previous_state.value]\
                .fire(EventType.BEFORE_LEAVE, state_change_event)

        self._transition_listeners[state_change_event.target_state.value]\
            .fire(EventType.BEFORE_ENTER, state_change_event)

        if state_change_event.cancelled:
            return self._currentState

        self._currentState = targetState
        self._current_change_state_event = None

        if state_change_event.previous_state:
            self._transition_listeners[state_change_event.previous_state.value]\
                .fire(EventType.AFTER_LEAVE, state_change_event)

        self._transition_listeners[state_change_event.target_state.value]\
            .fire(EventType.AFTER_ENTER, state_change_event)

        return self._currentState

    def transition(self, link_name: str, data: Any=None) -> BrowserState:
        """
        Transition into another state following a named transition.

        :param str link_name:
        :param object data:
        :return: BrowserState
        """
        self._ensure_state_machine_initialized()

        assert self._currentState

        source_state = link_map.get(self._currentState.value)

        if not source_state:
            return None

        if link_name not in source_state:
            print("There is no transition named `%s` starting from `%s`." %
                  (link_name, self._currentState.value))

            return None

        targetState = source_state[link_name]

        if not targetState:
            return None

        return self.changeState(targetState, data)

    def before_enter(self, state: BrowserState, callback: Callable[[BrowserStateChangeEvent], Optional[BrowserState]]):
        """
        Add a transition listener that will fire before entering a new state.
        The transition can still be cancelled at this stage via `ev.cancel()`
        in the callback.

        :param BrowserState state:
        :param Function callback:
        :return:
        """
        return self._transition_listeners[state.value].add_listener(EventType.BEFORE_ENTER, callback)

    def after_enter(self, state: BrowserState, callback: Callable[[BrowserStateChangeEvent], Optional[BrowserState]]):
        """
        Add a transition listener that will fire after the new state is entered.
        The transition can not be cancelled at this stage.
        :param BrowserState state:
        :param callback:
        :return:
        """
        return self._transition_listeners[state.value].add_listener(EventType.AFTER_ENTER, callback)

    def before_leave(self, state: BrowserState, callback: Callable[[BrowserStateChangeEvent], Optional[BrowserState]]):
        """
        Add a transition listener that will fire before leaving a state.
        The transition can be cancelled at this stage via `ev.cancel()`.

        :param BrowserState state:
        :param callback:
        :return:
        """
        return self._transition_listeners[state.value].add_listener(EventType.BEFORE_LEAVE, callback)

    def after_leave(self, state, callback):
        """
        Add a transition listener that will fire after leaving a state.
        The transition can not be cancelled at this stage.

        :param BrowserState state:
        :param callback:
        :return:
        """
        return self._transition_listeners[state.value].add_listener(EventType.AFTER_LEAVE, callback)

    def on_data(self, state: BrowserState, callback: Callable[[Any], Optional[BrowserState]]):
        """
        Add a data listener that will be called when data is being pushed for that transition.

        :param BrowserState state:
        :param callback:
        :return:
        """
        return self._data_listeners[state.value].add_listener(EventType.DATA, callback)

    def forward_data(self, new_state: BrowserState, data: Any) -> None:
        """
        Changes the state machine into the new state, then sends the data
        ignoring the result. This is so on `onData` calls we can just
        short-circuit the execution using: `return stateMachine.forwardData(..)`

        @param new_state The state to transition into.
        @param data The data to send.
        """
        self.send_data(new_state, data)

        return None

    def send_state_data(self, new_state: BrowserState, data: Any) -> BrowserState:
        """
        Sends the data into the state machine, to be processed by listeners
        registered with `onData`.
        @param new_state
        @param data The data to send.
        """
        self._ensure_state_machine_initialized()

        assert self._currentState

        self.changeState(new_state, data)

        target_state = self._data_listeners[self._currentState.value].fire(EventType.DATA, data)

        if target_state:
            return self.changeState(target_state, data)

        return self._currentState

    def send_data(self,
                  data: Any=None,
                  state: Optional[BrowserState]=None) -> BrowserState:
        """
        Transitions first the state machine into the new state, then it
        will send the data into the state machine.
        @param newState
        @param data
        """
        self._ensure_state_machine_initialized()

        assert self._currentState

        if state:
            self.changeState(state)

        target_state = self._data_listeners[self._currentState.value]\
            .fire(EventType.DATA, data)

        if target_state:
            return self.changeState(target_state, data)

        return self._currentState


class EventType(Enum):
    BEFORE_ENTER = 'before-enter'
    BEFORE_LEAVE = 'before-leave'
    AFTER_LEAVE = 'after-leave'
    AFTER_ENTER = 'after-enter'
    DATA = 'data'


class EventListenerRegistration(object):
    def __init__(self, event_listener, callback_id):
        self._event_listener = event_listener
        self._callback_id = callback_id

    def detach(self):
        self._event_listener.eventListeners.pop(self._callback_id)


class EventListener(object):
    def __init__(self):
        self.registered = dict()

    def add_listener(self, event_name, callback):
        event_listeners = self.registered.get(event_name.value)

        if not event_listeners:
            event_listeners = self.registered[event_name.value] = dict()

        callback_id = uuid.uuid4()
        event_listeners[callback_id] = callback

        return EventListenerRegistration(self, callback_id)

    def fire(self, event_type, ev):
        result = None

        if not self.registered.get(event_type.value):
            return

        listeners = self.registered[event_type.value]

        for callback in listeners.values():
            try:
                potential_result = callback.__call__(ev)

                if potential_result and result:
                    raise BrowserStateException("Data is already returned")

                result = potential_result
            except Exception as e:
                print(e)
                if isinstance(e, BrowserStateException):
                    raise e

        return result
