from datetime import datetime, timezone

import bcrypt
import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_gen import create_access_token, decode_jwt, oauth2_scheme
from app.models.user import Users
from app.repo.users_repo import AdminUsersRepo
from app.schemas.auth.users_auth_schemas import (
    RefreshTokenRequestSchema,
    RefreshTokenResponseSchema,
    UserAuthResponseSchema,
    UserLoginRequestSchema,
    UserRegisterRequestSchema,
)
from app.schemas.users_schemas import UsersCreateSchema
from app.settings.database import get_db
from app.settings.redis import get_redis

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", summary="Login as user", response_model=UserAuthResponseSchema)
async def login(body: UserLoginRequestSchema, session: AsyncSession = Depends(get_db)) -> UserAuthResponseSchema | None:

    user: Users | None = await AdminUsersRepo.admin_find_by_contact_info(session=session, email=body.email, phone_number=body.phone_number)

    if user:
        if bcrypt.checkpw(body.password.encode("utf-8"), user.hashed_password):
            jwt_token = create_access_token(user_id=user.id)

            return UserAuthResponseSchema(
                email=user.email,
                phone_number=user.phone_number,
                id=user.id,
                is_logined=True,
                full_name=user.full_name,
                jwt_token=jwt_token,
                role=user.role,
            )
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User with such contact data was not found")


@auth_router.post("/register", summary="Register as new user", response_model=UserAuthResponseSchema)
async def register(body: UserRegisterRequestSchema, session: AsyncSession = Depends(get_db)) -> UserAuthResponseSchema | None:
    new_user_dto = UsersCreateSchema(full_name=body.full_name, phone_number=body.phone_number, email=body.email, hashed_password=body.hashed_password)

    new_user: Users | None = await AdminUsersRepo.create(session=session, inserting_data_dto=new_user_dto)

    if new_user:
        jwt_token = create_access_token(user_id=new_user.id)

        return UserAuthResponseSchema(
            email=new_user.email,
            phone_number=new_user.phone_number,
            id=new_user.id,
            is_logined=True,
            full_name=new_user.full_name,
            jwt_token=jwt_token,
            role=new_user.role,
        )

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Back-end server BAD GATEWAY")


@auth_router.post("/logout", summary="Logout", response_model=JSONResponse)
async def logout(jwt_token: str = Depends(oauth2_scheme), redis_session: redis.Redis = Depends(get_redis)) -> JSONResponse:

    payload = decode_jwt(jwt_token=jwt_token)

    jti = payload.get("jti", None)

    if jti is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token, JTI not found")
    
    exp = payload.get("exp", None)

    if exp is not None:

        current_time_seconds = int(datetime.now(tz=timezone.utc).timestamp())
        time_left = exp - current_time_seconds

        if time_left > 0:
            await redis_session.set(f"blacklist:{jti}", "1", ex=time_left)

        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Successfull log out"})

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error while logging out, expiration time was not found")


@auth_router.post("/refresh", summary="Refresh token", response_model=RefreshTokenResponseSchema)
async def refresh(request: RefreshTokenRequestSchema, redis_session: redis.Redis = Depends(get_redis)) -> RefreshTokenResponseSchema:

    try:
        payload = decode_jwt(request.refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

        sub = payload.get("sub")
        if sub:
            user_id = int(sub)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id was not found in Payload")

    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired or invalid token type")

    stored_token = await redis_session.get(f"refresh:{user_id}")

    if not stored_token or stored_token != request.refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    new_access_token = create_access_token(int(user_id))

    return RefreshTokenResponseSchema(access_token=new_access_token, type="bearer")
