import { convertToSelector } from './convertToSelector'
import { PickState, PickStateMachine } from './PickStateMachine'
import { MouseState, MouseStateMachine } from './MouseStateMachine'

export interface IPickElementResult {
    pickCount: number,
    foundSelector: string,
}

(function() {

const pickState = new PickStateMachine()
const mouseState = new MouseStateMachine()

document.addEventListener("mousedown", mouseDownEventHandler, true);
document.addEventListener("mouseup", mouseUpEventHandler, true);
document.addEventListener("click", mouseClickEventHandler, true);

function halt(ev: Event) {
    ev.preventDefault();
    ev.stopImmediatePropagation();
    ev.stopPropagation();
}

// we need to specify how many items we're going to pick.
pickState.afterEnter(PickState.PICKING, function(ev) {
    pickState.pickCount = ev.data.count
    pickState.selectedElements = []
});

pickState.onData(PickState.PICKING, 'mouse_down', (ev) => {
    pickState.pickCount--;
    pickState.selectedElements.push(ev.data.target)

    if (pickState.pickCount == 0) {
        pickState.foundSelector = convertToSelector(pickState.selectedElements);
        return PickState.SELECTED;
    }
});

mouseState.onData(MouseState.NOT_PRESSED, 'mouse_down', (ev) => {
    ev.consume();
    return MouseState.MOUSE_DOWN;
});

mouseState.onData(MouseState.MOUSE_DOWN, 'mouse_up', (ev) => {
    ev.consume();
    return MouseState.MOUSE_UP;
});

mouseState.onData(MouseState.MOUSE_UP, 'click', (ev) => {
    ev.consume();
    return MouseState.NOT_PRESSED;
});

mouseState.onData(null, (ev) => {
    halt(ev.data);
});


function mouseDownEventHandler(ev: MouseEvent) {
    pickState.sendData('mouse_down', ev);
    mouseState.sendData('mouse_down', ev)
}

function mouseUpEventHandler(ev) {
    mouseState.sendData('mouse_up', ev)
}

function mouseClickEventHandler(ev) {
    mouseState.sendData('click', ev)
}

function germaniumPickElement(elementCount: number) {
    pickState.startPicking({count: elementCount});
    mouseState.startPicking();
}

function germaniumStopPickingElement() {
    pickState.cancelPick();
    mouseState.stopPicking();
}

var cursorX;
var cursorY;
document.addEventListener("mousemove", function (ev) {
    cursorX = ev.pageX;
    cursorY = ev.pageY;
}, true);

document.addEventListener("keydown", function(ev) {
    if (ev.keyCode == 16) {
        pickState.shiftDown = true
    }

    if (ev.keyCode == 17) {
        pickState.ctrlDown = true
    }

    if (pickState.ctrlDown && pickState.shiftDown) {
        pickState.ctrlShift(document.elementFromPoint(cursorX, cursorY))
    }
}, true);

document.addEventListener("keyup", function(ev) {
    if (ev.keyCode == 16) {
        pickState.shiftDown = false
    }

    if (ev.keyCode == 17) {
        pickState.ctrlDown = false
    }
}, true);

/**
 * If we have an element, we return it, and stop the picking.
 * 
 */
function germaniumGetPickedElement() : IPickElementResult {
    if (!pickState.foundSelector) {
        return {
            foundSelector: null,
            pickCount: pickState.pickCount,
        }
    }

    // if we cannot switch to ready, we wait first for the
    // events to be processed, and only then we return the
    // selector
    if (pickState.ready() != PickState.READY) {
        return {
            foundSelector: null,
            pickCount: pickState.pickCount,
        }
    }

    mouseState.stopPicking();

    const result = pickState.foundSelector
    pickState.foundSelector = null
    
    return {
        foundSelector: result,
        pickCount: pickState.pickCount
    }
}

// export global functions on the window object that will be used
// by the selector builder.
window["__germanium_loaded"] = true;

// these are always exported
window["germaniumPickElement"] = germaniumPickElement;
window["germaniumStopPickingElement"] = germaniumStopPickingElement;
window["germaniumGetPickedElement"] = germaniumGetPickedElement;

if (window["__germaniumDebugMode"]) {
    window["germaniumResolveElement"] = convertToSelector;
    window["mouseState"] = mouseState;
    window["pickState"] = pickState;
    window["PickState"] = PickState;
    window["MouseState"] = MouseState;
}

})();
