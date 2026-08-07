from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post(
    "/users/",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.create_user(db, user_in)

    return user