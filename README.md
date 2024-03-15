# FastAPI Cars API

## Description
This repository contains a FastAPI application for managing car data and user interactions. The application includes functionalities such as retrieving car details, managing users, and handling car ownership.

## Table of Contents
- [Description](#description)
- [Endpoints](#endpoints)
- [Models](#models)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Requirements](#requirements)
- [Author](#author)
- [License](#license)

## Endpoints
- `GET /api/v1/cars/{car_id}`: Retrieve details of a specific car by its ID.
- `GET /api/v1/cars`: Retrieve a list of cars, with optional sorting and filtering parameters.
- `PUT /api/v1/cars/{car_id}`: Update details of a specific car by its ID.
- `GET /api/v1/users/{user_id}`: Retrieve details of a specific user by their ID.
- `GET /api/v1/users`: Retrieve a list of all users.
- `POST /api/v1/users`: Create a new user.
- `DELETE /api/v1/users/{user_id}`: Delete a user by their ID.
- `GET /api/v1/users/{user_id}/car-info`: Retrieve ownership information for a specific user.
- `POST /api/v1/cars/{car_id}/buy/{user_id}`: Allow a user to buy a car.

## Models
The application uses Pydantic models for type specification throughout the app. These models include:
- `Car`: Represents a car with its attributes.
- `User`: Represents a user with user-related data.
- `UserData`: Represents ownership information for a user.
- `NewUser`: Represents data for creating a new user.
- `CarOwnershipDTO`: Represents data for car ownership operations.

## Running the Application
To run the FastAPI application, you can execute the `main.py` file. Make sure you have Python and FastAPI installed.
```
uvicorn main:app --reload
```

## Testing
The repository includes unit and integration tests for testing the endpoints and functionality of the FastAPI application. You can run the tests using the following command:
```
pytest # Run all tests in the directory
python -m pytest -v  # Run tests with detailed output (verbose mode)
python -m pytest -s  # Run tests and show standard output (stdout) from tests
```

## Requirements
The application requires Python 3.x and the FastAPI library. You can install the dependencies using:
```
pip install -r requirements.txt
```

## Author
This FastAPI application was created by [lazard9](https://github.com/lazard9).

## License
This project is licensed under the GNU General Public License v2.0 or later.