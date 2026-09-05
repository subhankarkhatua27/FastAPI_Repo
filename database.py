from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column

from enum import Enum
from sqlalchemy import Enum as saenum

class ProductCategory(str,Enum):
    CLOTHES = "clothing"
    TOYS = "toys"
    CAR = "cars"
    BIKE ="bikes"

from sqlalchemy.orm import Mapped
class Base(DeclarativeBase):
    pass 
class User(Base):
    __tablename__="users"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] 
    age : Mapped[int]
    role : Mapped[str] = mapped_column(default = "user")
     

class Product(Base):
    __tablename__ = "products"
    
    prod_id : Mapped[int] = mapped_column(primary_key = True)
    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    category : Mapped[ProductCategory] = mapped_column(
                                        saenum(ProductCategory),
                                        nullable = False
                                    )