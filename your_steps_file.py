from behave import given, when, then

from DatabaseApp import DatabaseApp


@given("the database is initialized")
def step_initialize_database(context):
    context.db = DatabaseApp(":memory:")  # Use in-memory DB for isolated tests

@when('I insert a user with name "{name}" and email "{email}"')
def step_insert_user(context, name, email):
    context.user_id = context.db.insert_user(name, email)

@then("the user should be present in the database")
def step_verify_user_exists(context):
    assert context.user_id is not None
    user = context.db.get_user_by_email("alice@example.com")
    assert user is not None

@given("the database contains users")
def step_insert_multiple_users(context):
    context.db = DatabaseApp(":memory:")
    context.db.insert_user("User1", "user1@example.com")
    context.db.insert_user("User2", "user2@example.com")

@when("I fetch all users")
def step_fetch_users(context):
    context.users = context.db.get_all_users()

@then("I should get a list of users")
def step_verify_users_list(context):
    assert len(context.users) > 0

@given('a user with email "{email}" exists')
def step_insert_specific_user(context, email):
    context.db = DatabaseApp(":memory:")
    context.user_id = context.db.insert_user("Test User", email)
    assert context.user_id is not None

@when('I search for the user by email "{email}"')
def step_search_user(context, email):
    context.user = context.db.get_user_by_email(email)

@then("I should find the user")
def step_verify_searched_user(context):
    assert context.user is not None



@given('a user exists with name "{name}" and email "{email}"')
def step_given_user_exists(context, name, email):
    """Ensure a user exists before updating."""
    context.db.insert_user(name, email)
    user = context.db.get_user_by_email(email)
    assert user is not None, f"User {email} was not inserted"
    context.user_id = user[0]  # Store user ID for updating

@when('I update the user\'s name to "{new_name}" and email to "{new_email}"')
def step_update_user(context, new_name, new_email):
    context.db.update_user(context.user_id, new_name, new_email)

@then("the user's details should be updated in the database")
def step_verify_updated_user(context):
    updated_user = context.db.get_user_by_email("charlie_new@example.com")
    assert updated_user is not None
    assert updated_user[1] == "Charlie Updated"


@given('a user with email "{email}" exists in the database')
def step_given_user_to_delete(context, email):
    """Ensure a user exists before deletion."""
    context.db.insert_user("Dave", email)
    user = context.db.get_user_by_email(email)
    assert user is not None, f"User {email} was not inserted"

@when('I delete the user with email "{email}"')
def step_delete_user(context, email):
    user = context.db.get_user_by_email(email)
    assert user is not None
    context.db.delete_user(user[0])

@then("the user should no longer be in the database")
def step_verify_user_deleted(context):
    user = context.db.get_user_by_email("dave@example.com")
    assert user is None
