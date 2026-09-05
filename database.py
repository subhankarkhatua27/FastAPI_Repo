from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column


from sqlalchemy.orm import Mapped
class Base(DeclarativeBase):
    pass 
class User(Base):
    __tablename__="users"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] 
    age : Mapped[int] 

  