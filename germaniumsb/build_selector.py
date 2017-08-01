from germanium.static import *


def build_selector(element):
    selector = construct_germanium_selector(element)
    return selector_to_string(selector)


def construct_germanium_selector(element):
    if is_inside_table(element):
        pass

    if is_input_text(element):
        selector = InputText()
        attributes = get_attributes(element)
        if 'name' in attributes:
            if not selector.exact_attributes:
                selector.exact_attributes = {}
            selector.exact_attributes['name'] = attributes['name']

        if 'placeholder' in attributes:
            if not selector.exact_attributes:
                selector.exact_attributes = {}
            selector.exact_attributes['placeholder'] = attributes['placeholder']

        if is_unique(selector):
            return selector

        #reference_text = get_reference_text(selector)
        #if reference_text:
        #    return reference_text

    return None


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
    result = 'Element("%s"' % selector.tag_name

    if selector.exact_attributes:
        result += ', exact_attributes=%s' % selector.exact_attributes

    result += ')'

    return result


def is_unique(selector):
    return len(selector.element_list()) == 1