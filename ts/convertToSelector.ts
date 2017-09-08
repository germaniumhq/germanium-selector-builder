
import { GeElement } from './Element'
import { elementList } from './Locator'

export function convertToSelector(e: Element) : string {
    return selectorToSeleniumString(constructGermaniumSelector(e))
}

function singleAttributeExactMatch(selector: GeElement,
                                   attributes: { [name: string] : string },
                                   attributeName: string) : boolean {
    if (typeof attributes[attributeName] != "undefined") {
        selector.exactAttributes[attributeName] = attributes[attributeName]

        if (isUnique(selector)) {
            return true;
        }
    }

    return false;
}

function isUnique(selector: GeElement) : boolean {
    return elementList(selector).length == 1
}

/**
 * Consturct a Germanium selector for the given element.
 * @param element The HTML Element to build the selector for
 */
function constructGermaniumSelector(element: Element) : GeElement {
    const attributes : { [name: string] : string } = getAttributes(element);
    
    const selector = new GeElement(element.tagName)

    if (selector.tagName == 'input') {
        if (singleAttributeExactMatch(selector, attributes, 'name')) {
            return selector;
        }

        if (singleAttributeExactMatch(selector, attributes, 'placeholder')) {
            return selector;
        }

        if (singleAttributeExactMatch(selector, attributes, 'type')) {
            return selector;
        }
    }

    const text = getText(element);

    // FIXME: if multiline it shold have a lower priority
    if (text) {
        selector.exactText = text

        if (isUnique(selector)) {
            return selector;
        }
    }

    if (singleAttributeExactMatch(selector, attributes, 'title')) {
        return selector;
    }

    if (singleAttributeExactMatch(selector, attributes, 'alt')) {
        return selector;
    }

    if (singleAttributeExactMatch(selector, attributes, 'aria-label')) {
        return selector;
    }

    if (selector.tagName == 'img') {
        // FIXME: try first /^...(/foo.gif)?...$/ and generate a contains if possible
        if (singleAttributeExactMatch(selector, attributes, 'src')) {
            return selector
        }
    }

    if (attributes['class']) {
        // FIXME: should try each class in turn, then only
        // use all the classes
        selector.cssClasses = attributes['class'].split(/\s+/)

        if (isUnique(selector)) {
            return selector
        }
    }

    return selector;
}

function selectorToSeleniumString(selector: GeElement) : string {
    if (!selector) {
        return "# unable to build selector";
    }

    const strSelector = selector.getSelector()

    if (isXPath(strSelector)) {
        return `XPath(${doubleQuotesText(removePrefix(strSelector))})`
    }

    return `Css(${doubleQuotesText(removePrefix(strSelector))})`
    
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

function removePrefix(value: string) : string {
    return value.substring(value.indexOf(":"))
}

function isPureAscii(value : string) : boolean {
    return /^[\x00-\x7F]*$/.test(value);
} 

function getAttributes(e: Element) : { [name: string ] : string } {
    const result = {}

    for (let i = 0; i < e.attributes.length; i++) {
        result[ e.attributes.item(i).name ] = e.attributes.item(i).value
    }

    return result
}

function getText(e: Element) : string {
    return e.textContent
}
