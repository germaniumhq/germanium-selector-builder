Feature: Resolving elements should work as expected.

Scenario: Resolving the google input should work as expected
  Given I open the browser on the saved google page
  When I try to resolve the element `InputText()`
  Then I get the css selector: "input[name='q']"

Scenario: Resolving the google search button should work as expected
  Given I open the browser on the saved google page
  When I try to resolve the element `Button("Google Search")`
  Then I get the css selector: "input[type='submit'][value='Google Search']"

Scenario: Resolving the google country text should work as expected
  Given I open the browser on the saved google page
  When I try to resolve the element `Text("Österreich")`
  Then I get the xpath selector: u"//div[string()='Österreich'][contains(concat(' ', @class, ' '), ' logo-subtext ')]"

Scenario: Resolving the bottom div should work as expected
  Given I open the browser on the saved google page
  When I try to resolve the element `Css("div.fbar")`
  Then I get the css selector: "div.fbar"

