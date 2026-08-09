from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt
import os

# Defining the varibles
SECRET_KEY = os.getenv("SECRET_KEY", "placeholder-key-for-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Defining the functions
def hash_password(user_password: str) -> str:
  return pwd_context.hash(user_password)

def verify_password(plain_password, hashed_password) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
  to_encode = data.copy()

  expire_time = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)

  to_encode.update({
    'exp': expire_time
  })

  return jwt.encode(
    to_encode,
    SECRET_KEY,
    algorithm=ALGORITHM
  )

def decode_access_token(token: str) -> dict: 
  payload = jwt.decode(token,
                       SECRET_KEY,
                       algorithms=[ALGORITHM]
                       )

  return payload