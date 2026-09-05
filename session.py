from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
import psycopg

from database import Base
from sqlalchemy import URL
PASSWORD = "subha7363KH@"
database_url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password=PASSWORD,
    host="localhost",
    database="fastapi_app",
)

engine = create_engine(database_url,pool_size = 5)



SessionLocal = sessionmaker(
    bind = engine,
    autocommit=False,)
    

def get_session():
    with SessionLocal() as session:
        yield session
        
        

with engine.begin() as conn:
    Base.metadata.create_all(conn)
    
            