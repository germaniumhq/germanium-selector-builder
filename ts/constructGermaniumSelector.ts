import { GeElement } from './Element'
import { elementList } from './Locator'
/**
 * Consturct a Germanium selector for the given element.
 * @param element The HTML Element to build the selector for
 */
export function constructGermaniumSelector(element: Element) : GeElement {
    const attributes : { [name: string] : string } = getAttributes(element);
    
    const selector = new GeElement(element.tagName)

    if (selector.tagName == 'input') {
        if (attributes.type == "button" || attributes.type == "submit") {
            const buttonSelector = selector.clone()

            buttonSelector.exactAttributes.type = attributes.type
            if (singleAttributeExactMatch(buttonSelector, attributes, 'value')) {
                return buttonSelector
            }
        }

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

    // if multiline it shold have a lower priority. multiple spaces means
    // that probably there are multiple elements contained.
    if (text && !/[\n\r]/.test(text) && !/  /.test(text)) {
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
        // we try each class in turn, then if not matching we try
        // using all the classes
        const cssClasses =  attributes['class'].split(/\s+/)

        for (let i = 0; i < cssClasses.length; i++) {
            selector.cssClasses = [ cssClasses[i] ]
            if (isUnique(selector)) {
                return selector;
            }
        }

        selector.cssClasses = cssClasses;

        if (isUnique(selector)) {
            return selector
        }
    }

    // if multiline it shold have a lower priority
    if (text && !selector.exactText) {
        selector.exactText = text

        if (isUnique(selector)) {
            return selector;
        }
    }

    return selector;
}

export function removeXPathPrefix(value: string) : string {
    const onlySelector = value.substring(value.indexOf(":") + 1)

    if (/^\.\/\//.test(onlySelector)) {
        return onlySelector.substring(1)
    }

    return onlySelector
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
