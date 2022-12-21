Feature: Frontpage
  Validate that frontpage is loading and functional

  Scenario: Frontpage shows welcome message
    When I open the site "http://localhost"
    Then I expect that element "h1" contains the text "Welcome to Flandria"
