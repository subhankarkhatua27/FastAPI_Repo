from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException
import jwt
#from Main import SECRET_KEY,ALGORITHM    // it can create circular import risk.
from database import RegisterDetails
from session import get_session
import os
from dotenv import load_dotenv




load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


if SECRET_KEY is None :
    raise RuntimeError(" can't find SECRET_KEY in environment variables. Please set it in .env file")

if ALGORITHM is None :
    raise RuntimeError(" can't find ALGORITHM in environment variables. Please set it in .env file")

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def get_current_user(session:Session = Depends(get_session),
                     token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY, 
            algorithms = [ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    
    user = session.get(RegisterDetails, user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    return user


def get_current_user_for_refresh(session:Session = Depends(get_session),
                     token:str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY, 
            algorithms = [ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    
    user = session.get(RegisterDetails, user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
    return user