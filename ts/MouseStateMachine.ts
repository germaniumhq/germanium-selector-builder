function strEnum<T extends string>(o: Array<T>): {[K in T]: K} {
    return o.reduce((res, key) => {
        res[key] = key;
        return res;
    }, Object.create(null));
}

export const MouseState = strEnum([
    'NOT_PRESSED',
    'MOUSE_DOWN',
    'MOUSE_UP',
    'PICKING',
])

const STATE_INDEX = {
    'NOT_PRESSED': 0,
    'MOUSE_DOWN': 1,
    'MOUSE_UP': 2,
    'PICKING': 3,
}

export type MouseState = keyof typeof MouseState

export class MouseStateChangeEvent {
    _cancelled: boolean

    constructor(private _previousState: MouseState,
        private _targetState: MouseState,
        public data: any) {
    }

    get previousState(): MouseState {
        return this._previousState
    }

    get targetState(): MouseState {
        return this._targetState
    }

    cancel() {
        this._cancelled = true
    }
}

export interface DataEvent {
    data: any
    type?: RoutingType
    consume()
}

export type RoutingType = (string | Function)
export type TransitionCallback = (event: MouseStateChangeEvent) => any;
export type DataCallback = ((ev: DataEvent) => MouseState) | ((ev: DataEvent) => void)

export interface CallbackRegistration {
    detach(): void
}

class CompositeCallbackRegistration implements CallbackRegistration {
    constructor(private listeners: Array<CallbackRegistration>) {
    }

    detach() {   
        for (let i = 0; i < this.listeners.length; i++) {
            try {
                this.listeners[i].detach()
            } catch(e) {
                // ignore on purpose
            }
        }
    }
}

function stateCall<T>(state: MouseState, callback: (state: MouseState) => CallbackRegistration) : CallbackRegistration {
    if (state) {
        return callback(state);
    }

    const registrations = []

    for (let k in MouseState) {                
        registrations.push(callback(MouseState[k]));
    }

    return new CompositeCallbackRegistration(registrations);
}

export class MouseStateError extends Error {
}

const transitionSet: { [transitionId: number]: boolean } = {}
const linkMap: {
    [fromStateId: number]: {
        [transitionName: string]: number
    }
} = {}

registerTransition("mouseDown", MouseState.NOT_PRESSED, MouseState.MOUSE_DOWN);
registerTransition("startPicking", MouseState.NOT_PRESSED, MouseState.PICKING);
registerTransition("mouseUp", MouseState.MOUSE_DOWN, MouseState.MOUSE_UP);
registerTransition("click", MouseState.MOUSE_UP, MouseState.NOT_PRESSED);
registerTransition("doubleClick", MouseState.MOUSE_UP, MouseState.NOT_PRESSED);
registerTransition("contextMenu", MouseState.MOUSE_UP, MouseState.NOT_PRESSED);
registerTransition("stopPicking", MouseState.PICKING, MouseState.NOT_PRESSED);

export class MouseStateMachine {

    private currentState: MouseState = null
    private initialState: MouseState

    private currentChangeStateEvent: MouseStateChangeEvent

    private transitionListeners: { [stateId: number]: EventListener<TransitionCallback> } = {}
    private dataListeners: { [stateId: number]: EventListener<DataCallback> } = {}

    constructor(initialState?: MouseState) {
        this.initialState = initialState || MouseState.NOT_PRESSED

this.transitionListeners[MouseState.NOT_PRESSED] = new EventListener<TransitionCallback>()
this.transitionListeners[MouseState.MOUSE_DOWN] = new EventListener<TransitionCallback>()
this.transitionListeners[MouseState.MOUSE_UP] = new EventListener<TransitionCallback>()
this.transitionListeners[MouseState.PICKING] = new EventListener<TransitionCallback>()
this.dataListeners[MouseState.NOT_PRESSED] = new EventListener<DataCallback>()
this.dataListeners[MouseState.MOUSE_DOWN] = new EventListener<DataCallback>()
this.dataListeners[MouseState.MOUSE_UP] = new EventListener<DataCallback>()
this.dataListeners[MouseState.PICKING] = new EventListener<DataCallback>()
    }

