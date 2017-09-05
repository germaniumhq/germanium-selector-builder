from germanium.static import *
import re

from germaniumsb.CodeMode import CodeMode


def build_selector(element, code_mode):
    selector = construct_germanium_selector(element, code_mode)

    if code_mode == CodeMode.Germanium:
        return selector_to_string(selector)

    return selector_to_selenium_string(selector)


def single_attribute_exact_match(selector, attributes, attribute_name):
    """
    Checks if there is an attribute defined that matches exactly
    a single element. This will mutate the selector.
    :param selector:
    :param attributes:
    :param attribute_name:
    :return:
    """
    if attribute_name in attributes and attributes[attribute_name]:
        if not selector.exact_attributes:
            selector.exact_attributes = {}
        selector.exact_attributes[attribute_name] = attributes[attribute_name]

        if is_unique(selector):
            return True

    return False


def construct_germanium_selector(element, code_mode):
    attributes = get_attributes(element)

    if is_input_text(element) and code_mode == CodeMode.Germanium:
        selector = InputText()

        if single_attribute_exact_match(selector, attributes, 'name'):
            return selector

        if single_attribute_exact_match(selector, attributes, 'placeholder'):
            return selector

        if 'class' in attributes and attributes['class']:
            selector.css_classes = attributes['class'].split()

        if is_unique(selector):
            return selector

    selector = Element(tag_name=element.tag_name)

    if element.tag_name == 'input':
        if single_attribute_exact_match(selector, attributes, 'name'):
            return selector

        if single_attribute_exact_match(selector, attributes, 'placeholder'):
            return selector

        if single_attribute_exact_match(selector, attributes, 'type'):
            return selector

    text = get_text(element)
    if text:
        selector.exact_text = text

        if is_unique(selector):
            return selector

    if single_attribute_exact_match(selector, attributes, 'title'):
        return selector

    if single_attribute_exact_match(selector, attributes, 'alt'):
        return selector

    if single_attribute_exact_match(selector, attributes, 'aria-label'):
        return selector

    if element.tag_name == 'img':
        if single_attribute_exact_match(selector, attributes, 'src'):
            return selector

    if 'class' in attributes and attributes['class']:
        selector.css_classes = attributes['class'].split()

        if is_unique(selector):
            return selector

    return selector


# def get_reference_text(original):
#     reference_text = get_left_reference_text(original)
#     if reference_text:
#         selector = original.right_of(Text(reference_text))
#         if is_unique(selector):
#             return selector
#
#     reference_text = get_right_reference_text(original)
#     if reference_text:
#         if is_unique(selector):
#             return selector
#
#     reference_text = get_top_reference_text(original)
#     if reference_text:
#         if is_unique(selector):
#             return selector
#
#     return None

def is_input_text(element):
    if element.tag_name != 'input':
        return False

    attributes = get_attributes(element)
    return 'type' not in attributes or attributes['type'] == 'text'


def is_inside_table(element):
    return StaticElement(element).inside('table').exists()


def selector_to_string(selector):
    if not selector:
        return "# unable to build selector"

    result = 'Element(' + double_quotes_text(selector.tag_name)

    if selector.exact_text is not None:
        result += ', exact_text=' + double_quotes_text(selector.exact_text)

    if selector.exact_attributes:
        result += ', exact_attributes=%s' % selector.exact_attributes

    if selector.css_classes:
        result += ', css_classes=%s' % selector.css_classes

    result += ')'

    return result


def selector_to_selenium_string(selector):
    if not selector:
        return "# unable to build selector"

    ge_xpath_selector = selector.get_selectors()[0]
    result = 'XPath(' + double_quotes_text(remove_xpath_prefix(ge_xpath_selector)) + ')'
    return result


def remove_xpath_prefix(xpath_expression):
    XPATH_PREFIX = re.compile(r"^xpath:.?(.*?)$")
    m = XPATH_PREFIX.match(xpath_expression)

    if not m:
        return xpath_expression

    return m.group(1)


# Escapes the double quotes. If the string is unicode, it will
# prefix the entry with an 'u'
# FIXME: should backslash escapes be used?
def double_quotes_text(s):
    if not is_pure_ascii(s):
        return 'u"' + s.replace('"', '\\"', 100000) + '"'

    return '"' + s.replace('"', '\\"', 100000) + '"'


def is_pure_ascii(s):
    try:
        s.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def is_unique(selector):
    return len(selector.element_list()) == 1