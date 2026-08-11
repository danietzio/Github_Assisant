from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import User, Repo
from schemas import UserCreate, LoginRequest, Token, RepoCreate, UserCreated
from security import (
    hash_password,
    verify_password,
    create_access_token,
)

# User queries
# Sign up user crud request
async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
) -> User:

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


# Login user crud request
async def login_user(
    db: AsyncSession,
    user_data: LoginRequest,
) -> Token:

    query = (
        select(User)
        .where(User.username == user_data.username)
    )

    result = await db.execute(query)

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(
        user_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token({
        "sub": str(user.id),
    })

    return Token(
        access_token=token,
        token_type="bearer",
    )


async def read_user_by_id(
    db: AsyncSession,
    user_id: int
) -> User | None:

    query = (
        select(User)
        .options(selectinload(User.liked_repos))
        .where(User.id == user_id)
    )

    result = await db.execute(query)

    return result.scalar_one_or_none()


# Repo Queries
async def create_repo(
    db: AsyncSession,
    repo_data: RepoCreate,
    user_id: int
) -> Repo:

    new_repo = Repo(
        title=repo_data.title,
        link=repo_data.link,
        user_id=user_id,
    )

    db.add(new_repo)

    await db.commit()
    await db.refresh(new_repo)

    return new_repo

async def read_repo(
    db: AsyncSession,
    repo_id: int
) -> Repo | None:

    query = (
        select(Repo)
        .where(Repo.id == repo_id)
    )

    result = await db.execute(query)

    return result.scalar_one_or_none()