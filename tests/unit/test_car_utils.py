from operator import attrgetter
from typing import List
from unittest import mock

import pytest
from fastapi import HTTPException

from models.cars import Car
from utils.car_utils import find_car, sort_cars, update_car_by_id


def mock_load_cars_data() -> List[Car]:
    return [
        Car(
            id=1,
            name="Test Car I",
            fuel="test fuel",
            category="coupe",
            link="",
            horse_power=399,
            price=100000
        ),
        Car(
            id=2,
            name="Test Car II",
            fuel="test fuel",
            category="compact",
            link="",
            horse_power=199,
            price=60000
        ),
        Car(
            id=3,
            name="Test Car III",
            fuel="test fuel",
            category="compact",
            link="",
            horse_power=299,
            price=70000
        ),
    ]


@mock.patch("utils.car_utils.load_cars_data")
def test_find_car(mocked_load_cars):
    mocked_load_cars.return_value = mock_load_cars_data()

    car_id = 2
    result = find_car(car_id)

    expected_car = Car(
        id=2,
        name="Test Car II",
        fuel="test fuel",
        category="compact",
        link="",
        horse_power=199,
        price=60000
    )

    assert result == expected_car


@mock.patch("utils.car_utils.load_cars_data")
def test_find_car_none(mocked_load_cars):
    mocked_load_cars.return_value = mock_load_cars_data()

    car_id = 333
    result = find_car(car_id)

    assert result is None


@mock.patch("utils.car_utils.load_cars_data")
@mock.patch("utils.car_utils.update_cars_data")
def test_update_car_by_id(mocked_update_cars, mocked_load_cars):
    mocked_load_cars.return_value = mock_load_cars_data()
    mocked_update_cars.return_value = None

    car_id = 2
    update_data = Car(
        id=2,
        name="Test Car 2",
        fuel="test bio fuel",
        category="compact",
        link="",
        horse_power=249,
        price=65000
    )

    updated_car = update_car_by_id(car_id, update_data)

    assert updated_car == update_data


@mock.patch("utils.car_utils.load_cars_data")
@mock.patch("utils.car_utils.update_cars_data")
def test_update_car_by_id_none(mocked_update_cars, mocked_load_cars):
    mocked_load_cars.return_value = mock_load_cars_data()
    mocked_update_cars.return_value = None

    car_id = 3333
    update_data = Car(
        id=3333,
        name="Test Car",
        fuel="test fuel",
        category="compact",
        link="",
        horse_power=349,
        price=75000
    )

    result = update_car_by_id(car_id, update_data)

    assert result == None


def test_sort_cars_invalid_param():

    with pytest.raises(HTTPException) as exception:
        sort_cars("invalid_param", "invalid_param_2")

    assert exception.value.status_code == 400
    assert exception.value.detail == "Invalid sorting parameter"


@mock.patch("utils.car_utils.load_cars_data")
def test_sort_cars_by_horse_power(mocked_load_cars):
    mocked_load_cars.return_value = mock_load_cars_data()

    sorted_cars = sort_cars("price", "")
    sorted_and_searched_cars = sort_cars("price", "compact")

    test_cars = mock_load_cars_data()
    mock_sorted_cars = sorted(test_cars, key=attrgetter(
        "horse_power"))

    mock_sorted_searched_cars = []
    if test_cars:
        filtered_cars = []
        for car in test_cars:
            if car.category == "compact":
                filtered_cars.append(car)

        mock_sorted_searched_cars = filtered_cars

    assert sorted_cars == mock_sorted_cars
    assert sorted_and_searched_cars == mock_sorted_searched_cars


@mock.patch("utils.car_utils.load_cars_data")
def test_sort_cars_list_order(mocked_load_cars):
    mocked_load_cars.return_value = mock_load_cars_data()

    # Empty stgrings for Query param
    sorted_cars = sort_cars("", "")

    mock_sorted_cars = mock_load_cars_data()

    assert sorted_cars == mock_sorted_cars
