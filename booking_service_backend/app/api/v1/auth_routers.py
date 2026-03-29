from typing import Annotated, Any, Sequence

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_gen import create_access_token
from app.models.user import Users
from app.repo.users_repo import UsersRepo, AdminUsersRepo
from app.schemas.auth.users_auth_schemas import UserAuthResponseSchema, UserLoginRequestSchema, UserRegisterRequestSchema
from app.schemas.users_schemas import UsersCreateSchema
from app.settings.database import get_db

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", summary="Login as user", response_model=UserAuthResponseSchema)
async def login(body: UserLoginRequestSchema, session: AsyncSession = Depends(get_db)) -> UserAuthResponseSchema | None:

    user: Users | None = await AdminUsersRepo.admin_find_by_contact_info(session=session, email=body.email, phone_number=body.phone_number)

    if user:
        if bcrypt.checkpw(body.password.encode("utf-8"), user.hashed_password):
            jwt_token = create_access_token(user_id=user.id)

            return UserAuthResponseSchema(
                email=user.email, phone_number=user.phone_number, id=user.id, is_logined=True, full_name=user.full_name, jwt_token=jwt_token, role=user.role
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
            role=new_user.role
        )

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Back-end server BAD GATEWAY")
