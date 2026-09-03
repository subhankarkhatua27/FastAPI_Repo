from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import psycopg

PASSWORD = "subha7363KH@"
engine =create_engine(f"postgresql+psycopg://postgres:{PASSWORD}@localhost/fastapi_app")  

SessionLocal = sessionmaker(
    bind = engine,
    pool_size = 5 )
    

def get_session():
    with SessionLocal() as session:
        yield session
        
        
        