from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.response_parser import create_user_response
from app.models.user import Users
from app.repo.users_repo import UsersRepo
from app.schemas.users_schemas import DeletedUserResponseSchema, UsersCreateSchema, UsersResponseSchema
from app.settings.database import get_db
from app.auth.jwt_gen import get_current_user

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/me", summary="Get users profile (only logined users)", response_model=UsersResponseSchema)
async def get_users_profile(current_user: Users = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    return create_user_response(current_user)


@users_router.get("/{user_id}", summary="Get all users", response_model=UsersResponseSchema)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)) -> UsersResponseSchema | None:
    user: Users | None = await UsersRepo.find_by_id(session=session, id_to_find=user_id)

    if user:
        return create_user_response(user)

    raise HTTPException(status_code=404, detail=f"Client with id {user_id} was not found")


@users_router.post("/", summary="Create user", response_model=UsersResponseSchema)
async def create_user(body: UsersCreateSchema, session: AsyncSession = Depends(get_db)) -> UsersResponseSchema | None:
    new_user: Users | None = await UsersRepo.create(session=session, inserting_data_dto=body)

    if new_user:
        return create_user_response(new_user)


    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Client not created, Back-end error.")


@users_router.delete("/{user_id}", summary="Delete user by id", response_model=DeletedUserResponseSchema)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db)) -> DeletedUserResponseSchema | None:
    deleted_user: Users | None = await UsersRepo.delete_by_id(id_to_delete=user_id, session=session)

    if deleted_user:
        return create_user_response(delete_user)

    raise HTTPException(status_code=404, detail=f"Client with id {user_id} was not found")
