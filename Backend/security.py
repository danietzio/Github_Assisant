from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt

# Later change to os.getenv("SECRET_KEY")
SECRET_KEY = "abc123xyz"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

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

  token = jwt.encode(
    to_encode,
    SECRET_KEY,
    algorithm=ALGORITHM
  )

  return token
