from Async_session import get_session 
from fastapi import Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
import jwt

from database import RegisterDetails
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


async def get_current_user(session:AsyncSession = Depends(get_session),
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