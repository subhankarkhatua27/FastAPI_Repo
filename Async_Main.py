from fastapi import FastAPI, Depends, HTTPException
from Async_session import get_session,async_engine
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy import select
from database import User



from contextlib import asynccontextmanager

from database import Base

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
         
app = FastAPI(lifespan=lifespan)

@app.get("/users/{user_id}")
async def get_user_data(session :AsyncSession = Depends(get_session), user_id:int = 1):
    async with session.begin():
        result= await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user