    get state() {
        this.ensureStateMachineInitialized()
        return this.currentState
    }

mouseDown(data?: any) : MouseState { return this.transition("mouseDown", data); }
startPicking(data?: any) : MouseState { return this.transition("startPicking", data); }
mouseUp(data?: any) : MouseState { return this.transition("mouseUp", data); }
click(data?: any) : MouseState { return this.transition("click", data); }
doubleClick(data?: any) : MouseState { return this.transition("doubleClick", data); }
contextMenu(data?: any) : MouseState { return this.transition("contextMenu", data); }
stopPicking(data?: any) : MouseState { return this.transition("stopPicking", data); }

    private ensureStateMachineInitialized() {
        if (this.currentState == null) {
            this.changeStateImpl(this.initialState, null);
        }
    }

    changeState(targetState: MouseState, data?: any): MouseState {
        this.ensureStateMachineInitialized()
        return this.changeStateImpl(targetState, data)
    }

    changeStateImpl(targetState: MouseState, data?: any): MouseState {
        if (typeof targetState == 'undefined') {
            throw new Error('No target state specified. Can not change the state.')
        }

        // this also ignores the fact that maybe there is no transition
        // into the same state.
        if (targetState == this.currentState) {
            return targetState
        }

        const stateChangeEvent = new MouseStateChangeEvent(this.currentState, targetState, data)

        if (this.currentChangeStateEvent) {
            throw new MouseStateError(
                `The MouseStateMachine is already in a changeState (${this.currentChangeStateEvent.previousState} -> ${this.currentChangeStateEvent.targetState}). ` +
                `Transitioning the state machine (${this.currentState} -> ${targetState}) in \`before\` events is not supported.`);
        }

        if (this.currentState != null && !transitionSet[STATE_INDEX[this.currentState] << 16 | STATE_INDEX[targetState]]) {
            console.error(`No transition exists between ${this.currentState} -> ${targetState}.`);
            return this.currentState;
        }

        this.currentChangeStateEvent = stateChangeEvent

        if (stateChangeEvent.previousState != null) {
            this.transitionListeners[stateChangeEvent.previousState].fire(EventType.BEFORE_LEAVE, stateChangeEvent)
        }
        this.transitionListeners[stateChangeEvent.targetState].fire(EventType.BEFORE_ENTER, stateChangeEvent)

        if (stateChangeEvent._cancelled) {
            return this.currentState
        }

        this.currentState = targetState
        this.currentChangeStateEvent = null

        if (stateChangeEvent.previousState != null) {
            this.transitionListeners[stateChangeEvent.previousState].fire(EventType.AFTER_LEAVE, stateChangeEvent)
        }
        this.transitionListeners[stateChangeEvent.targetState].fire(EventType.AFTER_ENTER, stateChangeEvent)

        return this.currentState
    }

    transition(linkName: string, data?: any): MouseState {
        this.ensureStateMachineInitialized()

        const sourceState = linkMap[this.currentState]

        if (!sourceState) {
            return null
        }

        const targetState = sourceState[linkName]

        if (typeof targetState == 'undefined') {
            return null
        }

        return this.changeState(targetState, data)
    }

    beforeEnter(state: MouseState, callback: TransitionCallback) {
        return stateCall(state, (state) => {
            return this.transitionListeners[state].addListener(EventType.BEFORE_ENTER, callback);
        });
    }

    afterEnter(state: MouseState, callback: TransitionCallback) {
        return stateCall(state, (state) => {
            return this.transitionListeners[state].addListener(EventType.AFTER_ENTER, callback);
        });
    }

    beforeLeave(state: MouseState, callback: TransitionCallback) {
        return stateCall(state, (state) => {
            return this.transitionListeners[state].addListener(EventType.BEFORE_LEAVE, callback);
        });
    }

    afterLeave(state: MouseState, callback: TransitionCallback) {
        return stateCall(state, (state) => {
            return this.transitionListeners[state].addListener(EventType.AFTER_LEAVE, callback);
        });
    }

