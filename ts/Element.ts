export interface IExactAttributes { [name: string] : string }

export interface IElementConfig {
    index? : number
    id? : string
    exactText? : string
    containsText? : string
    cssClasses? : Array<string>
    exactAttributes? : IExactAttributes
    containsAttributes? : IExactAttributes
    extraXPath? : string
}

function cloneAttributes(attrs: IExactAttributes) : IExactAttributes {
    const result = {}

    for (let k in attrs) {
        result[k] = attrs[k]
    }

    return result
}

/**
 * An element equivalent from Germanium.
 */
export class GeElement implements IElementConfig {
    public tagName: string;
    public index: number;
    public containsText: string;
    public exactText: string;
    public cssClasses: Array<string> = [];
    public exactAttributes: IExactAttributes = {};
    public containsAttributes: IExactAttributes = {};
    public extraXPath : string;

    constructor(tagName: string, config?: IElementConfig) {
        this.tagName = tagName.toLowerCase();

        if (config && config.id) {
            this.exactAttributes.id = config.id;
        }

        if (config) {
            this.index = config.index
            this.containsText = config.containsText
            this.exactText = config.exactText
            this.cssClasses = config.cssClasses ? config.cssClasses.slice() : []
            this.exactAttributes = config.exactAttributes ? cloneAttributes(config.exactAttributes) : {}
            this.containsAttributes = config.containsAttributes ? cloneAttributes(config.containsAttributes) : {}
            this.extraXPath = config.extraXPath
        }
    }

    public clone() : GeElement {
        return new GeElement(this.tagName, this)
    }

    getSelector() : string {
        return `xpath:${this.asXPath()}`
    }

    asXPath() : string {
        let xpathLocator = `.//${this.tagName}`
        
        if (this.containsText) {
            xpathLocator += `[contains(normalize-space(string()), '${this.containsText}')]`
        }

        if (this.exactText) {
            xpathLocator += `[string()='${this.exactText}']`
        }

        for (let i = 0; i < this.cssClasses.length; i++) {
            let cssClass = this.cssClasses[i]
            xpathLocator += `[contains(concat(' ', @class, ' '), ' ${cssClass} ')]`
        }

        for (let k in this.exactAttributes) {
            xpathLocator += `[@${k}='${this.exactAttributes[k]}']`
        }

        for (let k in this.containsAttributes) {
            xpathLocator += `[contains(normalize-space(@${k}), '${this.containsAttributes[k]}')]`
        }

        if (this.extraXPath) {
            xpathLocator += this.extraXPath
        }

        if (this.index) {
            xpathLocator = `(${xpathLocator})[${this.index}]`
        }

        return xpathLocator;
    }
}
