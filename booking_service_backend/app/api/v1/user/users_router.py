from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_gen import get_current_user
from app.models.user import Users
from app.schemas.users_schemas import UsersResponseSchema
from app.settings.database import get_db

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/me", summary="Get users profile (only logined users)", response_model=UsersResponseSchema)
async def get_users_profile(current_user: Users = Depends(get_current_user), session: AsyncSession = Depends(get_db)) -> UsersResponseSchema:
    return UsersResponseSchema.model_validate(current_user)
