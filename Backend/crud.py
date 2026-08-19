from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import User, Repository, CodeChunk
from schemas import UserCreate, LoginRequest, Token, RepositoryCreate, UserCreated
from security import (
    hash_password,
    verify_password,
    create_access_token,
)

import subprocess, sys, os
from pathlib import Path
from ingestion.chunker import chunk_repository
from ingestion.embedder import local_embedder
from mind import generate_answer

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
async def create_repository(
    db: AsyncSession,
    repo_data: RepositoryCreate,
    user_id: int
) -> Repository:

    query = (
        select(Repository)
        .where(Repository.id == user_id,
               Repository.url == repo_data.url)
    )

    result = await db.execute(query)

    existing_repo = result.scalar_one_or_none()

    if(existing_repo):
        return existing_repo
    
    new_repo = Repository(
        url=repo_data.url,
        local_path="",
        status="pending",
        user_id=user_id,
    )

    db.add(new_repo)

    await db.commit()
    await db.refresh(new_repo)


    # Adding Repository to Folders
    # For clonning, I would like to later think about people who have some access to private repos, and # they want to clone them, but if they want to clone them, they should authintcate with their github
    # if not, it will not show the repos
    #username_github = os.getenv("GITHUB_USER")

    repository_id = new_repo.id
    storage_destination = Path("/app/storage/repositories") / str(repository_id)
    storage_destination.mkdir(parents=True, exist_ok=True)

    new_repo.local_path = str(storage_destination)

    result = subprocess.run(["git", "clone", "--depth", "1", repo_data.url, str(storage_destination)], text=True, capture_output= True)

    if result.returncode == 0:
        new_repo.status = "ready"
        await chunk_repository(db, new_repo)

    else:
        new_repo.status = "failed"
        
    await db.commit()
    await db.refresh(new_repo)

    return new_repo

async def read_repository(
    db: AsyncSession,
    repo_id: int
) -> Repository | None:

    query = (
        select(Repository)
        .where(Repository.id == repo_id)
    )

    result = await db.execute(query)

    return result.scalar_one_or_none()


async def answer_question(
        db: AsyncSession,
        question: str
) -> str:

    question_embedding = local_embedder(question)    

    query = (
        select(CodeChunk)
        .order_by(
          CodeChunk.embedding.cosine_distance(question_embedding)
        )
        .limit(5)
    )

    result = await db.execute(query)
    chunks = result.scalars().all()

    chunks = sorted(chunks, key= lambda chunk: (chunk.local_path, chunk.start_line))

    context = "\n\n".join(
        f"File: {chunk.local_path}\n"
        f"lines: {chunk.start_line}-{chunk.finish_line}\n"
        f"{chunk.content}"
        for chunk in chunks
    )

    prompt = f"""
    You are a code review assistant, 

    Answer the user's question using the provided code context.local_embedder

    Code Context:
    {context}

    user's Question:
    {question}
    """
    # Where we write the prompt, add the query results and question, and ask ai to answer

    respone = generate_answer(prompt)
