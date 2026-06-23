from fastapi import FastAPI,HTTPException,File,UploadFile,Form,Depends
from src.schemas import PostCreate,PostResponse
from src.db import Post,create_db_and_tables ,get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager
from src.images import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import tempfile
import uuid
@asynccontextmanager
async def lifespan(app=FastAPI):
  await create_db_and_tables()
  yield





app=FastAPI(lifespan=lifespan)


@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        caption: str = Form(""),
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        upload_result = imagekit.upload_file(
            file=open(temp_file_path, "rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )

        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                user_id=user.id,
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()


@app.get("/feed")
async def get_feed(session:AsyncSession=Depends(get_async_session)):
  result= await session.execute(select(Post).order_by(Post.created_at.desc()))
  post= [row[0] for row in result.all()]
  post_data=[]
  for post in post:
    post_data.append({
        "id":str(post.id),
        "caption":post.caption,
        "url":post.url,
        file_type:post.file_type,
        file_name:post.file_name,
        created_at:post.create_at.isformat()
    })
    return {"posts":post_data}