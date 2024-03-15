import json
import shutil
from typing import List
from unittest import mock

import pytest

from models.cars import Car
from utils.car_utils import find_car, update_car_by_id


@pytest.fixture
def restore_file():
    yield
    shutil.copy2("tests/data/test_cars_backup.json",
                 "tests/data/test_cars.json")


def mock_load_cars_data() -> List[Car]:
    with open("tests/data/test_cars.json", "r") as f:
        cars_data = json.load(f)
        cars = [Car(**car) for car in cars_data]
        return cars


def mock_update_cars_data(update_cars_data: List[Car]):
    with open("tests/data/test_cars.json", "w") as f:
        cars_data_as_dict = [car.model_dump() for car in update_cars_data]
        json.dump(cars_data_as_dict, f, indent=2)


@mock.patch("utils.car_utils.load_cars_data")
def test_find_car(mocked_load_cars):
    mocked_load_cars.return_value = mock_load_cars_data()

    car_id = 1
    response = find_car(car_id)
    test_car = Car(
        id=1,
        name="Volkswagen ID.4",
        fuel="electric",
        category="compact",
        link="",
        horse_power=101,
        price=25025
    )

    assert response == test_car


@mock.patch("utils.car_utils.load_cars_data")
def test_find_car_none(mocked_load_cars):
    mocked_load_cars.return_value = mock_load_cars_data()

    response = find_car(333)

    assert response == None


@pytest.mark.usefixtures("restore_file")
def test_update_car_by_id(monkeypatch):

    monkeypatch.setattr(
        "utils.car_utils.load_cars_data.__code__", mock_load_cars_data.__code__)
    monkeypatch.setattr(
        "utils.car_utils.update_cars_data.__code__", mock_update_cars_data.__code__)

    car_id = 1
    update_data = Car(
        id=1,
        name="Volkswagen ID.5",
        fuel="electric",
        category="compact",
        link="",
        horse_power=202,
        price=35025
    )
    response = update_car_by_id(car_id, update_data)

    assert response == update_data


def test_update_car_by_id_none(monkeypatch):
    monkeypatch.setattr(
        "utils.car_utils.load_cars_data.__code__", mock_load_cars_data.__code__)
    monkeypatch.setattr(
        "utils.car_utils.update_cars_data.__code__", mock_update_cars_data.__code__)

    car_id = 333
    update_data = Car(
        id=333,
        name="Volkswagen ID.10",
        fuel="electric",
        category="compact",
        link="",
        horse_power=303,
        price=55025
    )
    response = update_car_by_id(car_id, update_data)

    assert response == None
