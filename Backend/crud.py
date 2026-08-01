from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models import User, Repo
from schemas import UserCreate, RepoCreate

# 1. Creating User
async def create_user(db: AsyncSession,user_data: UserCreate) -> User :
  new_user = User(username = user_data.username, email = user_data.email)
  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)
  return new_user

# 2. Read Users by id
async def read_user_by_id(db: AsyncSession, user_id: int) -> User | None:
  query = (
    select(User)
    .options(selectinload(User.liked_repos))
    .where(User.id == user_id)
  )

  result = await db.execute(query)
  return result

# 3. Create Repo
async def create_repo(db: AsyncSession, repo_data: RepoCreate) -> Repo :
  new_repo = Repo(title=repo_data.title, link=repo_data.link)
  db.add(new_repo)
  await db.commit()
  await db.refresh(new_repo)
  return new_repo

# Read Repo by id
async def read_repo(db: AsyncSession, id: int) -> Repo | None: 
  query = (
    select(Repo)
    .where(Repo.id == id)
  )

  result = await db.execute(query)
  return result