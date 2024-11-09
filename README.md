# Spy Cat Agency API

The goal of this project is to develop a management application for the Spy Cat Agency (SCA). 
This API will streamline the management of spy cats, their missions, and the targets they are assigned to. 
The system includes functionality to create, update, and delete spy cats and missions, and ensures that 
target information is appropriately handled throughout the mission lifecycle.


## Core Features

1. **Spy Cat Management**
   - Create Spy Cat: Add a new spy cat with Name, Years of Experience, Breed, and Salary. 
   - Update Spy Cat: Modify the spy cat’s information (e.g., Salary). 
   - Delete Spy Cat: Remove a spy cat from the system. 
   - List Spy Cats: View all spy cats in the system. 
   - Get Single Spy Cat: Retrieve information about a specific spy cat.

2. **Mission and Target Management**
   - Create Mission with Targets: Add a mission with 1-3 targets in a single request. A mission contains the spy cat assigned, the targets, and the completion status of the mission. 
   - Update Mission: Modify mission details and its targets. Marks targets as completed or updates notes if the mission is not completed. 
   - Delete Mission: Remove a mission from the system. A mission cannot be deleted if it is already assigned to a cat. 
   - Assign Spy Cat to Mission: Assign a spy cat to a mission, ensuring the cat is not already on another mission. 
   - List Missions: View all missions and their statuses. 
   - Get Single Mission: Retrieve information about a specific mission, including its targets and their completion status.
   - Automatic setting of the completed task status if all targets are completed.

3. **Data Integrity and Validations**
   - Validates cat breed using TheCatAPI.
   - Ensures that notes cannot be updated once a target or mission is completed.
   - Targets are unique to a mission, and each mission contains 1-3 targets. 
   - Validates request bodies and returns adequate status codes for invalid data.


## Installation

1. **Clone the repository**:
    ```
    git clone https://github.com/lilarin/Spy-Cat-Agency-API.git
    ```
2. **Create a virtual environment**:
    ```
    python -m venv env
    source env/bin/activate
    ```
### Run without docker:

1. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```
2. **Apply migrations**:
    ```
    python manage.py migrate
    ```
3. **Run the development server**:
    ```
    python manage.py runserver
    ```

4. (Optional) **Run the tests**:
    ```
    python manage.py test
    ```

### Run with Docker:

1. **Launch Docker application**:

2. **Run the docker-compose**:
    ```
    docker-compose up --build
   ```
3. (Optional) **Run the tests**:
    ```
    python manage.py test
    ```

## API Endpoints

- **[Postman collection with all of the endpoints](https://www.postman.com/material-geoscientist-76643827/spy-cat-agency-api/collection/upfwu0r/spy-cat-agency-api?action=share&creator=38092262)**

- **Swagger documentation with all API endpoints**:
  - `/api/doc/swagger`

![img.png](https://imgur.com/eT6TObg.png)

## Environment Variables

This project uses environment variables to manage sensitive 
settings like API keys, database configurations, etc. Ensure
you create a `.env` file based on `.env.sample` in the root directory and set
the required environment variables before running the project.

## Requirements
- **Python**: 3.8+ (recommended 3.12+)
- **PostgreSQL**: 13.0+
