Feature: Picking elements with the mouse should work as expected.

@1
Scenario: Picking an input with the mouse should work correctly
  Given I open the browser on the saved google page
  When I try to pick the element `InputText()`
  Then I get the css selector: "input[name='q']"

@2
Scenario: Picking two elements that are close to each other
          with the mouse should work correctly
  Given I open the browser on the saved google page
  When I try to pick 2 elements: `Element('span').right_of(InputText())`
  And using a reference of: `InputText()`
  Then I get the xpath selector: "//input[@name='q']/../../..//span[contains(concat(' ', @class, ' '), ' gsri_a ')]"
  When I try to find the returned xpath selector
  Then I get the element: `Element('span').right_of(InputText())`

@3
Scenario: Picking two elements that are far to each other
          with the mouse should work correctly
  Given I open the browser on the saved google page
  When I try to pick 2 elements: `InputText()`
  And using a reference of: `Text("Österreich")`
  Then I get the xpath selector: u"//div[string()='Österreich'][contains(concat(' ', @class, ' '), ' logo-subtext ')]/../../../../../../..//input[@name='q']"
  When I try to find the returned xpath selector
  Then I get the element: `InputText()`

@4
Scenario: Picking three elements with the mouse should
          work correctly.
  Given I open the browser on the saved google page
  When I try to pick 3 elements: `InputText()`
  And using a first reference of: `Element('span').right_of(InputText())`
  And using a second reference of: `Text("Österreich")`
  Then I get the xpath selector: u"//div[string()='Österreich'][contains(concat(' ', @class, ' '), ' logo-subtext ')]/../../../../../../..//span[contains(concat(' ', @class, ' '), ' gsri_a ')]/../../..//input[@name='q']"
  When I try to find the returned xpath selector
  Then I get the element: `InputText()`

@5
Scenario: Picking and cancelling should work correctly.
  Given I open the browser on the saved google page
  When I start picking elements
  And I cancel picking elements
  Then the state of the browser is correct and accepting commands

@6
Scenario: Picking the same element twice, should return the single element once.
  Given I open the browser on the saved google page
  When I try to pick 2 elements: `InputText()`
  And using a reference of: `InputText()`
  Then I get the xpath selector: "//input[@name='q']"

@7
Scenario: Picking an element that is nested in another element, with the parent as a reference should yield the reference
  Given I open the browser on the saved google page
  When I try to pick 2 elements: `Element('a', exact_text='Deutsch')`
  And using a reference of: `XPath("//div[string()='Google.at offered in: Deutsch ']")`
  Then I get the xpath selector: "//div[string()='Google.at offered in: Deutsch ']//a[string()='Deutsch']"

@8
Scenario: Picking an image should get only the image reference.
  Given I open the browser on the static test page
  When I try to pick the element `Css("#single-matching")`
  Then I get the xpath selector: "//img[contains(normalize-space(@src), '/cool.png')]"

@9
Scenario: Picking an image that matches shuld get the real reference
  Given I open the browser on the static test page
  When I try to pick the element `Css("#double-matching1")`
  Then I get the css selector: "img[src='/some/image/image.png']"

@10
Scenario: Picking an input where a focus class gets assigned,
    should not return the focus class in the returned selector.
  Given I open the browser on the static test page
  When I try to pick the element `Css("#first-input")`
  Then I get the css selector: "input[name='address'].short-identifier"
