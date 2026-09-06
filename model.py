from pydantic import BaseModel


class UserRequest (BaseModel):
    name: str|None = None
    age : int

class UserResponse(BaseModel):
    
    name: str|None = None
    age : int 
    id : int
    model_config = {"from_attributes": True}

class PartialUserUpdate(BaseModel):
    name: str|None = None
    age : int|None = None
    model_config = {"from_attributes": True}