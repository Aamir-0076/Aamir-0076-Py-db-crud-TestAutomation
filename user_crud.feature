Feature: User Management in Database

Scenario: Insert a new user
  Given the database is initialized
  When I insert a user with name "Alice" and email "alice@example.com"
  Then the user should be present in the database

Scenario: Retrieve all users
  Given the database contains users
  When I fetch all users
  Then I should get a list of users

Scenario: Retrieve user by email
  Given a user with email "bob@example.com" exists
  When I search for the user by email "bob@example.com"
  Then I should find the user

Scenario: Update a user
  Given a user with email "charlie@example.com" exists
  When I update the user's name to "Charlie Updated" and email to "charlie_new@example.com"
  Then the user's details should be updated in the database

Scenario: Delete a user
  Given a user with email "dave@example.com" exists
  When I delete the user with email "dave@example.com"
  Then the user should no longer be in the database
