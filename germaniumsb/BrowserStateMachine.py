from enum import Enum
import uuid


class BrowserState(Enum):
    STOPPED = 'STOPPED'
    STARTED = 'STARTED'
    ERROR = 'ERROR'
    INJECTING_CODE = 'INJECTING_CODE'
    READY = 'READY'
    PICKING = 'PICKING'
    GENERATING_SELECTOR = 'GENERATING_SELECTOR'
    BROWSER_NOT_STARTED = 'BROWSER_NOT_STARTED'
    BROWSER_NOT_READY = 'BROWSER_NOT_READY'


STATE_INDEX = {
    'STOPPED': 0,
    'STARTED': 1,
    'ERROR': 2,
    'INJECTING_CODE': 3,
    'READY': 4,
    'PICKING': 5,
    'GENERATING_SELECTOR': 6,
    'BROWSER_NOT_STARTED': 7,
    'BROWSER_NOT_READY': 8,
}


class BrowserStateChangeEvent(object):
    """
    Event that gets on all the before/after callbacks that are
    triggered on state changes.
    """

    def __init__(self, previous_state, target_state, data):
        """
        Create a new event.

        :param BrowserState previous_state: The state that the state machine is transitioning from.
        :param BrowserState target_state: The state that the state machine is transitioning to.
        :param object data: Optional data that is passed in the event.
        """
        self._previousState = previous_state
        self._targetState = target_state
        self.data = data
        self._cancelled = False

    def cancel(self):
        """
        Cancel the current transition.
        """
        self._cancelled = True

    @property
    def cancelled(self):
        """
        Is the current transition cancelled.
        :return:
        """
        return self._cancelled

    @property
    def previous_state(self):
        """
        The state from which we're transitioning.
        :return:
        """
        return self._previousState

    @property
    def target_state(self):
        """
        Thestate towards we're transitioning.
        :return:
        """
        return self._targetState


class BrowserStateException(Exception):
    pass


transition_set = dict()
link_map = dict()


def register_transition(name, from_state, to_state):
    transition_set[STATE_INDEX[from_state.value] << 16 | STATE_INDEX[to_state.value]] = True

    if not name:
        return

    fromMap = link_map.get(from_state.value)

    if not fromMap:
        fromMap = link_map[from_state.value] = dict()

    fromMap[name] = to_state

register_transition('start_browser', BrowserState.STOPPED, BrowserState.STARTED)
register_transition('pick', BrowserState.STOPPED, BrowserState.BROWSER_NOT_STARTED)
register_transition('inject_code', BrowserState.STARTED, BrowserState.INJECTING_CODE)
register_transition('error', BrowserState.STARTED, BrowserState.ERROR)
register_transition('close_browser', BrowserState.STARTED, BrowserState.STOPPED)
register_transition('pick', BrowserState.STARTED, BrowserState.BROWSER_NOT_READY)
register_transition('close_browser', BrowserState.ERROR, BrowserState.STOPPED)
register_transition('error_processed', BrowserState.ERROR, BrowserState.STARTED)
register_transition('ready', BrowserState.INJECTING_CODE, BrowserState.READY)
register_transition('error', BrowserState.INJECTING_CODE, BrowserState.ERROR)
register_transition('close_browser', BrowserState.INJECTING_CODE, BrowserState.STOPPED)
register_transition('pick', BrowserState.INJECTING_CODE, BrowserState.BROWSER_NOT_READY)
register_transition('highlight', BrowserState.INJECTING_CODE, BrowserState.BROWSER_NOT_READY)
register_transition('pick', BrowserState.READY, BrowserState.PICKING)
register_transition('generate_selector', BrowserState.READY, BrowserState.GENERATING_SELECTOR)
register_transition('error', BrowserState.READY, BrowserState.ERROR)
register_transition('close_browser', BrowserState.READY, BrowserState.STOPPED)
register_transition('generate_selector', BrowserState.PICKING, BrowserState.GENERATING_SELECTOR)
register_transition('cancel_pick', BrowserState.PICKING, BrowserState.READY)
register_transition('error', BrowserState.PICKING, BrowserState.ERROR)
register_transition('close_browser', BrowserState.PICKING, BrowserState.STOPPED)
register_transition('ready', BrowserState.GENERATING_SELECTOR, BrowserState.READY)
register_transition('error', BrowserState.GENERATING_SELECTOR, BrowserState.ERROR)
register_transition('close_browser', BrowserState.GENERATING_SELECTOR, BrowserState.STOPPED)
register_transition('error_processed', BrowserState.BROWSER_NOT_STARTED, BrowserState.STOPPED)
register_transition('error_processed', BrowserState.BROWSER_NOT_READY, BrowserState.STARTED)


