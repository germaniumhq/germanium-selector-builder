(function() {

function germaniumPickElement() {
    window.__germanium_picking_mode_enabled = true;
    document.addEventListener("mousedown", mouseDownListener, true);
}
window.germaniumPickElement = germaniumPickElement;

function germaniumStopPickingElement() {
    window.__germanium_picking_mode_enabled = false;
    document.removeEventListener("mousedown", mouseDownListener, true);
}
window.germaniumStopPickingElement = germaniumStopPickingElement;

var cursorX;
var cursorY;
document.addEventListener("mousemove", function (ev) {
    cursorX = ev.pageX;
    cursorY = ev.pageY;
}, true);

document.addEventListener("keyup", function(ev) {
    if (ev.ctrlKey && ev.keyCode == 16 || ev.shiftKey && ev.keyCode == 17) {
        window.__germanium_element = document.elementFromPoint(cursorX, cursorY);
    }
}, true);

function mouseDownListener(ev) {
    window.__germanium_element = ev.target;

    ev.preventDefault();
    ev.stopImmediatePropagation();
    ev.stopPropagation();
}


window.__germanium_loaded = true;

})();
