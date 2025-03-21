# fastapi_tutorial
This project is a simple web application built using FastAPI. It performs the CRUD operations for registering the user and storing in the database. For this project, we are using SQLite database, since python has in-built support for it.

## Table of Contents
- Technologies Used
- Installation
- Usage

## Technologies Used
- OS: Windows 10
- Python 3.8.8
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

## Installation
1. Create the python environment:
python -m venv <name of the environment>
2. Activate the environment:
.\tutorial\Scripts\activate
Here tutorial is the name of the environment.
3. Install necessary python libraries:
    a. FastAPI: pip install fastapi
    b. Uvicorn: pip install uvicorn
    c. SQLAlchemy: pip install sqlalchemy
4. Run the application
uvicorn main:app --reload

## Usage
http://localhost:8000/docs
 
