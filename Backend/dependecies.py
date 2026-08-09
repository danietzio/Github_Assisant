from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from security import decode_access_token
from crud import read_user_by_id

from fastapi import HTTPException, status
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):

  credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="user is not authorized",
    headers={"WWWW-Authenticate": "Bearer"},
  )

  try: 
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if user_id is None:
      raise credential_exception

    user_id = int(user_id)

  except(JWTError, ValueError, TypeError):
    raise credential_exception

  user = await read_user_by_id(db, user_id)

  if user is None:
    raise credential_exception

  return user

  
