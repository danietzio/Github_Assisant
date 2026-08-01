from pydantic import BaseModel, ConfigDict

# -- post schemas --
class RepoBase(BaseModel):
  title: str
  link: str

class RepoCreate(RepoBase):
  pass

class RepoRead(RepoBase):
  id: int
  user_id: int

  model_config: ConfigDict(from_attributes=True)

# -- User Schemas --
class UserBase(BaseModel):
  username: str
  email: str

class UserCreate(UserBase):
  pass

class UserRead(UserBase):
  id: int
  liked_repos: list[RepoRead] = []

  model_config = ConfigDict(from_attributes=True)