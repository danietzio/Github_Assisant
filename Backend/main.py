from datetime import date
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from typing import Annotated, List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# We are going to have users with name, email, data of birth, github repo and github for logging in
# Learn the whole checking thing
class userBase(BaseModel):
  name: str
  lastname: str
  github_username: str # How to check if its real username before putting it in the databse
  data_birth: date


def get_db():
  db = SessionLocal()
  try: 
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# Defining the API
@app.post("/users/")
async def create_users(user: userBase, db: db_dependency):
  db_user = models.Users(name=user.name, lastname=user.lastname, github_username=user.github_username, date_birth=user.data_birth)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)


  