import datetime
import asyncio
from aiohttp import web

from fastapi import status
from aiogram import Router, Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.schemas.bot_schemas import BookingApproveRequestSchema, BookingApproveResponseSchema, BookingApproveProcessSchema
from app.repo.hotels_repo import AdminBotHotelRepo
from app.repo.bookings_repo import AdminBookingsRepo
from app.settings.database import async_session_factory
from app.models.hotel import HotelAdmins


async def handle_external_request(request: web.Request) -> None:
    bot: Bot = request.app.get("bot")

    try:
        body = await request.json()

        data = BookingApproveProcessSchema(**body)
        hotel_id = data.hotel_id
        
        with async_session_factory.begin() as session:
            logined_admin_info: HotelAdmins | None = await AdminBotHotelRepo.get_hotel_admin_info(hotel_id=hotel_id, session=session)

            if logined_admin_info:
                chat_id = logined_admin_info.chat_id
                message_to_send = (
                    f"🆕 New booking (Room: {data.booking_info.room_id})\n"
                    f"📅 Dates: {data.booking_info.check_in.date()} — {data.booking_info.check_out.date()}\n\n"
                    f"💰 Total price: {data.booking_info.total_price} 💲\n"
                    f"⌛ Created: {data.booking_info.created_at.strftime('%d.%m %H:%M')}"
                )

                # message_to_send = f"New booking request! 🏡\n\nRoom ID: {data.booking_info.room_id}\nCheck in date: {datetime.date(data.booking_info.check_in)}\nCheck out date: {datetime.date(data.booking_info.check_out)}\n\nTotal price: {data.booking_info.total_price} 💲\nCreated at: {data.booking_info.created_at} ⌛"
                bot.send_message(chat_id=chat_id, text=message_to_send)

            else:
                return web.Response(status=status.HTTP_401_UNAUTHORIZED, text="Hotel is not authorized, booking can not be accepted")

    except Exception:
        return web.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, text=f"Internal server ERROR")


