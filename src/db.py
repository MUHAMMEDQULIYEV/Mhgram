from collections.abs import AsyncGenerator
import uuid
from sqlalchemy import Column,String ,Text,DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import DeclarativeBase,relationship
import datetime

DATABASE_URL="sqlite+aiolite:///./test.db"



class Post(DeclarativeBase):

    __tablename__="posts"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    caption=Column(Text)
    url=Column(String,nullable=True)
    file_type=Column(String,nullable=True)
    file_name=Column(String,nullable=True)
    created_at=Column(DateTime,nullable=datetime.utcnow)


engine=create_async_engine(DATABASE_URL)
async_session_maker=async_session_maker(engine,expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)