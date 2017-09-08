(function() {

document.addEventListener("mousedown", mouseDownEventHandler, true);
document.addEventListener("mouseup", mouseUpEventHandler, true);
document.addEventListener("click", mouseClickEventHandler, true);

germaniumStopPickingElement();

var mouseDown = false;
var mouseDownCancelled = false;
var captureTimerRunning = false;

function halt(ev) {
    ev.preventDefault();
    ev.stopImmediatePropagation();
    ev.stopPropagation();
}

function mouseDownEventHandler(ev) {
    if (captureTimerRunning) {
        return halt(ev);
    }

    if (window['__germanium_picking_mode_enabled']) {
        console.log('cancel mousedown event');
        window["__germanium_element"] = convertToSelector(ev.target);
        halt(ev);
        mouseDown = true;
        mouseDownCancelled = true;
        captureTimerRunning = true;

        setTimeout(function() {
            captureTimerRunning = false;
        }, 1000);

        return false;
    }

}

function mouseUpEventHandler(ev) {
    if (window['__germanium_picking_mode_enabled'] || mouseDown || captureTimerRunning) {
        console.log('cancel mouseup event');
        halt(ev);
        mouseDown = false;

        return false;
    }
}

function mouseClickEventHandler(ev) {
    if (window['__germanium_picking_mode_enabled'] || mouseDownCancelled || captureTimerRunning) {
        console.log('cancel click event');
        halt(ev);
        mouseDownCancelled = false;

        return false;
    }
}

function germaniumPickElement() {
    console.log('picking element');
    window['__germanium_picking_mode_enabled'] = true;
}

function germaniumStopPickingElement() {
    console.log('STOPPED picking element');
    window['__germanium_picking_mode_enabled'] = false;
}

var cursorX;
var cursorY;
document.addEventListener("mousemove", function (ev) {
    cursorX = ev.pageX;
    cursorY = ev.pageY;
}, true);

document.addEventListener("keyup", function(ev) {
    if (ev.ctrlKey && ev.keyCode == 16 || ev.shiftKey && ev.keyCode == 17) {
        window["__germanium_element"] = convertToSelector(document.elementFromPoint(cursorX, cursorY));
    }
}, true);

function convertToSelector(element: Element) : string {
    return "//" + element.tagName
}

// export global functions on the window object that will be used
// by the selector builder.
window["__germanium_loaded"] = true;
window['__germanium_picking_mode_enabled'] = false;
window["germaniumPickElement"] = germaniumPickElement;
window["germaniumStopPickingElement"] = germaniumStopPickingElement;

console.log('germanium injected');

})();
