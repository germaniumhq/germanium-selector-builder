(function() {

console.log('yay we are in');
window.__germanium_loaded = true;

function mouseDownListener(ev) {
    window.__germanium_element = ev.target;
}

document.addEventListener("mousedown", mouseDownListener, true);

})();
