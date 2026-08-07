from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String)
    lastname: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String(40), unique=True)
    email: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))

    liked_repos: Mapped[list["Repo"]] = relationship(
        back_populates="user"
    )


class Repo(Base):
    __tablename__ = "repos"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(100))
    link: Mapped[str] = mapped_column(String)

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