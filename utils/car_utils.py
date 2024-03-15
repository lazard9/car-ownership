import json
from operator import attrgetter
from typing import List, Optional

from fastapi import HTTPException

from models.cars import Car


def load_cars_data() -> List[Car]:
    with open("data/cars.json", "r") as f:
        cars_data = json.load(f)
        cars = [Car(**car) for car in cars_data]
        # returns `<class 'list'>` containing `<class 'models.cars.Car'>` items
        return cars


def update_cars_data(updated_cars_data: List[Car]):
    with open("data/cars.json", "w") as f:
        cars_data_as_dict = [car.model_dump() for car in updated_cars_data]
        json.dump(cars_data_as_dict, f, indent=2)


def find_car(car_id: int) -> Optional[Car]:
    cars_data = load_cars_data()

    for car in cars_data:
        if car.id == car_id:
            return car
    return None


def sort_cars(sort_by: Optional[str], search_by: Optional[str]) -> List[Car]:
    cars = load_cars_data()

    if sort_by and sort_by not in {"horse_power", "price"}:
        raise HTTPException(
            status_code=400, detail="Invalid sorting parameter")

    if search_by and search_by not in {"compact", "suv", "sporting turbo"}:
        raise HTTPException(
            status_code=400, detail="Invalid sorting parameter")

    if search_by:
        filtered_cars = []
        for car in cars:
            if car.category == search_by:
                filtered_cars.append(car)

        cars = filtered_cars

    if sort_by:
        sorted_cars = sorted(cars, key=attrgetter(sort_by))
        cars = sorted_cars

    return cars


def update_car_by_id(car_id: int, update_data: Car) -> Optional[Car]:
    cars_data = load_cars_data()

    for car in cars_data:
        if car.id == car_id:
            for attr_name, attr_value in update_data.model_dump().items():
                setattr(car, attr_name, attr_value)

            update_cars_data(cars_data)

            return car

    return None
