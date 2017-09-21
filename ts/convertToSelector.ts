
import { GeElement } from './Element'
import { constructGermaniumSelector, removeXPathPrefix } from './constructGermaniumSelector'
import { xpathRelativize } from './xpathRelativize'

export function convertToSelector(elements: Array<Element>) : string {
    let result = constructGermaniumSelector(elements[0])

    if (elements.length == 1) {
        return selectorToSeleniumString(result);
    }

    if (elements.length > 2) {
        return xpathRelativize(
            convertToSelector(elements.slice(1)),
            elementPathFromBody(elements[1]),
            constructGermaniumSelector(elements[0]).asXPath(),
            elementPathFromBody(elements[0]),
        );
    }

    return "XPath(" + doubleQuotesText(xpathRelativize(
        constructGermaniumSelector(elements[1]).asXPath(),
        elementPathFromBody(elements[1]),
        constructGermaniumSelector(elements[0]).asXPath(),
        elementPathFromBody(elements[0]),
    )) + ")";
}

function elementPathFromBody(element: Element) : Array<Element> {
    const result = [element]

    while (element.tagName != 'BODY') {
        element = <Element> element.parentNode
        result.splice(0, 0, element)
    }

    return result
}
 

function selectorToSeleniumString(selector: GeElement) : string {
    if (!selector) {
        return "# unable to build selector";
    }

    const strSelector = selector.getSelector()

    if (isXPath(strSelector)) {
        return `XPath(${doubleQuotesText(removeXPathPrefix(strSelector))})`
    }

    return `Css(${doubleQuotesText(removeXPathPrefix(strSelector))})`
    
}

function isXPath(strSelector: string) {
    return /^xpath:/.test(strSelector)
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
