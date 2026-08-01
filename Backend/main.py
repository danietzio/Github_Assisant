from contextlib import asynccontextmanager
from database import Base, engine, get_df
from fastapi import FastAPI, status
import schemas
import crud
from sqlalchemy.ext.asyncio import AsyncSession

# Let's create our Tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


# Defining the API
@app.post("/users/", response_class=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
  user_in: schemas.UserCreate,
  db: AsyncSession = Depends(get_df())
):
  user = await crud.create_user(db, user_in)
  return user




  