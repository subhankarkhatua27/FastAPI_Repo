from fastapi import FastAPI, Depends, File, HTTPException
from Async_session import get_session,async_engine
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from sqlalchemy import select
from database import User,RegisterDetails,File_details
from fastapi import UploadFile
from uuid import uuid4
from check_async_auth import get_current_user
from fastapi.responses import FileResponse
from  Auth_Policy import UserAuthPolicy 



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


@app.post("/uploads")
async def upload_file(session:AsyncSession = Depends(get_session), file : UploadFile = File(...)):
    async with session.begin():
        filename = file.filename
        if filename is None:
            raise HTTPException(
                status_code=400, detail="Filename is missing"
            )
        extention= filename.split(".")[-1]
        secret_file_name = f"{uuid4()}.{extention}"
        
        with open(f"uploads/{secret_file_name}", "ab") as f:
           
            while True:
                chunk = await file.read(1024*1024)
                if chunk is None:
                    break
                
                
                size += len(chunk)
                if size > 5*1024*1024:
                    raise HTTPException(
                        status_code = 400,
                        detail="file size is bigger than 5 MB"
                    )
                f.write(chunk)
            file_detail = File_details(original_name=file.filename, storage_name=f"uploads/{secret_file_name}" )
            session.add(file_detail)
            await session.refresh(file_detail)
    
    
    
    @app.get("/files/{file_id}")
    async def download_file(file_id : int ,current_user:RegisterDetails = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
        async with session.begin():
            file_detail = await session.scalar(select(File_details).where(File_details.file_id == file_id))
            if file_detail is None:
                raise HTTPException(
                    status_code = 400,
                    detail = "No such file exist"
                )
            if not UserAuthPolicy.can_download_file(current_user, file_detail):
                raise HTTPException(
                    status_code = 403,
                    detail = "unauthorized user"
                )
                
            return FileResponse(
                path = file_detail.storage_name,
                filename = file_detail.original_name,
                content_disposition_type="attachment"
            )