from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class User(Base):
  __tablename__ = 'user'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String)
  lastname: Mapped[str] = mapped_column(String)
  username: Mapped[str] = mapped_column(String(40), unique=True)
  email: Mapped[str] = mapped_column(String(100))

  liked_repos: Mapped[List["Repo"]]

class Repo(Base):
  __tablename__ = 'repo'

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(100))
  link: Mapped[str] = mapped_column(String)

  followers: Mapped[List[User]]

  