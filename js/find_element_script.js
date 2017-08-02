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

document.addEventListener("keyup", function(ev) {
    if (ev.ctrlKey && ev.keyCode == 16 || ev.shiftKey && ev.keyCode == 17) {
        alert('let the capture begin');
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
