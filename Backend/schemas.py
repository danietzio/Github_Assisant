from pydantic import BaseModel, ConfigDict, Field


class RepositoryCreate(BaseModel):
    url: str


class RepositoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    status: str


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str

class UserCreated(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    liked_repos: list[RepositoryRead] = Field(
        default_factory=list
    )


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str