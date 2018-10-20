import unittest

from behave import use_step_matcher, step
import time
from germanium.static import *


use_step_matcher("re")

testcase = unittest.TestCase()
testcase.maxDiff = None
assertEqual = testcase.assertEqual
assertIsNotNone = testcase.assertIsNotNone


@step("I open the browser on the saved google page")
def open_browser_on_saved_google_page(context):
    go_to("http://localhost:8000/features/sites/saved_google")


@step("I open the browser on the static test page")
def open_browser_on_static_test_page(context):
    go_to("http://localhost:8000/features/sites/static_test_site")


@step("I try to resolve the element `(.*?)`")
def resolve_germanium_selector_in_js(context, source):
    element = eval(source + '.element()', globals(), dict())

    assertIsNotNone(element)

    js('window["__germaniumDebugMode"] = true;')
    loaded_code = read_file("js/main.js")
    js(loaded_code)

    context.resolved_selector = js('return germaniumResolveElement([arguments[0]])', element)


@step("I try to pick the element `(.*?)`")
def try_to_pick_the_element(context, source):
    # we inject first the code.
    loaded_code = read_file("js/main.js")

    js('window["__germaniumDebugMode"] = true;')
    js(loaded_code)
    js('germaniumPickElement(1)')

    click(eval(source, globals(), dict()))

    context.resolved_selector = js('return germaniumGetPickedElement().foundSelector')
    assertEqual(js('return pickState.state;'), 'READY')
    assertEqual(js('return mouseState.state;'), 'NOT_PRESSED')


@step("I try to pick (\\d+) elements: `(.*?)`")
def pick_two_elements(context, element_count, source):
    # we inject first the code.
    loaded_code = read_file("js/main.js")

    js('window["__germaniumDebugMode"] = true;')
    js(loaded_code)
    js('germaniumPickElement(%s)' % element_count)

    click(eval(source, globals(), dict()))


@step("using a reference of: `(.*?)`")
def pick_second_element(context, source):
    click(eval(source, globals(), dict()))
    context.resolved_selector = js('return germaniumGetPickedElement().foundSelector')

    assertEqual(js('return pickState.state;'), 'READY')
    assertEqual(js('return mouseState.state;'), 'NOT_PRESSED')


@step("using a first reference of: `(.*?)`")
def using_first_reference_of(context, source):
    click(eval(source, globals(), dict()))

    assertEqual(js('return pickState.state;'), 'PICKING')
    assertEqual(js('return mouseState.state;'), 'PICKING')


@step("using a second reference of: `(.*?)`")
def using_a_second_reference_of(context, source):
    click(eval(source, globals(), dict()))
    context.resolved_selector = js('return germaniumGetPickedElement().foundSelector')

    assertEqual(js('return pickState.state;'), 'READY')
    assertEqual(js('return mouseState.state;'), 'NOT_PRESSED')


@step('I start picking elements')
def start_picking_the_element(context):
    # we inject first the code.
    loaded_code = read_file("js/main.js")

    js('window["__germaniumDebugMode"] = true;')
    js(loaded_code)
    js('germaniumPickElement(1)')


@step('I cancel picking elements')
def cancel_picking_the_element(context):
    js('germaniumStopPickingElement()')


@step('the state of the browser is correct and accepting commands')
def is_the_correct_state(context):
    assertEqual(js('return pickState.state;'), 'READY')
    assertEqual(js('return mouseState.state;'), 'NOT_PRESSED')


@step("I get the xpath selector: (u?\".*?\")")
def validate_xpath_selector(context, expected_selector):
    assertEqual('XPath(' + expected_selector + ')', context.resolved_selector)


@step("I get the css selector: (u?\".*?\")")
def validate_css_selector(context, expected_selector):
    assertEqual('Css(' + expected_selector + ')', context.resolved_selector)


@step("I try to find the returned xpath selector")
def get_the_element_using_the_resolved_selector(context):
    context.found_element = eval(context.resolved_selector, globals(), locals()).element()


@step("I wait forever")
def i_sleep_forever(context):
    time.sleep(10000)


@step("I get the element: `(.*?)`")
def then_i_get_the_element(context, selector):
    reference_element = eval(selector, globals(), locals()).element()
    assertEqual(reference_element, context.found_element)


def read_file(path):
    with open(path, 'r') as myfile:
        return myfile.read()
