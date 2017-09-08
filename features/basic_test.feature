Feature: Resolving elements should work as expected.

Scenario: Resolving the google input should work as expected
  Given I open the browser on the saved google page
  When I try to resolve the element `InputText()`
  Then I get the xpath selector: "//input[@name='q']"

Scenario: Resolving the google search button should work as expected
  Given I open the browser on the saved google page
  When I try to resolve the element `Button("Search")`
  Then I get the xpath selector: "//input[@name='q']"

Scenario: Resolving the google country text should work as expected
  Given I open the browser on the saved google page
  When I try to resolve the element `Text("Wut")`
  Then I get the xpath selector: "//span[contains(concat(' ', @class, ' '), ' wut '][string()='']"

