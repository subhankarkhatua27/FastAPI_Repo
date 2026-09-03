from pydantic import BaseModel

class UserRequest (BaseModel):
    name: str|None = None
    age : int

class UserResponse(BaseModel):
    
    name: str|None = None
    age : int 
    id : str   