# README.md
# Automation Testing for Database Operations

## Objective
Develop automated tests for a simple Python application interacting with an SQLite database. The goal is to validate CRUD operations using BDD principles with pytest and Behave.

## Scope of Testing
- **Insert Operation**: Verify successful insertion of new user records.
- **Read Operation**: Ensure retrieval of all users and searching by email.
- **Update Operation**: Confirm updates reflected in subsequent reads.
- **Delete Operation**: Validate users are deleted and not retrievable.

## Technology Stack
- Python
- SQLite
- Behave (for BDD scenarios)
- pytest (for test execution)

## Running the Tests
```sh
pip install -r requirements.txt
pytest test_database.py
behave
```

## Expected Outcome
The automated tests should ensure full coverage of database operations, robustness, and accuracy. They should be reusable, maintainable, and provide meaningful output.

## Additional Considerations
- Ensure tests are idempotent.
- Handle edge cases (duplicate emails, non-existent users, etc.).
- Implement logging for tracking test execution and failures.
---------------------------------------------------------------------------------------------

# firstDatabaseApp.py
import sqlite3

class DatabaseApp:
    def __init__(self, db_name="test.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """)
        self.conn.commit()

    def insert_user(self, name, email):
        try:
            self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()

    def update_user(self, user_id, name, email):
        self.cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return self.cursor.rowcount

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DatabaseApp()
    user_id = db.insert_user("John Doe", "john@example.com")
    print(f"Inserted User ID: {user_id}")
    print("All Users:", db.get_all_users())
    print("Search User:", db.get_user_by_email("john@example.com"))
    db.update_user(user_id, "John Updated", "john_updated@example.com")
    print("After Update:", db.get_all_users())
    db.delete_user(user_id)
    print("After Deletion:", db.get_all_users())
    db.close()

-------------------------------------------------------------------------------------------------------------
# test_database.py
import pytest
from firstDatabaseApp import DatabaseApp

@pytest.fixture
def db():
    db_instance = DatabaseApp(":memory:")
    yield db_instance
    db_instance.close()

def test_insert_user(db):
    user_id = db.insert_user("Eve", "eve@example.com")
    assert user_id is not None
    user = db.get_user_by_email("eve@example.com")
    assert user is not None

def test_get_all_users(db):
    db.insert_user("Frank", "frank@example.com")
    db.insert_user("Grace", "grace@example.com")
    users = db.get_all_users()
    assert len(users) == 2

def test_get_user_by_email(db):
    db.insert_user("Hank", "hank@example.com")
    user = db.get_user_by_email("hank@example.com")
    assert user is not None

def test_update_user(db):
    user_id = db.insert_user("Ivy", "ivy@example.com")
    db.update_user(user_id, "Ivy Updated", "ivy_updated@example.com")
    updated_user = db.get_user_by_email("ivy_updated@example.com")
    assert updated_user is not None
    assert updated_user[1] == "Ivy Updated"

def test_delete_user(db):
    user_id = db.insert_user("Jack", "jack@example.com")
    db.delete_user(user_id)
    user = db.get_user_by_email("jack@example.com")
    assert user is None

------------------------------------------------------------------------------------------------------------------------------
# features/user_management.feature
Feature: User Management in Database

Scenario: Insert a new user
  Given the database is initialized
  When I insert a user with the name "Alice" and email "alice@example.com"
  Then the user should be present in the database

Scenario: Retrieve all users
  Given the database contains users
  When I fetch all users
  Then I should get a list of users

Scenario: Retrieve the user by email
  Given a user with the email "bob@example.com" exists
  When I search for the user by email "bob@example.com"
  Then I should find the user

Scenario: Update a user
  Given a user with the email "charlie@example.com" exists
  When I update the user's name to "Charlie Updated" and email to "charlie_new@example.com"
  Then the user's details should be updated in the database

Scenario: Delete a user
  Given a user with the email "dave@example.com" exists
  When I delete the user with the email "dave@example.com"
  Then the user should no longer be in the database


