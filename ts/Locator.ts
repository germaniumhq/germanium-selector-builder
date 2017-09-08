
import { GeElement } from './Element'

// A very lame implementation of a locator, that just differentiates
// on the string prefix.

const GE_SELECTOR = /^(.*?)\:(.*)$/;

/**
 * Finds all the elements that match the selector.
 * @param selector The selector to use for the find.
 */
export function elementList(selector: GeElement) : Array<Element> {
    const strSelector = selector.getSelector()
    const m = GE_SELECTOR.exec(strSelector)

    if (!m) {
        return []
    }

    if (m[1] == "xpath") {
        return xpathElementList(m[2])
    } else if (m[1] == "css") {
        return asList(document.querySelectorAll(m[2]))
    }
    
    throw new Error("Unsupported algorithm: " + m[1]);
}

/**
 * Evaluates the xpath and returns a list of all the elements
 * that match the given xpath.
 */
function xpathElementList(xpath: string) : Array<Element> {
    const xpathResult = document.evaluate(xpath,
         document,
         /* ns resolver */ null,
         XPathResult.ORDERED_NODE_ITERATOR_TYPE, 
         /* xpath result */ null)

    const result = []
    
    let item
    while (item = xpathResult.iterateNext()) {
        result.push(item)
    }

    return result
}

/**
 * Converts something that has a length to an array. ie a NodeList.
 * @param items Something that has a length.
 */
function asList<T>(items) : Array<T> {
    const result = []

    for (let i = 0; i < items.length; i += 1) {
        result.push(items[i])
    }

    return result;
}
