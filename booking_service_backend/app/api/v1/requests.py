import asyncio

import aiohttp
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.models.hotel import Rooms
from app.repo.rooms_repo import AdminRoomsRepo
from app.schemas.bookings_schemas import BookingsResponseSchema
from app.schemas.bot_schemas import BookingApproveRequestSchema, BookingApproveResponseSchema
from app.settings.database import async_session_factory


async def send_approving_request(booking_info: BookingsResponseSchema):
    url = "https://5a45-195-211-138-69.ngrok-free.app/external-data"

    async with async_session_factory.begin() as session:
        room_info: Rooms = await AdminRoomsRepo.admin_find_by_id(id_to_find=booking_info.room_id, session=session)

        hotel_id = room_info.hotel_id

    booking_req_obj = BookingApproveRequestSchema(booking_info=booking_info, hotel_id=hotel_id)

    async with aiohttp.ClientSession() as session:
        body = jsonable_encoder(booking_req_obj)

        try:
            async with session.post(url=url, json=body, timeout=10) as response:
                status = response.status

                return status

        except aiohttp.ClientError as e:
            return None
