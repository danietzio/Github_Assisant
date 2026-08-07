from pydantic import BaseModel, ConfigDict, Field


class RepoBase(BaseModel):
    title: str
    link: str


class RepoCreate(RepoBase):
    pass


class RepoRead(RepoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    liked_repos: list[RepoRead] = Field(default_factory=list)