from typing import List

from pydantic import BaseModel


class HelloCars(BaseModel):
    Hello: str


class Car(BaseModel):
    id: int
    name: str
    fuel: str
    category: str
    link: str
    horse_power: int
    price: int


class CarOwnership(BaseModel):
    user_id: int
    cars: List[int]


class CarOwnershipDTO(CarOwnership):
    message: str
