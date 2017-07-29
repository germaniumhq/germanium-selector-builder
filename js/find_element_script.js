(function() {

console.log('yay we are in');

function mouseDownListener(ev) {
    window.__germanium_element = ev.target;
}

document.addEventListener("mousedown", mouseDownListener, true);

window.__germanium_loaded = true;

})();
