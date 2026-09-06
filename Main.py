


from fastapi import  FastAPI,Depends, HTTPException
from database import  User
from session import get_session
from model import UserRequest, UserResponse
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError
from fastapi import Request
from fastapi.responses import JSONResponse

app=FastAPI()

@app.exception_handler(IntegrityError)
def handle_integrity_error(request:Request, exc:IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Integrity error: likely a duplicate entry or constraint violation"}
    )
@app.get("/users", response_model= UserResponse)
def get_user(session : Session = Depends(get_session)):
    
    with session.begin():
        user = session.get(User,1)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
    return user

@app.post("/users", response_model= UserResponse)
def create_user(data:UserRequest, session:Session = Depends(get_session)):
    with session.begin():
        user = User(name=data.name, age=data.age)
        session.add(user)
        session.flush()
        session.refresh(user)
    return user
