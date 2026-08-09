from pydantic import BaseModel, ConfigDict, Field


class RepoBase(BaseModel):
    title: str
    link: str


class RepoCreate(RepoBase):
    pass


class RepoRead(RepoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    liked_repos: list[RepoRead] = Field(
        default_factory=list
    )


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str