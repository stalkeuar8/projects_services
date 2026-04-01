from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_gen import get_current_admin_user
from app.models.user import Users
from app.repo.users_repo import AdminUsersRepo
from app.schemas.users_schemas import UsersCreateSchema, UsersResponseSchema, UserStatsResponseSchema
from app.settings.database import get_db

admin_users_router = APIRouter(prefix="/admin/users", tags=["Admin"], dependencies=[Depends(get_current_admin_user)])


@admin_users_router.post("/", summary="Create user (Admin)", response_model=UsersResponseSchema)
async def admin_create_user(body: UsersCreateSchema, session: AsyncSession = Depends(get_db)) -> UsersResponseSchema:
    new_user: Users | None = await AdminUsersRepo.create(session=session, inserting_data_dto=body)

    if new_user:
        return UsersResponseSchema.model_validate(new_user)

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="User not created, Back-end error.")


@admin_users_router.delete("/{user_id}", summary="Delete user by id (Admin)", response_model=UsersResponseSchema)
async def admin_delete_user(user_id: int, session: AsyncSession = Depends(get_db)) -> UsersResponseSchema:
    deleted_user: Users | None = await AdminUsersRepo.admin_delete_by_id(id_to_delete=user_id, session=session)

    if deleted_user:
        return UsersResponseSchema.model_validate(deleted_user)

    raise HTTPException(status_code=404, detail=f"User with id {user_id} was not found")


@admin_users_router.get("/{user_id}", summary="Get user by id (Admin)", response_model=UsersResponseSchema)
async def admin_get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)) -> UsersResponseSchema:
    user: Users | None = await AdminUsersRepo.admin_find_by_id(session=session, id_to_find=user_id)

    if user:
        return UsersResponseSchema.model_validate(user)

    raise HTTPException(status_code=404, detail=f"User with id {user_id} was not found")


@admin_users_router.get("/{user_id}/bookings", summary="Get users bookings (Admin)", response_model=UserStatsResponseSchema)
async def admin_get_user_stats(user_id: int, session: AsyncSession = Depends(get_db)) -> UserStatsResponseSchema:
    users_stats: UserStatsResponseSchema | None = await AdminUsersRepo.admin_get_users_stats(user_id=user_id, session=session)

    if users_stats:
        return users_stats

    raise HTTPException(status_code=404, detail=f"User with id {user_id} was not found")
