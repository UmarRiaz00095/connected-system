Feature: Connected Inventory to Storefront Journey
  
  @smoke @regression @api @ui
  Scenario: Create inventory item via API and process it in UI
    Given a new pet is created in the inventory system
    When the user logs into the storefront
    And the user completes a checkout using the pet data
    Then the order should be completed successfully