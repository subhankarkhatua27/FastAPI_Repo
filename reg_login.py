from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta
password_hash = PasswordHash.recommended()

def hash_generator(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

def generate_jwt_token(user_id: int, secret_key: str|None, algorithm: str | None):
    payload = {
        "sub": user_id,
        "exp": datetime.now()+ timedelta(minutes=30)
        
    }
    
    return jwt.encode(payload, secret_key, algorithm)