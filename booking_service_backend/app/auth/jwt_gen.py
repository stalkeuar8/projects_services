from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Users
from app.repo.users_repo import AdminUsersRepo
from app.settings.config import jwt_settings
from app.settings.database import get_db

SECRET_KEY = jwt_settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
oauth2_scheme = OAuth2PasswordBearer("/auth/login")


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"sub": str(user_id), "exp": expires_at}

    encoded_jwt = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_jwt(jwt_token: str) -> dict[str, Any]:

    try:
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")


async def get_current_user(jwt_token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> Users:
    payload = decode_jwt(jwt_token=jwt_token)

    user_id = payload.get("sub", None)

    if user_id:
        user: Users | None = await AdminUsersRepo.admin_find_by_id(id_to_find=int(user_id), session=session)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT Auth error, can not find user")

        return user

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT Auth error, Could not validate credentials")


async def get_current_admin_user(current_user: Users = Depends(get_current_user)) -> Users:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Method not allowed for users (Admin only)")

    return current_user
