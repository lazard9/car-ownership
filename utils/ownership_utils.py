from typing import Optional

from models.cars import CarOwnershipDTO
from models.users import User, UserData
from utils.car_utils import load_cars_data
from utils.user_utils import load_users_data, update_users_data


def user_ownership_data(user: User) -> Optional[UserData]:
    cars_data = load_cars_data()
    users_data = load_users_data()

    user_cars_ids = None
    for item in users_data:
        if item.id == user.id:
            user_cars_ids = item.car_ownership
            break

    if user_cars_ids:
        # Pronalaženje automobila koji pripadaju korisniku
        user_cars = [car for car in cars_data if car.id in user_cars_ids]
        # Izračunavanje ukupne vrednosti automobila
        total_car_value = sum(car.price for car in user_cars)
    else:
        total_car_value = 0

    # Kreiranje UserData objekta sa total_car_value
    user_data = UserData(user=user, total_car_value=total_car_value)

    return user_data


def update_car_ownership(car_id: int, user_id: int) -> CarOwnershipDTO:
    users_dat = load_users_data()

    # Proveravamo da li je automobil u vlasnistvu
    for user in users_dat:
        if car_id in user.car_ownership:
            # Da li pripada bas ovom kupcu?
            if user.id == user_id:
                return CarOwnershipDTO(
                    message=f"Car ID {car_id} already belongs to the user ID {user_id}.",
                    user_id=user.id,
                    cars=user.car_ownership
                )

            # Uklanjamo ga ukoliko pripada drugom kupcu
            user.car_ownership.remove(car_id)
            break

    for user in users_dat:
        if user_id == user.id:
            user.car_ownership.append(car_id)

            update_users_data(users_dat)

            return CarOwnershipDTO(
                message=f"Car {car_id} successfully bought",
                user_id=user.id,
                cars=user.car_ownership
            )
