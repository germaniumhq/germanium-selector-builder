import { 
    constructGermaniumSelector,
    removeXPathPrefix,
    removeXPathSearchPrefix,
} from './constructGermaniumSelector';

/**
 * Computes a path from the parent to the target node.
 * @param parentReferenceXPath The parent node XPath (The node used as a reference).
 * @param parentAbsoluteXPath The parent node absolute path starting from the /body/ node.
 * @param targetNodeXPath  The target node XPath (the node that should be found).
 * @param targetAbsoluteXPath The target node absolute path starting from the /body/ node.
 */
export function xpathRelativize(parentReferenceXPath: string,
                                parentAbsoluteXPath: Array<Element>,
                                targetNodeXPath: string,
                                targetAbsoluteXPath: Array<Element>) : string {    
    let commonParent = parentAbsoluteXPath[0]
    let index = 0

    // we find the common parent.
    while (index < parentAbsoluteXPath.length && index < targetAbsoluteXPath.length) {
        if (parentAbsoluteXPath[index] != targetAbsoluteXPath[index]) {
            break
        }

        commonParent = parentAbsoluteXPath[index]
        index++
    }

    // if the targetNode is actually the parentNode, we return the parent XPath
    if (index == parentAbsoluteXPath.length && index == targetAbsoluteXPath.length) {
        return parentReferenceXPath;
    }

    // we exit from the reference node until the common parent.
    // if we have more than 3 levels of exiting, we build a selector for the
    // common parent.
    if (parentAbsoluteXPath.length - index > 3) {
        return removeXPathPrefix(parentReferenceXPath) + 
                 "/ancestor::" + 
                 removeXPathSearchPrefix(constructGermaniumSelector(commonParent, { excludeTextSearch: true }).asXPath()) + 
                 removeXPathPrefix(targetNodeXPath)
    }

    let prefix = ""
    for (let i = 0; i < parentAbsoluteXPath.length - index; i++) {
        prefix += '/..'
    } 

    return removeXPathPrefix(parentReferenceXPath) + prefix + removeXPathPrefix(targetNodeXPath)
}
