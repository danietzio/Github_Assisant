from pydantic import BaseModel, ConfigDict, Field

class RepoRead(BaseModel):
    model_config = ConfigDict(from_attributes= True)

    id: int
    title: str
    link: str

class RepoCreate(RepoRead):
    pass

# User Models
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    pass

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    liked_repos: list[RepoRead] = Field(default_factory=list)


# Login Model
class LoginRequest(BaseModel):
    username: str
    password: str

# Token Model
class Token(BaseModel):
    access_token: str
    token_type: str
