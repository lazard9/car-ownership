import json
import shutil
from typing import List

import pytest

from models.users import User
from utils.user_utils import delete_user_by_id


@pytest.fixture
def restore_file():
    yield
    shutil.copy2("tests/data/test_users_backup.json", "tests/data/test_users.json")


def mock_load_users_data() -> List[User]:
    with open("tests/data/test_users.json", "r") as f:
        users_data = json.load(f)
        users = [User(**car) for car in users_data]
        return users


def mock_update_users_data(update_users_data: List[User]):
    with open("tests/data/test_users.json", "w") as f:
        users_data_as_dict = [car.model_dump() for car in update_users_data]
        json.dump(users_data_as_dict, f, indent=2)


@pytest.mark.usefixtures("restore_file")
def test_delete_user_by_id(monkeypatch):

    monkeypatch.setattr(
        "utils.user_utils.load_users_data.__code__", mock_load_users_data.__code__)
    monkeypatch.setattr(
        "utils.user_utils.update_users_data.__code__", mock_update_users_data.__code__)

    user_id = 1
    user = User(
        id=1,
        name="Marko",
        mail="example_marko@mail.com",
        phone="98769878",
        car_ownership=[4,2]
    )
    deleted_user = delete_user_by_id(user_id)

    assert deleted_user == user
    assert user_id not in [user.id for user in mock_load_users_data()]


def test_delete_user_by_id_none(monkeypatch):
    monkeypatch.setattr(
        "utils.user_utils.load_users_data.__code__", mock_load_users_data.__code__)
    monkeypatch.setattr(
        "utils.user_utils.update_users_data.__code__", mock_update_users_data.__code__)

    user_id = 333
    deleted_user = delete_user_by_id(user_id)

    assert deleted_user == None
