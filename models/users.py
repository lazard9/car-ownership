from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    mail: str
    phone: str
    car_ownership: List[int]


class NewUser(BaseModel):
    name: str
    mail: str
    phone: str
    car_ownership: List[int]


class UserData(BaseModel):
    user: User
    total_car_value: int
