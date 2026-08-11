from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import Base, engine, get_db

from dependecies import get_current_user
from models import User

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

# Registration Process
@app.post("/auth/signup",response_model=schemas.UserCreated,status_code=status.HTTP_201_CREATED)

async def create_user_endpoint(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await crud.create_user(db, user_in)

    return user

# Login Process
@app.post("/auth/login", response_model=schemas.Token, status_code=status.HTTP_200_OK)

async def login_user_endpoint(
    user_in: schemas.LoginRequest,
    db: AsyncSession = Depends(get_db),
):

    token = await crud.login_user(db, user_in)

    return token

@app.get("/users/get", response_model=schemas.UserRead, status_code=status.HTTP_200_OK)

async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user