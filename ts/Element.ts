export interface IExactAttributes { [name: string] : string }

export interface IElementConfig {
    index? : number
    id? : string
    exactText? : string
    containsText? : string
    cssClasses? : string | Array<string>
    exactAttributes? : IExactAttributes
    containsAttributes? : IExactAttributes
    extraXPath? : string
}

/**
 * An element equivalent from Germanium.
 */
export class GeElement {
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
    }

    getSelector() : string {
        let xpathLocator = `.//${this.tagName}`

        if (this.containsText) {
            xpathLocator += `[contains(normalize-space(string()), '${this.containsText}')]`
        }

        if (this.exactText) {
            xpathLocator += `[string() = '${this.exactText}']`
        }

        for (let i = 0; i < this.cssClasses.length; i++) {
            let cssClass = this.cssClasses[i]
            xpathLocator += `[contains(concat(' ', @class, ' '), ' ${cssClass} ')]`
        }

        for (let k in this.exactAttributes) {
            xpathLocator += `[@${k} = '${this.exactAttributes[k]}']`
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

        return `xpath:${xpathLocator}`
    }
}