    onData(state: MouseState, type: RoutingType, callback: DataCallback);
    onData(state: MouseState, callback: DataCallback);
    onData(state: MouseState) {
        let callback;
        let type;

        if (arguments.length == 2) {
            callback = arguments[1]
            return stateCall(state, (state) => {
                return this.dataListeners[state].addListener('data', callback)
            })
        }

        type = arguments[1]
        callback = arguments[2]

        return stateCall(state, (state) => {
            return this.dataListeners[state].addListener('data', function(ev) {
                if (ev.type == type) {
                    return callback.apply(this, arguments);
                }
            });
        });
    }

    /**
     * Changes the state machine into the new state, then sends the data
     * ignoring the result. This is so on `onData` calls we can just
     * short-circuit the execution using: `return stateMachine.forwardData(..)`
     * 
     * @param newState The state to transition into.
     * @param data The data to send.
     */
    forwardData(newState: MouseState, data: any): MouseState {
        this.sendData(newState, data)
        return null
    }

    /**
     * Sends the data into the state machine, to be processed by listeners
     * registered with `onData`.
     * @param data The data to send.
     */
    sendData(data: any): MouseState;
    /**
     * Transitions first the state machine into the new state, then it
     * will send the data with an attached type into the state machine.
     * @param newState 
     * @param data 
     * @param type
     */
    sendData(newState: MouseState, type: RoutingType, data: any): MouseState;
    /**
     * Sends the data into the state machine, with an attached type.
     * @param type
     * @param data 
     */
    sendData(type: RoutingType, data: any): MouseState;
    /**
     * Transitions first the state machine into the newState, then sends the data
     * to it.
     * @param newState
     * @param data 
     */
    sendData(newState: MouseState, data: any): MouseState;
    /**
     * Ensure the state machine is getting
     * @param newState 
     * @param type
     * @param data 
     */
    sendData(newState: any, type?: any, data?: any) {
        this.ensureStateMachineInitialized()

        if (typeof type == 'undefined') {
            data = newState
            newState = undefined
        }

        if (typeof data == 'undefined') {
            data = type
            
            if (MouseState[newState]) { // our enums
                type = undefined
            } else {
                type = newState
                newState = undefined
            }
        }

        if (typeof newState != 'undefined') {
            this.changeState(newState, data)
        }

        const targetState = this.dataListeners[this.currentState].fire('data', new ListenerEvent(data, type))

        if (targetState != null) {
            return this.changeState(targetState, data)
        }

        return this.currentState
    }
}

function registerTransition(name: string, fromState: MouseState, toState: MouseState): void {
    transitionSet[STATE_INDEX[fromState] << 16 | STATE_INDEX[toState]] = true

    if (!name) {
        return
    }

    let fromMap = linkMap[fromState]
    if (!fromMap) {
        fromMap = linkMap[fromState] = {}
    }

    fromMap[name] = toState
}

const EventType = {
    BEFORE_ENTER: 'before-enter',
    BEFORE_LEAVE: 'before-leave',
    AFTER_LEAVE: 'after-leave',
    AFTER_ENTER: 'after-enter',
}

class EventListener<T extends Function> {
    registered: { [eventName: string]: { [callbackId: number]: Function } } = {}

    addListener(eventName: string, callback: T): CallbackRegistration {
        let eventListeners = this.registered[eventName]

        if (!eventListeners) {
            eventListeners = this.registered[eventName] = {};
        }

        // GUID generation: https://stackoverflow.com/a/2117523/163415
        const callbackId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
            .replace(/[xy]/g, function (c) {
                var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });

        eventListeners[callbackId] = callback

        return {
            detach() {
                delete eventListeners[callbackId]
            }
        }
    }

    fire(eventName: string, ev: any): any {
        if (!this.registered[eventName]) {
            return
        }

        let result        

        const listeners = this.registered[eventName]

        for (var k in listeners) {
            try {
                const callback = listeners[k];

                const potentialResult = callback.call(null, ev)
                if (typeof potentialResult !== 'undefined' && typeof result != 'undefined') {
                    throw new MouseStateError(`Data is already returned.`)
                }

                result = potentialResult

                if (ev && ev.consumed) {
                    break;
                }
            } catch (e) {
                if (e instanceof MouseStateError) {
                    throw e
                }
            }

        }

        return result
    }
}

class ListenerEvent {
    private _consumed : boolean

    constructor(public data: any, public type?: any) {
    }

    consume() {
        this._consumed = true
    }

    get consumed() {
        return this._consumed
    }
}
