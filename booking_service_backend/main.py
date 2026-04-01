from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.api.v1.admin.admin_bookings_router import admin_bookings_router
from app.api.v1.admin.admin_hotels_router import admin_hotels_router
from app.api.v1.admin.admin_rooms_router import admin_rooms_router
from app.api.v1.admin.admin_users_router import admin_users_router
from app.api.v1.user.auth_routers import auth_router
from app.api.v1.user.bookings_router import bookings_router
from app.api.v1.user.hotels_router import hotels_router
from app.api.v1.user.rooms_router import rooms_router
from app.api.v1.user.users_router import users_router
from app.settings.database import async_engine

# START FUNCS, ROUTERS


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    yield
    await async_engine.dispose()


def create_app() -> FastAPI:

    app = FastAPI(title="Booking Service", lifespan=lifespan)

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(bookings_router)
    app.include_router(hotels_router)
    app.include_router(rooms_router)
    app.include_router(admin_bookings_router)
    app.include_router(admin_hotels_router)
    app.include_router(admin_rooms_router)
    app.include_router(admin_users_router)

    return app


app = create_app()


@app.exception_handler(IntegrityError)
async def handle_integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
    error_msg = str(exc.orig)

    error_details = "Error caused becuase "

    if "phone_number" in error_msg:
        error_details += "'phone_number' "
    if "email" in error_msg:
        error_details += "'email' "
    error_details += " already exists, must be unique"

    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"error_msg": error_msg, "details": error_details})
