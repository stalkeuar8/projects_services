from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Users
from app.repo.users_repo import UsersRepo
from app.schemas.users_schemas import UsersCreateSchema, DeletedUserResponseSchema, UsersListResponseSchema, UsersResponseSchema
from app.settings.database import get_db

users_router = APIRouter(prefix="/users", tags=["Users"])




@users_router.get("/{user_id}", summary="Get all users", response_model=UsersResponseSchema)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)) -> UsersResponseSchema | None:
    user: Users | None = await UsersRepo.find_by_id(session=session, id_to_find=user_id)

    if user:
        return UsersResponseSchema(id=user.id, full_name=user.full_name, phone_number=user.phone_number, email=user.email)

    raise HTTPException(status_code=404, detail=f"Client with id {user_id} was not found")


@users_router.post("/", summary="Create user", response_model=UsersResponseSchema)
async def create_user(body: UsersCreateSchema, session: AsyncSession = Depends(get_db)) -> UsersResponseSchema | None:
    new_user: Users | None = await UsersRepo.create(session=session, inserting_data_dto=body)

    if new_user:
        return UsersResponseSchema(id=new_user.id, full_name=new_user.full_name, phone_number=new_user.phone_number, email=new_user.email)

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Client not created, Back-end error.")


@users_router.delete("/{user_id}", summary="Delete user by id", response_model=DeletedUserResponseSchema)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db)) -> DeletedUserResponseSchema | None:
    deleted_user: Users | None = await UsersRepo.delete_by_id(id_to_delete=user_id, session=session)

    if deleted_user:
        return DeletedUserResponseSchema(
            id=deleted_user.id, full_name=deleted_user.full_name, phone_number=deleted_user.phone_number, email=deleted_user.email, is_deleted=True
        )

    raise HTTPException(status_code=404, detail=f"Client with id {user_id} was not found")
