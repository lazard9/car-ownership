import json
from typing import List, Optional

from models.users import NewUser, User


def load_users_data() -> List[User]:
    with open("data/users.json", "r") as f:
        users_data = json.load(f)
        users = [User(**user) for user in users_data]
        return users


def update_users_data(updated_users_data: List[User]):
    with open("data/users.json", "w") as f:
        updated_users_data_dict = [user.model_dump()
                                   for user in updated_users_data]
        json.dump(updated_users_data_dict, f, indent=2)


def find_user(user_id: int) -> Optional[User]:
    users_data = load_users_data()
    for user in users_data:
        if user.id == user_id:
            return user
    return None


def user_list() -> List[User]:
    users_data = load_users_data()
    return users_data


def find_user_by_mail(mail: str):
    users_data = load_users_data()

    for user in users_data:
        if user.mail == mail:
            return user
    return None


def create_user(new_user: NewUser) -> User:
    users_data = load_users_data()

    # Find biggest user ID in users data and increment
    max_id = max(user.id for user in users_data) if users_data else 0
    new_user_id = max_id + 1

    created_user = User(
        id=new_user_id,
        name=new_user.name,
        mail=new_user.mail,
        phone=new_user.phone,
        car_ownership=new_user.car_ownership,
    )

    users_data.append(created_user)

    update_users_data(users_data)

    return created_user


def delete_user_by_id(user_id: int) -> Optional[User]:
    users_data = load_users_data()

    # user_to_remove = None
    # for user in users_data:
    #     if user.id == user_id:
    #         user_to_remove = user
    #         break

    # if user_to_remove:
    #     users_data.remove(user_to_remove)

    #     update_users_data(users_data)

    #     return user_to_remove
    # else:
    #     return None

    # Simplified code!
    for user in users_data:
        if user.id == user_id:
            users_data.remove(user)
            update_users_data(users_data)
            return user

    return None
