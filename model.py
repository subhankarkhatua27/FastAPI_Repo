from pydantic import BaseModel, EmailStr


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
    
class RegisterRequest(BaseModel):
    user_id:int
    password:str
    email:EmailStr
    
class RegisterResponse(BaseModel):
    user_id:int
    email:EmailStr
    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    email:EmailStr
    password:str
    
class RefreshTokenRequest(BaseModel):
    refresh_token:str