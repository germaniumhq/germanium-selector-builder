!function(e){function t(i){if(n[i])return n[i].exports;var r=n[i]={exports:{},id:i,loaded:!1};return e[i].call(r.exports,r,r.exports,t),r.loaded=!0,r.exports}var n={};t.m=e,t.c=n,t.p="",t(0)}([function(e,t,n){e.exports=n(1)},function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var i=n(2);!function(){function e(e){e.preventDefault(),e.stopImmediatePropagation(),e.stopPropagation()}function t(t){return m?e(t):window.__germanium_picking_mode_enabled?(console.log("cancel mousedown event"),window.__germanium_element=i.convertToSelector(t.target),e(t),c=!0,l=!0,m=!0,setTimeout(function(){m=!1},1e3),!1):void 0}function n(t){if(window.__germanium_picking_mode_enabled||c||m)return console.log("cancel mouseup event"),e(t),c=!1,!1}function r(t){if(window.__germanium_picking_mode_enabled||l||m)return console.log("cancel click event"),e(t),l=!1,!1}function o(){console.log("picking element"),window.__germanium_picking_mode_enabled=!0}function s(){console.log("STOPPED picking element"),window.__germanium_picking_mode_enabled=!1}document.addEventListener("mousedown",t,!0),document.addEventListener("mouseup",n,!0),document.addEventListener("click",r,!0),s();var a,u,c=!1,l=!1,m=!1;document.addEventListener("mousemove",function(e){a=e.pageX,u=e.pageY},!0),document.addEventListener("keyup",function(e){(e.ctrlKey&&16==e.keyCode||e.shiftKey&&17==e.keyCode)&&(window.__germanium_element=i.convertToSelector(document.elementFromPoint(a,u)))},!0),window.__germanium_loaded=!0,window.__germanium_picking_mode_enabled=!1,window.germaniumPickElement=o,window.germaniumStopPickingElement=s,window.germaniumResolveElement=i.convertToSelector,console.log("germanium injected")}()},function(e,t,n){"use strict";function i(e){return a(s(e))}function r(e,t,n){return!(void 0===t[n]||(e.exactAttributes[n]=t[n],!o(e)))}function o(e){return 1==p.elementList(e).length}function s(e){var t=d(e),n=new g.GeElement(e.tagName);if("input"==n.tagName){if("button"==t.type||"submit"==t.type){var i=n.clone();if(i.exactAttributes.type=t.type,r(i,t,"value"))return i}if(r(n,t,"name"))return n;if(r(n,t,"placeholder"))return n;if(r(n,t,"type"))return n}var s=f(e);if(s&&!/[\n\r]/.test(s)&&!/  /.test(s)&&(n.exactText=s,o(n)))return n;if(r(n,t,"title"))return n;if(r(n,t,"alt"))return n;if(r(n,t,"aria-label"))return n;if("img"==n.tagName&&r(n,t,"src"))return n;if(t.class){for(var a=t.class.split(/\s+/),u=0;u<a.length;u++)if(n.cssClasses=[a[u]],o(n))return n;if(n.cssClasses=a,o(n))return n}return s&&!n.exactText&&(n.exactText=s,o(n)),n}function a(e){if(!e)return"# unable to build selector";var t=e.getSelector();return u(t)?"XPath("+c(l(t))+")":"Css("+c(l(t))+")"}function u(e){return/^xpath:/.test(e)}function c(e){return m(e)?'"'+e.replace('"','\\"')+'"':'u"'+e.replace('"','\\"')+'"'}function l(e){var t=e.substring(e.indexOf(":")+1);return/^\.\/\//.test(t)?t.substring(1):t}function m(e){return/^[\x00-\x7F]*$/.test(e)}function d(e){for(var t={},n=0;n<e.attributes.length;n++)t[e.attributes.item(n).name]=e.attributes.item(n).value;return t}function f(e){return e.textContent}Object.defineProperty(t,"__esModule",{value:!0});var g=n(3),p=n(4);t.convertToSelector=i},function(e,t){"use strict";function n(e){var t={};for(var n in e)t[n]=e[n];return t}Object.defineProperty(t,"__esModule",{value:!0});var i=function(){function e(e,t){this.cssClasses=[],this.exactAttributes={},this.containsAttributes={},this.tagName=e.toLowerCase(),t&&t.id&&(this.exactAttributes.id=t.id),t&&(this.index=t.index,this.containsText=t.containsText,this.exactText=t.exactText,this.cssClasses=t.cssClasses?t.cssClasses.slice():[],this.exactAttributes=t.exactAttributes?n(t.exactAttributes):{},this.containsAttributes=t.containsAttributes?n(t.containsAttributes):{},this.extraXPath,t.extraXPath)}return e.prototype.clone=function(){return new e(this.tagName,this)},e.prototype.getSelector=function(){var e=".//"+this.tagName;this.containsText&&(e+="[contains(normalize-space(string()), '"+this.containsText+"')]"),this.exactText&&(e+="[string()='"+this.exactText+"']");for(var t=0;t<this.cssClasses.length;t++){e+="[contains(concat(' ', @class, ' '), ' "+this.cssClasses[t]+" ')]"}for(var n in this.exactAttributes)e+="[@"+n+"='"+this.exactAttributes[n]+"']";for(var n in this.containsAttributes)e+="[contains(normalize-space(@"+n+"), '"+this.containsAttributes[n]+"')]";return this.extraXPath&&(e+=this.extraXPath),this.index&&(e="("+e+")["+this.index+"]"),"xpath:"+e},e}();t.GeElement=i},function(e,t){"use strict";function n(e){var t=e.getSelector(),n=o.exec(t);if(!n)return[];if("xpath"==n[1])return i(n[2]);if("css"==n[1])return r(document.querySelectorAll(n[2]));throw new Error("Unsupported algorithm: "+n[1])}function i(e){for(var t,n=document.evaluate(e,document,null,XPathResult.ORDERED_NODE_ITERATOR_TYPE,null),i=[];t=n.iterateNext();)i.push(t);return i}function r(e){for(var t=[],n=0;n<e.length;n+=1)t.push(e[n]);return t}Object.defineProperty(t,"__esModule",{value:!0});var o=/^(.*?)\:(.*)$/;t.elementList=n}]);