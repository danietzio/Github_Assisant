# This file is for connecting the enginge to the databse and using it later
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
  create_async_engine,
  async_sessionmaker,
  AsyncSession
)
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

URL_DATABASE = "postgresql+asyncpg://daniyal:12345!@localhost:5432/users"

engine = create_async_engine(URL_DATABASE, echo=True)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)

# Defining the base class for SQLAlchemy models
class Base(DeclarativeBase):
  pass

async def get_df() -> AsyncGenerator[AsyncSession, None]:
  async with AsyncSessionLocal() as session:
    yield session