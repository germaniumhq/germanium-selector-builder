from germanium.static import *


def build_selector(element):
    selector = construct_germanium_selector(element)
    return selector_to_string(selector)


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



def construct_germanium_selector(element):
    if is_inside_table(element):
        pass

    attributes = get_attributes(element)

    if is_input_text(element):
        selector = InputText()

        if single_attribute_exact_match(selector, attributes, 'name'):
            return selector

        if single_attribute_exact_match(selector, attributes, 'placeholder'):
            return selector

        if 'class' in attributes and attributes['class']:
            selector.css_classes = attributes['class'].split()

        if is_unique(selector):
            return selector

    #reference_text = get_reference_text(selector)
    #if reference_text:
    #    return reference_text

    selector = Element(tag_name=element.tag_name)

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

    result = 'Element("%s"' % selector.tag_name

    if selector.exact_text is not None:
        result += ', exact_text="%s"' % selector.exact_text

    if selector.exact_attributes:
        result += ', exact_attributes=%s' % selector.exact_attributes

    if selector.css_classes:
        result += ', css_classes=%s' % selector.css_classes

    result += ')'

    return result


def is_unique(selector):
    return len(selector.element_list()) == 1