import pytest
from DatabaseApp import DatabaseApp

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
