from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine, async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError(
        "can't find the valid database url"
    )


async_engine = create_async_engine(
    DATABASE_URL, pool_size= 5
)

AsyncSessionLocal = async_sessionmaker(
    bind = async_engine , auto_commit = False
)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
        
