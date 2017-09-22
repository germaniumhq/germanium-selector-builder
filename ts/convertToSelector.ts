
import { GeElement } from './Element'
import { constructGermaniumSelector, removeXPathPrefix } from './constructGermaniumSelector'
import { xpathRelativize } from './xpathRelativize'

export function convertToSelector(elements: Array<Element>) : string {
    if (elements.length == 1) {
        return selectorToSeleniumString( constructGermaniumSelector(elements[0]).getSelector());    
    }

    return selectorToSeleniumString(constructXPathSelector(elements));
}

/**
 * Builds an XPath for the first element, taking the parents into
 * account.
 * 
 * @param elements An array of elements to construct the XPath for. The
 *                 first element is the target, and the rest are the
 *                 references.
 */
function constructXPathSelector(elements: Array<Element>) : string {
    let result = constructGermaniumSelector(elements[0])
    
    if (elements.length == 1) {
        return result && result.asXPath();
    }
    
    if (elements.length > 2) {
        return xpathRelativize(
            constructXPathSelector(elements.slice(1)),
            elementPathFromBody(elements[1]),
            constructGermaniumSelector(elements[0]).asXPath(),
            elementPathFromBody(elements[0]),
        );
    }

    return xpathRelativize(
        constructGermaniumSelector(elements[1]).asXPath(),
        elementPathFromBody(elements[1]),
        constructGermaniumSelector(elements[0]).asXPath(),
        elementPathFromBody(elements[0]),
    );
}

function elementPathFromBody(element: Element) : Array<Element> {
    const result = [element]

    while (element.tagName != 'BODY') {
        element = <Element> element.parentNode
        result.splice(0, 0, element)
    }

    return result
}
 

function selectorToSeleniumString(strSelector: string) : string {
    if (!strSelector) {
        return "# unable to build selector";
    }

    if (/^\w+\(/.test(strSelector)) {
        return strSelector;
    }

    if (isXPath(strSelector)) {
        return `XPath(${doubleQuotesText(removeXPathPrefix(strSelector))})`
    }

    return `Css(${doubleQuotesText(removeXPathPrefix(strSelector))})`
    
}

function isXPath(strSelector: string) {
    return /^xpath:/.test(strSelector) || /^\/\//.test(strSelector)
}

function doubleQuotesText(value: string) {
    if (!isPureAscii(value)) {
        return 'u"' + value.replace('"', '\\"') + '"'
    }

    return '"' + value.replace('"', '\\"') + '"'    
}

function isPureAscii(value : string) : boolean {
    return /^[\x00-\x7F]*$/.test(value);
} 
