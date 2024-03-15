"""Module defines the main FastAPI application."""

from typing import List, Optional

from fastapi import APIRouter, FastAPI, HTTPException, Query

from models.cars import Car, CarOwnershipDTO, HelloCars
from models.users import NewUser, User, UserData
from utils.car_utils import find_car, sort_cars, update_car_by_id
from utils.ownership_utils import update_car_ownership, user_ownership_data
from utils.user_utils import (create_user, delete_user_by_id, find_user,
                              find_user_by_mail, user_list)

app = FastAPI()

router = APIRouter(prefix="/api/v1")


@router.get("/", response_model=HelloCars)
def read_root():
    """Root endpoint returning a HelloCars message."""
    return HelloCars(Hello="Cars")


@router.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int):
    """Retrieve details of a specific car by its ID."""
    car = find_car(car_id)
    if car:
        return car
    raise HTTPException(status_code=404, detail="Car not found")


@router.get("/cars", response_model=List[Car])
def get_cars(
    sort_by: Optional[str] = Query(
        None, description="Sort cars by 'horse_power' or 'price'"),
    search_by: Optional[str] = Query(
        None, description="Search cars by category")
):
    """Retrieve a list of cars, with optional sorting and filtering parameters."""
    return sort_cars(sort_by, search_by)


@router.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, update_data: Car):
    """Update details of a specific car by its ID."""
    car = update_car_by_id(car_id, update_data)
    if car:
        return car
    raise HTTPException(status_code=404, detail="Car not found")


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Retrieve details of a specific user by their ID."""
    user = find_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/users", response_model=List[User])
def list_all_users():
    """Retrieve a list of all users."""
    all_users = user_list()
    return all_users


@router.post("/users", response_model=User)
def create_new_user(new_user: NewUser):
    """Create a new user."""
    existing_user = find_user_by_mail(new_user.mail)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    created_user = create_user(new_user)
    return created_user


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    """Delete a user by their ID."""
    deleted_user = delete_user_by_id(user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} has not been found"
        )
    return {"message": f"User {deleted_user.name} with ID {deleted_user.id} deleted successfully"}


@router.get("/users/{user_id}/car-info", response_model=UserData)
def get_user_data(user_id: int):
    """Retrieve ownership information for a specific user."""
    user = find_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    user_data = user_ownership_data(user)
    return user_data


@router.post("/cars/{car_id}/buy/{user_id}", response_model=CarOwnershipDTO)
def buy_car(
    car_id: int,
    user_id: int
):
    """Allow a user to buy a car."""
    car = find_car(car_id)
    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )
    user = find_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    new_ownership = update_car_ownership(car_id, user_id)
    return new_ownership


# Include router
app.include_router(router)
