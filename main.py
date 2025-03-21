"""
    Purpose: Build the web application performing CRUD operations using FastAPI
    Created At: 21st March,2025
    Author: Shivani Shah
"""
# Import the necessary libraries
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from typing import List
import datetime
import re


app=FastAPI()
SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    """
        Purpose: User Model
    """
    id:int
    username:str = Field(min_length=3,max_length=30)
    password:str = Field(min_length=8,max_length=15)

    @validator('username')
    def validate_username(cls,v):
        """
            Purpose: Validates username
        """
        if not(v.isalnum()):
            raise ValueError("Username should be alphanumeric only")
        return v
    
    @validator('password')
    def validate_password(cls,v):
        """
            Purpose: Validates password
        """
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        if re.match(pattern,v):
            return v
        raise ValueError("Password must contain atleast 1 capital letter, 1 small letter, 1 numeric and 1 special character atleast")
        
    class Config:
        orm_mode=True



@app.on_event("startup")
async def startup_event():
    """
        Purpose: Log the server start time
    """
    print("Server started: ",datetime.datetime.now())
    

@app.on_event("shutdown")
async def shutdown_event():
    """
        Purpose: Log the server shut down time
    """
    print("Server shutdown: ",datetime.datetime.now())


def get_db_connection():
    db=session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index():
    """
        Purpose: Home Page
    """
    return {"message":"Welcome to Home Page"}


@app.post("/register",response_model=User)
async def register_user(us1:User, db:Session=Depends(get_db_connection)):
    """
        Purpose: User registering
    """
    db_fetch_obj=db.query(Users).filter(Users.id==us1.id).first()
    if db_fetch_obj:
        raise HTTPException(status_code=400, detail="User with this id already exists")
    user_obj=Users(id=us1.id,username=us1.username,password=us1.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return Users(**us1.dict())

@app.get("/list",response_model=List[User])
async def get_users(db:Session=Depends(get_db_connection)):
    """
        Purpose: Get all users
    """
    users_list=db.query(Users).all()
    return users_list

@app.get("/user/{id}",response_model=User)
async def get_user_info(id:int,db:Session=Depends(get_db_connection)):
    """
        Purpose: Get user information for the given id
    """
    user_obj=db.query(Users).filter(Users.id==id).first()
    if not(user_obj):
        raise HTTPException(status_code=400,detail="User with the given id doesnot exist")
    return user_obj

@app.put("/update/{id}",response_model=User)
async def update_user(id:int,user_info:User,db:Session=Depends(get_db_connection)):
    """
        Purpose: Update user information for the given id
    """
    us1=db.query(Users).filter(Users.id==id).first()
    if not(us1):
        raise HTTPException(status_code=400,detail="User with the given id doesnot exist")
    us1.id=user_info.id
    us1.username=user_info.username
    us1.password=user_info.password
    db.commit()
    return db.query(Users).filter(Users.id==id).first()

@app.delete("/delete/{id}")
async def delete_user(id:int,db:Session=Depends(get_db_connection)):
    """
        Purpose: Delete user information for the given id
    """
    try:
        db.query(Users).filter(Users.id==id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
    return {"Delete status":"Success"}