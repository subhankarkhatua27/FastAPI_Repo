


from sqlalchemy import select

from fastapi import  FastAPI,Depends, HTTPException
from database import  User, RegisterDetails
from session import get_session
from check_auth import get_current_user, get_current_user_for_refresh 
from model import PartialUserUpdate, UserRequest, UserResponse,RegisterRequest, RegisterResponse, LoginRequest, RefreshTokenRequest
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError
from fastapi import Request
from fastapi.responses import JSONResponse
from reg_login import generate_jwt_access_token, generate_jwt_refresh_token, hash_generator, verify_password 
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None :
    raise RuntimeError(" can't find SECRET_KEY in environment variables. Please set it in .env file")

SECRET_REFRESH_KEY = os.getenv("SECRET_REFRESH_KEY")
if SECRET_REFRESH_KEY is None :
    raise RuntimeError(" can't find SECRET_REFRESH_KEY in environment variables. Please set it in .env file")

ALGORITHM = os.getenv("ALGORITHM")
if ALGORITHM is None :
    raise RuntimeError(" can't find ALGORITHM in environment variables. Please set it in .env file")

app=FastAPI()
@app.post("/register", response_model=RegisterResponse)
def register_user(data:RegisterRequest ,session:Session=Depends(get_session)):
    with session.begin():
        existing_user=session.scalar(select(RegisterDetails).where (RegisterDetails.email == data.email))
        
        if existing_user:
            raise HTTPException(
                status_code = 401,
                detail = "Email already registered",
                
            )

        registered_user = RegisterDetails(
            user_id = data.user_id,
            password_hash = hash_generator(data.password),
            email = data.email
                
        )
         
        session.add(registered_user)
        session.flush()
        session.refresh(registered_user)
        
    return registered_user


@app.post("/login")
def login_user(data:LoginRequest, session:Session=Depends(get_session)):
    with session.begin():
        user = session.scalar(select(RegisterDetails).where(RegisterDetails.email == data.email))
        
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code = 401,
                detail = "Invalid email or password"
            )
        
    access_token = generate_jwt_access_token(user.user_id, secret_key=SECRET_KEY , algorithm= ALGORITHM)
    refresh_token = generate_jwt_refresh_token(user.user_id, secret_key=SECRET_REFRESH_KEY , algorithm= ALGORITHM)
        
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
@app.post("/refresh")
def refresh_token_endpoint( data:RefreshTokenRequest, user : RegisterDetails = Depends(get_current_user_for_refresh)):
    new_access_token = generate_jwt_access_token(user.user_id, secret_key=SECRET_KEY , algorithm= ALGORITHM)
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
        



@app.exception_handler(IntegrityError)
def handle_integrity_error(request:Request, exc:IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Integrity error: likely a duplicate entry or constraint violation"}
    )
@app.get("/users", response_model= UserResponse)
def get_user(session : Session = Depends(get_session), current_user: RegisterDetails = Depends(get_current_user)):
    
    with session.begin():
        user = session.get(User,1)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
    return user

@app.post("/users", response_model= UserResponse)
def create_user(data:UserRequest, session:Session = Depends(get_session), current_user: RegisterDetails = Depends(get_current_user)):
    with session.begin():
        user = User(name=data.name, age=data.age)
        session.add(user)
        session.flush()
        session.refresh(user)
    return user

@app.patch("/users/:user_id", response_model=PartialUserUpdate)
def update_user(user_id:int , data:PartialUserUpdate, session:Session = Depends(get_session), current_user: RegisterDetails = Depends(get_current_user)):
    with session.begin():
        user = session.get(User,user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        update_data = data.model_dump(exclude_unset = True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        
        session.flush()
        session.refresh(user)
    return user