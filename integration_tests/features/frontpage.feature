Feature: Frontpage
  Validate that frontpage is loading and functional

  Scenario: Frontpage shows welcome message
    When I open the site "/"
    Then I expect that element "h1" contains the text "Welcome to Flandria"
    And I expect that the title is "Home | Flandria"
