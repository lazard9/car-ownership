from typing import Optional

from fastapi.testclient import TestClient

from main import app, router
# from unittest.mock import patch
from models.cars import Car
from models.users import NewUser, User

client = TestClient(app)

"""
Home
"""


def test_read_root():
    response = client.get(router.url_path_for("read_root"))
    assert response.status_code == 200
    assert response.json() == {"Hello": "Cars"}


"""
Cars endpoints
"""


def mock_find_car(car_id: int) -> Optional[Car]:
    if car_id == 1:
        return Car(
            id=1,
            name="Test Car I",
            fuel="test fuel",
            category="test cat",
            link="",
            horse_power=99,
            price=50000
        )
    return None


# GET car by id
def test_get_car(monkeypatch):

    monkeypatch.setattr("utils.car_utils.find_car.__code__",
                        mock_find_car.__code__)

    response = client.get(router.url_path_for("get_car", car_id=1))

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Car I",
        "fuel": "test fuel",
        "category": "test cat",
        "link": "",
        "horse_power": 99,
        "price": 50000
    }


def test_get_car_none(monkeypatch):

    monkeypatch.setattr("utils.car_utils.find_car.__code__",
                        mock_find_car.__code__)

    response = client.get(router.url_path_for("get_car", car_id=2))

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Car not found"
    }


# PUT (update) car by id
def mock_update_car_by_id(car_id: int, update_data: Car):
    
    if car_id == 1:
        return update_data
    
    return None


def test_update_car_by_id(monkeypatch):

    monkeypatch.setattr(
        "utils.car_utils.update_car_by_id.__code__", mock_update_car_by_id.__code__)

    response = client.put(router.url_path_for("update_car", car_id=1), json={
        "id": 1,
        "name": "Test Car IV",
        "fuel": "test fuel",
        "category": "test car",
        "link": "",
        "horse_power": 399,
        "price": 100000
    })

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Test Car IV",
        "fuel": "test fuel",
        "category": "test car",
        "link": "",
        "horse_power": 399,
        "price": 100000
    }


def test_update_car_by_id_none(monkeypatch):

    monkeypatch.setattr("utils.car_utils.update_car_by_id.__code__",
                        mock_update_car_by_id.__code__)

    response = client.put(router.url_path_for("update_car", car_id=2), json={
        "id": 2,
        "name": "Test Car V",
        "fuel": "test fuel",
        "category": "test car",
        "link": "",
        "horse_power": 599,
        "price": 140000
    })

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Car not found"
    }


"""
Users endpoints
"""


# POST (create) new user
def mock_find_user_by_mail(mail: str):
    if mail == "smith_example@mail.com":
        return User(
            id=1,
            name="Smith",
            mail="smith_example@mail.com",
            phone="11111111",
            car_ownership=[]
        )
    return None


# Da li je ovo neophodno i da li je dobar nacin?
# Razlog: usled greske kod mok funkcije mock_find_user_by_mail
# prilikom greske u proveri mejla doslo je do upisa u fajl novih usera!
def mock_create_user(new_user: NewUser):
    created_user = User(
        id=2,
        name=new_user.name,
        mail=new_user.mail,
        phone=new_user.phone,
        car_ownership=new_user.car_ownership
    )
    return created_user


# Check if user exists by email
def test_create_new_user_exists(monkeypatch):

    monkeypatch.setattr(
        "utils.user_utils.find_user_by_mail.__code__", mock_find_user_by_mail.__code__)
    monkeypatch.setattr(
        "utils.user_utils.create_user.__code__", mock_create_user.__code__)

    response = client.post(router.url_path_for("create_new_user"), json={
        "name": "Smith",
        "mail": "smith_example@mail.com",
        "phone": "11111111",
        "car_ownership": []
    })

    assert response.status_code == 400
    assert response.json() == {
        "detail": "User with this email already exists"
    }


# Create new user
def test_create_new_user(monkeypatch):

    monkeypatch.setattr(
        "utils.user_utils.create_user.__code__", mock_create_user.__code__)

    response = client.post(router.url_path_for("create_new_user"), json={
        "name": "New",
        "mail": "new_example@mail.com",
        "phone": "22222222",
        "car_ownership": []
    })

    assert response.status_code == 200
    assert response.json() == {
        "id": 2,
        "name": "New",
        "mail": "new_example@mail.com",
        "phone": "22222222",
        "car_ownership": []
    }


# DELETE user
def mock_delete_user_by_id(user_id: int):
    user_to_remove = None

    if user_id == 1:
        user_to_remove = User(
            id=1,
            name="Smith",
            mail="smith_example@mail.com",
            phone="11111111",
            car_ownership=[]
        )
        return user_to_remove

    return None


def test_delete_user(monkeypatch):

    monkeypatch.setattr(
        "utils.user_utils.delete_user_by_id.__code__", mock_delete_user_by_id.__code__)

    response = client.delete(router.url_path_for("delete_user", user_id=1))

    assert response.status_code == 200
    assert response.json() == {
        "message": "User Smith with ID 1 deleted successfully"
    }


def test_delete_car_none(monkeypatch):

    monkeypatch.setattr(
        "utils.user_utils.delete_user_by_id.__code__", mock_delete_user_by_id.__code__)

    response = client.delete(router.url_path_for("delete_user", user_id=2))

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User with ID 2 has not been found"
    }
