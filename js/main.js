!function(t){function e(r){if(n[r])return n[r].exports;var i=n[r]={exports:{},id:r,loaded:!1};return t[r].call(i.exports,i,i.exports,e),i.loaded=!0,i.exports}var n={};e.m=t,e.c=n,e.p="",e(0)}([function(t,e,n){t.exports=n(1)},function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var r=n(2),i=n(7),a=n(8);!function(){function t(t){t.preventDefault(),t.stopImmediatePropagation(),t.stopPropagation()}function e(t){h.sendData("mouse_down",t),f.sendData("mouse_down",t)}function n(t){f.sendData("mouse_up",t)}function o(t){f.sendData("click",t)}function s(t){h.startPicking({count:t}),f.startPicking()}function u(){h.cancelPick(),f.stopPicking()}function c(){if(!h.foundSelector)return null;if(h.ready()!=i.PickState.READY)return null;f.stopPicking();var t=h.foundSelector;return h.foundSelector=null,t}var h=new i.PickStateMachine,f=new a.MouseStateMachine;document.addEventListener("mousedown",e,!0),document.addEventListener("mouseup",n,!0),document.addEventListener("click",o,!0),h.afterEnter(i.PickState.PICKING,function(t){console.log(t,arguments),h.pickCount=t.data.count,h.selectedElements=[]}),h.onData(i.PickState.PICKING,"mouse_down",function(t){if(console.log("pick"+t.data.target),h.pickCount--,h.selectedElements.push(t.data.target),0==h.pickCount)return h.foundSelector=r.convertToSelector(h.selectedElements),i.PickState.SELECTED}),f.onData(a.MouseState.NOT_PRESSED,"mouse_down",function(t){return t.consume(),a.MouseState.MOUSE_DOWN}),f.onData(a.MouseState.MOUSE_DOWN,"mouse_up",function(t){return t.consume(),a.MouseState.MOUSE_UP}),f.onData(a.MouseState.MOUSE_UP,"click",function(t){return t.consume(),a.MouseState.NOT_PRESSED}),f.onData(null,function(e){console.log("mouse state is: "+f.state),t(e.data)});var l,S;document.addEventListener("mousemove",function(t){l=t.pageX,S=t.pageY},!0),document.addEventListener("keydown",function(t){16==t.keyCode&&(h.shiftDown=!0),17==t.keyCode&&(h.ctrlDown=!0),h.ctrlDown&&h.shiftDown&&h.ctrlShift(document.elementFromPoint(l,S))},!0),document.addEventListener("keyup",function(t){16==t.keyCode&&(h.shiftDown=!1),17==t.keyCode&&(h.ctrlDown=!1)},!0),window.__germanium_loaded=!0,window.germaniumPickElement=s,window.germaniumStopPickingElement=u,window.germaniumGetPickedElement=c,window.__germaniumDebugMode&&(window.germaniumResolveElement=r.convertToSelector,window.mouseState=f,window.pickState=h,window.PickState=i.PickState,window.MouseState=a.MouseState)}()},function(t,e,n){"use strict";function r(t){var e=h.constructGermaniumSelector(t[0]);return 1==t.length?a(e):t.length>2?f.xpathRelativize(h.constructGermaniumSelector(t[0]).asXPath(),i(t[0]),r(t.slice(1)),i(t[1])):f.xpathRelativize(h.constructGermaniumSelector(t[0]).asXPath(),i(t[0]),h.constructGermaniumSelector(t[1]).asXPath(),i(t[1]))}function i(t){for(var e=[t];"BODY"!=t.tagName;)t=t.parentNode,e.splice(0,0,t);return e}function a(t){if(!t)return"# unable to build selector";var e=t.getSelector();return o(e)?"XPath("+s(u(e))+")":"Css("+s(u(e))+")"}function o(t){return/^xpath:/.test(t)}function s(t){return c(t)?'"'+t.replace('"','\\"')+'"':'u"'+t.replace('"','\\"')+'"'}function u(t){var e=t.substring(t.indexOf(":")+1);return/^\.\/\//.test(e)?e.substring(1):e}function c(t){return/^[\x00-\x7F]*$/.test(t)}Object.defineProperty(e,"__esModule",{value:!0});var h=n(3),f=n(6);e.convertToSelector=r},function(t,e,n){"use strict";function r(t){var e=o(t),n=new u.GeElement(t.tagName);if("input"==n.tagName){if("button"==e.type||"submit"==e.type){var r=n.clone();if(r.exactAttributes.type=e.type,i(r,e,"value"))return r}if(i(n,e,"name"))return n;if(i(n,e,"placeholder"))return n;if(i(n,e,"type"))return n}var c=s(t);if(c&&!/[\n\r]/.test(c)&&!/  /.test(c)&&(n.exactText=c,a(n)))return n;if(i(n,e,"title"))return n;if(i(n,e,"alt"))return n;if(i(n,e,"aria-label"))return n;if("img"==n.tagName&&i(n,e,"src"))return n;if(e.class){for(var h=e.class.split(/\s+/),f=0;f<h.length;f++)if(n.cssClasses=[h[f]],a(n))return n;if(n.cssClasses=h,a(n))return n}return c&&!n.exactText&&(n.exactText=c,a(n)),n}function i(t,e,n){return!(void 0===e[n]||(t.exactAttributes[n]=e[n],!a(t)))}function a(t){return 1==c.elementList(t).length}function o(t){for(var e={},n=0;n<t.attributes.length;n++)e[t.attributes.item(n).name]=t.attributes.item(n).value;return e}function s(t){return t.textContent}Object.defineProperty(e,"__esModule",{value:!0});var u=n(4),c=n(5);e.constructGermaniumSelector=r},function(t,e){"use strict";function n(t){var e={};for(var n in t)e[n]=t[n];return e}Object.defineProperty(e,"__esModule",{value:!0});var r=function(){function t(t,e){this.cssClasses=[],this.exactAttributes={},this.containsAttributes={},this.tagName=t.toLowerCase(),e&&e.id&&(this.exactAttributes.id=e.id),e&&(this.index=e.index,this.containsText=e.containsText,this.exactText=e.exactText,this.cssClasses=e.cssClasses?e.cssClasses.slice():[],this.exactAttributes=e.exactAttributes?n(e.exactAttributes):{},this.containsAttributes=e.containsAttributes?n(e.containsAttributes):{},this.extraXPath,e.extraXPath)}return t.prototype.clone=function(){return new t(this.tagName,this)},t.prototype.getSelector=function(){return"xpath:"+this.asXPath()},t.prototype.asXPath=function(){var t=".//"+this.tagName;this.containsText&&(t+="[contains(normalize-space(string()), '"+this.containsText+"')]"),this.exactText&&(t+="[string()='"+this.exactText+"']");for(var e=0;e<this.cssClasses.length;e++){t+="[contains(concat(' ', @class, ' '), ' "+this.cssClasses[e]+" ')]"}for(var n in this.exactAttributes)t+="[@"+n+"='"+this.exactAttributes[n]+"']";for(var n in this.containsAttributes)t+="[contains(normalize-space(@"+n+"), '"+this.containsAttributes[n]+"')]";return this.extraXPath&&(t+=this.extraXPath),this.index&&(t="("+t+")["+this.index+"]"),t},t}();e.GeElement=r},function(t,e){"use strict";function n(t){var e=t.getSelector(),n=a.exec(e);if(!n)return[];if("xpath"==n[1])return r(n[2]);if("css"==n[1])return i(document.querySelectorAll(n[2]));throw new Error("Unsupported algorithm: "+n[1])}function r(t){for(var e,n=document.evaluate(t,document,null,XPathResult.ORDERED_NODE_ITERATOR_TYPE,null),r=[];e=n.iterateNext();)r.push(e);return r}function i(t){for(var e=[],n=0;n<t.length;n+=1)e.push(t[n]);return e}Object.defineProperty(e,"__esModule",{value:!0});var a=/^(.*?)\:(.*)$/;e.elementList=n},function(t,e,n){"use strict";function r(t,e,n,r){for(var a=e[0],o=0;o<e.length&&o<r.length&&e[o]==r[o];)a=e[o],o++;return e.length-o>3?t+"/ancestor::"+i.constructGermaniumSelector(a)+n:t+"/.."+n}Object.defineProperty(e,"__esModule",{value:!0});var i=n(3);e.xpathRelativize=r},function(t,e){"use strict";function n(t,n){if(t)return n(t);var r=[];for(var i in e.PickState)r.push(n(e.PickState[i]));return new s(r)}function r(t,e,n){if(c[a[e]<<16|a[n]]=!0,t){var r=h[e];r||(r=h[e]={}),r[t]=n}}var i=this&&this.__extends||function(){var t=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var n in e)e.hasOwnProperty(n)&&(t[n]=e[n])};return function(e,n){function r(){this.constructor=e}t(e,n),e.prototype=null===n?Object.create(n):(r.prototype=n.prototype,new r)}}();Object.defineProperty(e,"__esModule",{value:!0}),e.PickState=function(t){return t.reduce(function(t,e){return t[e]=e,t},Object.create(null))}(["READY","PICKING","MOUSE_DOWN","MOUSE_UP","CLICK","SELECTED"]);var a={READY:0,PICKING:1,MOUSE_DOWN:2,MOUSE_UP:3,CLICK:4,SELECTED:5},o=function(){function t(t,e,n){this._previousState=t,this._targetState=e,this.data=n}return Object.defineProperty(t.prototype,"previousState",{get:function(){return this._previousState},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"targetState",{get:function(){return this._targetState},enumerable:!0,configurable:!0}),t.prototype.cancel=function(){this._cancelled=!0},t}();e.PickStateChangeEvent=o;var s=function(){function t(t){this.listeners=t}return t.prototype.detach=function(){for(var t=0;t<this.listeners.length;t++)try{this.listeners[t].detach()}catch(t){}},t}(),u=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return i(e,t),e}(Error);e.PickStateError=u;var c={},h={};r("startPicking",e.PickState.READY,e.PickState.PICKING),r("ctrlShift",e.PickState.READY,e.PickState.SELECTED),r("cancelPick",e.PickState.PICKING,e.PickState.READY),r("selected",e.PickState.PICKING,e.PickState.SELECTED),r("ready",e.PickState.SELECTED,e.PickState.READY);var f=function(){function t(t){this.currentState=null,this.transitionListeners={},this.dataListeners={},this.initialState=t||e.PickState.READY,this.transitionListeners[e.PickState.READY]=new S,this.transitionListeners[e.PickState.PICKING]=new S,this.transitionListeners[e.PickState.MOUSE_DOWN]=new S,this.transitionListeners[e.PickState.MOUSE_UP]=new S,this.transitionListeners[e.PickState.CLICK]=new S,this.transitionListeners[e.PickState.SELECTED]=new S,this.dataListeners[e.PickState.READY]=new S,this.dataListeners[e.PickState.PICKING]=new S,this.dataListeners[e.PickState.MOUSE_DOWN]=new S,this.dataListeners[e.PickState.MOUSE_UP]=new S,this.dataListeners[e.PickState.CLICK]=new S,this.dataListeners[e.PickState.SELECTED]=new S}return Object.defineProperty(t.prototype,"state",{get:function(){return this.ensureStateMachineInitialized(),this.currentState},enumerable:!0,configurable:!0}),t.prototype.startPicking=function(t){return this.transition("startPicking",t)},t.prototype.ctrlShift=function(t){return this.transition("ctrlShift",t)},t.prototype.cancelPick=function(t){return this.transition("cancelPick",t)},t.prototype.selected=function(t){return this.transition("selected",t)},t.prototype.ready=function(t){return this.transition("ready",t)},t.prototype.ensureStateMachineInitialized=function(){null==this.currentState&&this.changeStateImpl(this.initialState,null)},t.prototype.changeState=function(t,e){return this.ensureStateMachineInitialized(),this.changeStateImpl(t,e)},t.prototype.changeStateImpl=function(t,e){if(void 0===t)throw new Error("No target state specified. Can not change the state.");if(t==this.currentState)return t;var n=new o(this.currentState,t,e);if(this.currentChangeStateEvent)throw new u("The PickStateMachine is already in a changeState ("+this.currentChangeStateEvent.previousState+" -> "+this.currentChangeStateEvent.targetState+"). Transitioning the state machine ("+this.currentState+" -> "+t+") in `before` events is not supported.");return null==this.currentState||c[a[this.currentState]<<16|a[t]]?(this.currentChangeStateEvent=n,null!=n.previousState&&this.transitionListeners[n.previousState].fire(l.BEFORE_LEAVE,n),this.transitionListeners[n.targetState].fire(l.BEFORE_ENTER,n),n._cancelled?this.currentState:(this.currentState=t,this.currentChangeStateEvent=null,null!=n.previousState&&this.transitionListeners[n.previousState].fire(l.AFTER_LEAVE,n),this.transitionListeners[n.targetState].fire(l.AFTER_ENTER,n),this.currentState)):(console.error("No transition exists between "+this.currentState+" -> "+t+"."),this.currentState)},t.prototype.transition=function(t,e){this.ensureStateMachineInitialized();var n=h[this.currentState];if(!n)return null;var r=n[t];return void 0===r?null:this.changeState(r,e)},t.prototype.beforeEnter=function(t,e){var r=this;return n(t,function(t){return r.transitionListeners[t].addListener(l.BEFORE_ENTER,e)})},t.prototype.afterEnter=function(t,e){var r=this;return n(t,function(t){return r.transitionListeners[t].addListener(l.AFTER_ENTER,e)})},t.prototype.beforeLeave=function(t,e){var r=this;return n(t,function(t){return r.transitionListeners[t].addListener(l.BEFORE_LEAVE,e)})},t.prototype.afterLeave=function(t,e){var r=this;return n(t,function(t){return r.transitionListeners[t].addListener(l.AFTER_LEAVE,e)})},t.prototype.onData=function(t){var e,r,i=this;return 2==arguments.length?(e=arguments[1],n(t,function(t){return i.dataListeners[t].addListener("data",e)})):(r=arguments[1],e=arguments[2],n(t,function(t){return i.dataListeners[t].addListener("data",function(t){if(t.type==r)return e.apply(this,arguments)})}))},t.prototype.forwardData=function(t,e){return this.sendData(t,e),null},t.prototype.sendData=function(t,n,r){this.ensureStateMachineInitialized(),void 0===n&&(r=t,t=void 0),void 0===r&&(r=n,e.PickState[t]?n=void 0:(n=t,t=void 0)),void 0!==t&&this.changeState(t,r);var i=this.dataListeners[this.currentState].fire("data",new d(r,n));return null!=i?this.changeState(i,r):this.currentState},t}();e.PickStateMachine=f;var l={BEFORE_ENTER:"before-enter",BEFORE_LEAVE:"before-leave",AFTER_LEAVE:"after-leave",AFTER_ENTER:"after-enter"},S=function(){function t(){this.registered={}}return t.prototype.addListener=function(t,e){var n=this.registered[t];n||(n=this.registered[t]={});var r="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(t){var e=16*Math.random()|0;return("x"==t?e:3&e|8).toString(16)});return n[r]=e,{detach:function(){delete n[r]}}},t.prototype.fire=function(t,e){if(this.registered[t]){var n,r=this.registered[t];for(var i in r)try{var a=r[i],o=a.call(null,e);if(void 0!==o&&void 0!==n)throw new u("Data is already returned.");if(n=o,e&&e.consumed)break}catch(t){if(t instanceof u)throw t}return n}},t}(),d=function(){function t(t,e){this.data=t,this.type=e}return t.prototype.consume=function(){this._consumed=!0},Object.defineProperty(t.prototype,"consumed",{get:function(){return this._consumed},enumerable:!0,configurable:!0}),t}()},function(t,e){"use strict";function n(t,n){if(t)return n(t);var r=[];for(var i in e.MouseState)r.push(n(e.MouseState[i]));return new s(r)}function r(t,e,n){if(c[a[e]<<16|a[n]]=!0,t){var r=h[e];r||(r=h[e]={}),r[t]=n}}var i=this&&this.__extends||function(){var t=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var n in e)e.hasOwnProperty(n)&&(t[n]=e[n])};return function(e,n){function r(){this.constructor=e}t(e,n),e.prototype=null===n?Object.create(n):(r.prototype=n.prototype,new r)}}();Object.defineProperty(e,"__esModule",{value:!0}),e.MouseState=function(t){return t.reduce(function(t,e){return t[e]=e,t},Object.create(null))}(["NOT_PRESSED","MOUSE_DOWN","MOUSE_UP","PICKING"]);var a={NOT_PRESSED:0,MOUSE_DOWN:1,MOUSE_UP:2,PICKING:3},o=function(){function t(t,e,n){this._previousState=t,this._targetState=e,this.data=n}return Object.defineProperty(t.prototype,"previousState",{get:function(){return this._previousState},enumerable:!0,configurable:!0}),Object.defineProperty(t.prototype,"targetState",{get:function(){return this._targetState},enumerable:!0,configurable:!0}),t.prototype.cancel=function(){this._cancelled=!0},t}();e.MouseStateChangeEvent=o;var s=function(){function t(t){this.listeners=t}return t.prototype.detach=function(){for(var t=0;t<this.listeners.length;t++)try{this.listeners[t].detach()}catch(t){}},t}(),u=function(t){function e(){return null!==t&&t.apply(this,arguments)||this}return i(e,t),e}(Error);e.MouseStateError=u;var c={},h={};r("mouseDown",e.MouseState.NOT_PRESSED,e.MouseState.MOUSE_DOWN),r("startPicking",e.MouseState.NOT_PRESSED,e.MouseState.PICKING),r("mouseUp",e.MouseState.MOUSE_DOWN,e.MouseState.MOUSE_UP),r("click",e.MouseState.MOUSE_UP,e.MouseState.NOT_PRESSED),r("doubleClick",e.MouseState.MOUSE_UP,e.MouseState.NOT_PRESSED),r("contextMenu",e.MouseState.MOUSE_UP,e.MouseState.NOT_PRESSED),r("stopPicking",e.MouseState.PICKING,e.MouseState.NOT_PRESSED);var f=function(){function t(t){this.currentState=null,this.transitionListeners={},this.dataListeners={},this.initialState=t||e.MouseState.NOT_PRESSED,this.transitionListeners[e.MouseState.NOT_PRESSED]=new S,this.transitionListeners[e.MouseState.MOUSE_DOWN]=new S,this.transitionListeners[e.MouseState.MOUSE_UP]=new S,this.transitionListeners[e.MouseState.PICKING]=new S,this.dataListeners[e.MouseState.NOT_PRESSED]=new S,this.dataListeners[e.MouseState.MOUSE_DOWN]=new S,this.dataListeners[e.MouseState.MOUSE_UP]=new S,this.dataListeners[e.MouseState.PICKING]=new S}return Object.defineProperty(t.prototype,"state",{get:function(){return this.ensureStateMachineInitialized(),this.currentState},enumerable:!0,configurable:!0}),t.prototype.mouseDown=function(t){return this.transition("mouseDown",t)},t.prototype.startPicking=function(t){return this.transition("startPicking",t)},t.prototype.mouseUp=function(t){return this.transition("mouseUp",t)},t.prototype.click=function(t){return this.transition("click",t)},t.prototype.doubleClick=function(t){return this.transition("doubleClick",t)},t.prototype.contextMenu=function(t){return this.transition("contextMenu",t)},t.prototype.stopPicking=function(t){return this.transition("stopPicking",t)},t.prototype.ensureStateMachineInitialized=function(){null==this.currentState&&this.changeStateImpl(this.initialState,null)},t.prototype.changeState=function(t,e){return this.ensureStateMachineInitialized(),this.changeStateImpl(t,e)},t.prototype.changeStateImpl=function(t,e){if(void 0===t)throw new Error("No target state specified. Can not change the state.");if(t==this.currentState)return t;var n=new o(this.currentState,t,e);if(this.currentChangeStateEvent)throw new u("The MouseStateMachine is already in a changeState ("+this.currentChangeStateEvent.previousState+" -> "+this.currentChangeStateEvent.targetState+"). Transitioning the state machine ("+this.currentState+" -> "+t+") in `before` events is not supported.");return null==this.currentState||c[a[this.currentState]<<16|a[t]]?(this.currentChangeStateEvent=n,null!=n.previousState&&this.transitionListeners[n.previousState].fire(l.BEFORE_LEAVE,n),this.transitionListeners[n.targetState].fire(l.BEFORE_ENTER,n),n._cancelled?this.currentState:(this.currentState=t,this.currentChangeStateEvent=null,null!=n.previousState&&this.transitionListeners[n.previousState].fire(l.AFTER_LEAVE,n),this.transitionListeners[n.targetState].fire(l.AFTER_ENTER,n),this.currentState)):(console.error("No transition exists between "+this.currentState+" -> "+t+"."),this.currentState)},t.prototype.transition=function(t,e){this.ensureStateMachineInitialized();var n=h[this.currentState];if(!n)return null;var r=n[t];return void 0===r?null:this.changeState(r,e)},t.prototype.beforeEnter=function(t,e){var r=this;return n(t,function(t){return r.transitionListeners[t].addListener(l.BEFORE_ENTER,e)})},t.prototype.afterEnter=function(t,e){var r=this;return n(t,function(t){return r.transitionListeners[t].addListener(l.AFTER_ENTER,e)})},t.prototype.beforeLeave=function(t,e){var r=this;return n(t,function(t){return r.transitionListeners[t].addListener(l.BEFORE_LEAVE,e)})},t.prototype.afterLeave=function(t,e){var r=this;return n(t,function(t){return r.transitionListeners[t].addListener(l.AFTER_LEAVE,e)})},t.prototype.onData=function(t){var e,r,i=this;return 2==arguments.length?(e=arguments[1],n(t,function(t){return i.dataListeners[t].addListener("data",e)})):(r=arguments[1],e=arguments[2],n(t,function(t){return i.dataListeners[t].addListener("data",function(t){if(t.type==r)return e.apply(this,arguments)})}))},t.prototype.forwardData=function(t,e){return this.sendData(t,e),null},t.prototype.sendData=function(t,n,r){this.ensureStateMachineInitialized(),void 0===n&&(r=t,t=void 0),void 0===r&&(r=n,e.MouseState[t]?n=void 0:(n=t,t=void 0)),void 0!==t&&this.changeState(t,r);var i=this.dataListeners[this.currentState].fire("data",new d(r,n));return null!=i?this.changeState(i,r):this.currentState},t}();e.MouseStateMachine=f;var l={BEFORE_ENTER:"before-enter",BEFORE_LEAVE:"before-leave",AFTER_LEAVE:"after-leave",AFTER_ENTER:"after-enter"},S=function(){function t(){this.registered={}}return t.prototype.addListener=function(t,e){var n=this.registered[t];n||(n=this.registered[t]={});var r="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(t){var e=16*Math.random()|0;return("x"==t?e:3&e|8).toString(16)});return n[r]=e,{detach:function(){delete n[r]}}},t.prototype.fire=function(t,e){if(this.registered[t]){var n,r=this.registered[t];for(var i in r)try{var a=r[i],o=a.call(null,e);if(void 0!==o&&void 0!==n)throw new u("Data is already returned.");if(n=o,e&&e.consumed)break}catch(t){if(t instanceof u)throw t}return n}},t}(),d=function(){function t(t,e){this.data=t,this.type=e}return t.prototype.consume=function(){this._consumed=!0},Object.defineProperty(t.prototype,"consumed",{get:function(){return this._consumed},enumerable:!0,configurable:!0}),t}()}]);