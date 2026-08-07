from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import User, Repo
from schemas import UserCreate, RepoCreate


async def create_user(
    db: AsyncSession,
    user_data: UserCreate
) -> User:

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        name="",
        lastname="",
    )

    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


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