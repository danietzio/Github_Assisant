from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Users(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  lastname = Column(String)
  github_username = Column(String)
  date_birth = Column(Date)

  