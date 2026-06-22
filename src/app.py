from fastapi import FastAPI,HTTPException,File,UploadFile,Form,Depends
from src.schemas import PostCreate,PostResponse
from src.db import Post,create_db_and_tables ,get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app=FastAPI):
  await create_db_and_tables()
  yield





app=FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...),
    caption:str=Form(""),
    session:AsyncSession=Depends(get_async_session)
):
 post=Post(
    caption=caption,
    url="dummyurl",
    file_type="dummy name"
 )
 session.add(post)
 await session.commit()
 await session.refresh(post)


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