class BrowserStateMachine(object):
    def __init__(self, initial_state=None):
        self._transition_listeners = dict()
        self._data_listeners = dict()
        self._initial_state = initial_state or BrowserState.STOPPED

        self._transition_listeners['STOPPED'] = EventListener()
        self._transition_listeners['STARTED'] = EventListener()
        self._transition_listeners['ERROR'] = EventListener()
        self._transition_listeners['INJECTING_CODE'] = EventListener()
        self._transition_listeners['READY'] = EventListener()
        self._transition_listeners['PICKING'] = EventListener()
        self._transition_listeners['GENERATING_SELECTOR'] = EventListener()
        self._transition_listeners['BROWSER_NOT_STARTED'] = EventListener()
        self._transition_listeners['BROWSER_NOT_READY'] = EventListener()
        self._data_listeners['STOPPED'] = EventListener()
        self._data_listeners['STARTED'] = EventListener()
        self._data_listeners['ERROR'] = EventListener()
        self._data_listeners['INJECTING_CODE'] = EventListener()
        self._data_listeners['READY'] = EventListener()
        self._data_listeners['PICKING'] = EventListener()
        self._data_listeners['GENERATING_SELECTOR'] = EventListener()
        self._data_listeners['BROWSER_NOT_STARTED'] = EventListener()
        self._data_listeners['BROWSER_NOT_READY'] = EventListener()
        self._currentState = None
        self._current_change_state_event = None

    @property
    def state(self):
        self._ensure_state_machine_initialized()
        return self._currentState

    def start_browser(self, data=None):
        return self.transition("start_browser", data)

    def pick(self, data=None):
        return self.transition("pick", data)

    def inject_code(self, data=None):
        return self.transition("inject_code", data)

    def error(self, data=None):
        return self.transition("error", data)

    def close_browser(self, data=None):
        return self.transition("close_browser", data)

    def error_processed(self, data=None):
        return self.transition("error_processed", data)

    def ready(self, data=None):
        return self.transition("ready", data)

    def highlight(self, data=None):
        return self.transition("highlight", data)

    def generate_selector(self, data=None):
        return self.transition("generate_selector", data)

    def cancel_pick(self, data=None):
        return self.transition("cancel_pick", data)

    def _ensure_state_machine_initialized(self):
        if not self._currentState:
            self._change_state_impl(self._initial_state, None)

    def changeState(self, targetState, data = None):
        self._ensure_state_machine_initialized()
        return self._change_state_impl(targetState, data)

    def _change_state_impl(self, targetState, data = None):
        if not targetState:
            raise Exception("No target state specified. Can not change the state.")

        # this also ignores the fact that maybe there is no transition
        # into the same state.
        if targetState == self._currentState:
            return targetState

        state_change_event = BrowserStateChangeEvent(self._currentState, targetState, data)

        if self._current_change_state_event:
            raise BrowserStateException(
                "The BrowserStateMachine is already in a changeState (%s -> %s). "
                "Transitioning the state machine (%s -> %s) in `before` events is not supported." % (
                    self._current_change_state_event.previous_state.value,
                    self._current_change_state_event.target_state.value,
                    self._currentState.value,
                    targetState.value
                ))

        if self._currentState and not transition_set.get(STATE_INDEX[self._currentState.value] << 16 | STATE_INDEX[targetState.value]):
            print("No transition exists between %s -> %s." % (self._currentState.value, targetState.value))
            return self._currentState

        self._current_change_state_event = state_change_event

        if state_change_event.previous_state:
            self._transition_listeners[state_change_event.previous_state.value].fire(EventType.BEFORE_LEAVE, state_change_event)

        self._transition_listeners[state_change_event.target_state.value].fire(EventType.BEFORE_ENTER, state_change_event)

        if state_change_event.cancelled:
            return self._currentState

        self._currentState = targetState
        self._current_change_state_event = None

        if state_change_event.previous_state:
            self._transition_listeners[state_change_event.previous_state.value].fire(EventType.AFTER_LEAVE, state_change_event)

        self._transition_listeners[state_change_event.target_state.value].fire(EventType.AFTER_ENTER, state_change_event)

        return self._currentState

    def transition(self, link_name, data=None):
        """
        Transition into another state following a named transition.

        :param str link_name:
        :param object data:
        :return: BrowserState
        """
        self._ensure_state_machine_initialized()

        source_state = link_map.get(self._currentState.value)

        if not source_state:
            return None

        targetState = source_state[link_name]

        if not targetState:
            return None

        return self.changeState(targetState, data)

    def before_enter(self, state, callback):
        """
        Add a transition listener that will fire before entering a new state.
        The transition can still be cancelled at this stage via `ev.cancel()`
        in the callback.

        :param BrowserState state:
        :param Function callback:
        :return:
        """
        return self._transition_listeners[state.value].add_listener(EventType.BEFORE_ENTER, callback)

    def after_enter(self, state, callback):
        """
        Add a transition listener that will fire after the new state is entered.
        The transition can not be cancelled at this stage.
        :param BrowserState state:
        :param callback:
        :return:
        """
        return self._transition_listeners[state.value].add_listener(EventType.AFTER_ENTER, callback)

    def before_leave(self, state, callback):
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

    def on_data(self, state, callback):
        """
        Add a data listener that will be called when data is being pushed for that transition.

        :param BrowserState state:
        :param callback:
        :return:
        """
        return self._data_listeners[state.value].add_listener(EventType.DATA, callback)

    def forward_data(self, new_state, data):
        """
        Changes the state machine into the new state, then sends the data
        ignoring the result. This is so on `onData` calls we can just
        short-circuit the execution using: `return stateMachine.forwardData(..)`

        @param new_state The state to transition into.
        @param data The data to send.
        """
        self.send_data(new_state, data)

        return None

    def send_state_data(self, new_state, data):
        """
        Sends the data into the state machine, to be processed by listeners
        registered with `onData`.
        @param new_state
        @param data The data to send.
        """
        self._ensure_state_machine_initialized()
        self.changeState(new_state, data)

        target_state = self._data_listeners[self._currentState.value].fire(EventType.DATA, data)

        if target_state:
            return self.changeState(target_state, data)

        return self._currentState

    def send_data(self, data):
        """
        Transitions first the state machine into the new state, then it
        will send the data into the state machine.
        @param newState
        @param data
        """
        self._ensure_state_machine_initialized()
        target_state = self._data_listeners[self._currentState.value].fire(EventType.DATA, data)

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
                print e
                if isinstance(e, BrowserStateException):
                    raise e

        return result
