


from fastapi import  FastAPI,Depends
from database import User
from session import get_session
from model import UserRequest, UserResponse
from sqlalchemy.orm import Session 





app = FastAPI()
@app.get("/users", response_model= UserResponse)
def get_user(session : Session = Depends(get_session)):
    
    with session.begin():
        user = session.get(User,1)
        
    return user

@app.post("/users", response_model= UserResponse)
def create_user(data:UserRequest, session:Session = Depends(get_session)):
    with session.begin():
        user = User(name=data.name, age=data.age)
        session.add(user)
        session.flush()
        session.refresh(user)
    return user
