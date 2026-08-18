from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    
    username: Mapped[str] = mapped_column(String(40), unique=True)
    email: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))

    liked_repos: Mapped[list["Repository"]] = relationship(
        back_populates="user"
    )


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(primary_key=True)

    url: Mapped[str] = mapped_column(String)
    local_path: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    user: Mapped["User"] = relationship(
        back_populates="liked_repos"
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)

    question_answers: Mapped[list["QuestionAnswer"]] = relationship(
        back_populates="conversation"
    )


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id: Mapped[int] = mapped_column(primary_key=True)

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id")
    )

    question: Mapped[str] = mapped_column(String(500))
    answer: Mapped[str] = mapped_column(String(2000))

    conversation: Mapped["Conversation"] = relationship(
        back_populates="question_answers"
    )


class CodeChunk(Base):
    __tablename__ = "code_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    local_path: Mapped[str] = mapped_column(String(500))
    start_line: Mapped[int] = mapped_column(Integer)
    finish_line: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))

    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id"))