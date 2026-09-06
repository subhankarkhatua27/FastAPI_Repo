


from fastapi import  FastAPI,Depends, HTTPException
from database import  User
from session import get_session
from model import PartialUserUpdate, UserRequest, UserResponse
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

@app.patch("/users/:user_id", response_model=PartialUserUpdate)
def update_user(user_id:int , data:PartialUserUpdate, session:Session = Depends(get_session)):
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