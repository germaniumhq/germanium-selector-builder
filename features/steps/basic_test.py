import unittest

from behave import *
from germanium.static import *

use_step_matcher("re")


assertEqual = unittest.TestCase().assertEqual
assertIsNotNone = unittest.TestCase().assertIsNotNone


@step("I open the browser on the saved google page")
def open_browser_on_saved_google_page(context):
    go_to("http://localhost:8000/features/sites/saved_google")


@step("I try to resolve the element `(.*?)`")
def resolve_germanium_selector_in_js(context, source):
    element = eval(source + '.element()', globals(), dict())

    assertIsNotNone(element)

    js('window["__germaniumDebugMode"] = true;')
    loaded_code = read_file("js/main.js")
    js(loaded_code)

    context.resolved_selector = js('return germaniumResolveElement(arguments[0])', element)


@step("I try to pick the element `(.*?)`")
def resolve_germanium_selector_in_js(context, source):
    # we inject first the code.
    loaded_code = read_file("js/main.js")

    js('window["__germaniumDebugMode"] = true;')
    js(loaded_code)
    js('germaniumPickElement()')

    click(eval(source, globals(), dict()))

    context.resolved_selector = js('return germaniumGetPickedElement()')
    assertEqual(js('return pickState.state;'), 'READY')
    assertEqual(js('return mouseState.state;'), 'NOT_PRESSED')


@step("I get the xpath selector: (u?\".*?\")")
def validate_xpath_selector(context, expected_selector):
    assertEqual('XPath(' + expected_selector + ')', context.resolved_selector)


def read_file(path):
    with open(path, 'r') as myfile:
        return myfile.read()
