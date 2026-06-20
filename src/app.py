from fastapi import FastAPI,HTTPException
from src.schemas import PostCreate,PostResponse
from src.db import Post,create_db_and_tables ,get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app=FastAPI):
  await create_db_and_tables()
  yield





app=FastAPI(lifespan=lifespan)

text_post = {
    1: "Hello this is text message",
    2: "Heyyo nasilsin adamim",
    3: "사랑한대 연새",
    4: "Just grabbing a coffee and getting ready to code.",
    5: "Bugün hava gerçekten çok güzel, dışarı çıkmak lazım.",
    6: "한국어 공부는 진짜 재미있지만 문법이 조금 어려워요.",
    7: "Does anyone know the best way to handle async uploads in FastAPI?",
    8: "Ne yaparsan yap, aşk ile yap!",
    9: "오늘도 좋은 하루 보내세요! 파이팅!",
    10: "Finally fixed that stubborn memory leak. Time to celebrate!"
}

@app.get("/posts")
def get_all_post(limit:int=None):
    if limit:
     return list(text_post.values())[:limit]
    return text_post



@app.get("/post/{id}")
def get_specific_post(id:int):
    if id not in text_post:
        raise HTTPException(status_code=404,detail="Post not found")
    else:
     return text_post.get(id)
     

@app.post("/posts")
def create_post(post: PostCreate)->PostResponse:
    # 1. Calculate the next available ID number
    new_id = max(text_post.keys()) + 1
    
    # 2. Save the incoming content to your dictionary
    text_post[new_id] = post.content
    
    # 3. Return the newly created item so the user knows it worked
    return {"id": new_id, "post": text_post[new_id]}