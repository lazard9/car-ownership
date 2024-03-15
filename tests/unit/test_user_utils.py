
from typing import List
from unittest import mock

from models.users import User
from utils.user_utils import delete_user_by_id


def mock_load_users_data() -> List[User]:
    return [
        User(
            id=1,
            name="Stan",
            mail="example_stan@mail.com",
            phone="98769878",
            car_ownership=[1, 4, 6]
        ),
        User(
            id=2,
            name="Joe",
            mail="example_joe@mail.com",
            phone="32369668",
            car_ownership=[2, 3]
        ),
        User(
            id=3,
            name="Jack",
            mail="example_jack@mail.com",
            phone="98236446",
            car_ownership=[5]
        ),
    ]


@mock.patch("utils.user_utils.load_users_data")
@mock.patch("utils.user_utils.update_users_data")
def test_delete_user_by_id(mocked_update_users, mocked_load_users):
    mocked_load_users.return_value = mock_load_users_data()
    mocked_update_users.return_value = None

    user_id = 3
    user_to_remove = delete_user_by_id(user_id)

    expected_user = User(
        id=3,
        name="Jack",
        mail="example_jack@mail.com",
        phone="98236446",
        car_ownership=[5]
    )

    assert user_to_remove == expected_user


@mock.patch("utils.user_utils.load_users_data")
@mock.patch("utils.user_utils.update_users_data")
def test_delete_user_by_id_none(mocked_update_users, mocked_load_users):
    mocked_load_users.return_value = mock_load_users_data()
    mocked_update_users.return_value = None

    user_id = 3333
    user_to_remove = delete_user_by_id(user_id)

    assert user_to_remove == None
