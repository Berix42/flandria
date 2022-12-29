Feature: Navigation
  Validate that page-navigation is working

  Scenario: Navigate from Frontpage to Flandria API
    Given I open the site "/"
    When I click on the link "Flandria API"
    Then I expect a new tab has been opened
    When I focus the last opened tab
    Then I expect the url to contain "/api"

  Scenario: Navigate from the Frontpage to the monster "Weak Fungi"
    Given I open the site "/"
    When I click on the link "Monsters"
    Then I expect that the title is "Monster | Flandria"
    And I expect the url to contain "/database/monster?page=1&sort=index&filter=all&area=-1&effects=%5B%5D&order=asc"
    And I wait on element "h3" for 5000ms to exist
    When I click on the element "h3"
    Then I expect the url to contain "/database/monster/mtpunjai1"
    And I wait on element "h2" for 5000ms to exist
    And I expect that the title is "Weak Fungi | Flandria"
    And I expect that element "h2" contains the text "Weak Fungi"
