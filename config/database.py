from .settings import DATABASE_URL, DB_ECHO
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator



engine = create_async_engine(DATABASE_URL, echo=DB_ECHO)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session :
        yield session

class Base(DeclarativeBase):
    pass