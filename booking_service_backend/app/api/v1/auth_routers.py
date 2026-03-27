from typing import Annotated, Any, Sequence

import bcrypt

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Users
from app.repo.users_repo import UsersRepo
from app.schemas.auth.users_auth_schemas import UserLoginRequestSchema, UserRegisterRequestSchema, UserAuthResponseSchema
from app.settings.database import get_db


auth_router = APIRouter(prefix="/auth", tags=['Authentication'])

@auth_router.post("/login", summary="Login as user", response_model=UserAuthResponseSchema)
async def login(body: UserLoginRequestSchema, session: AsyncSession = Depends(get_db)) -> UserAuthResponseSchema | None:

    user: Users | None = await UsersRepo.find_by_contact_info(session=session, email=body.email, phone_number=body.phone_number)

    if user:
        if user.hashed_password == body.password:
            return UserAuthResponseSchema(email=user.email, phone_number=user.phone_number, id=user.id, is_logined=True, full_name=user.full_name)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User with such contact data was not found")



@auth_router.post("/register", summary="Register as new user", response_model=UserAuthResponseSchema)
async def register(body: UserRegisterRequestSchema, session: AsyncSession = Depends(get_db)) -> UserAuthResponseSchema | None:
    
    new_user: Users | None = await UsersRepo.create(session=session, inserting_data_dto=body)

    if new_user:
        return UserAuthResponseSchema(email=new_user.email, phone_number=new_user.phone_number, id=new_user.id, is_logined=True, full_name=new_user.full_name)

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Back-end server BAD GATEWAY")
