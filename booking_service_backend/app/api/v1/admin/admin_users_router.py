from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Users
from app.repo.users_repo import UsersRepo
from app.schemas.users_schemas import DeletedUserResponseSchema, UsersCreateSchema, UsersListResponseSchema, UsersResponseSchema
from app.settings.database import get_db
from app.auth.jwt_gen import get_current_user, get_current_admin_user
