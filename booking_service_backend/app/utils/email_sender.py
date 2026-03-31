import aiosmtplib
from email.message import EmailMessage
import asyncio
from datetime import datetime, timezone, timedelta

from aiogram import Bot, Router, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from fastapi import status

from app.settings.config import email_settings
from app.models.hotel import HotelAdmins
from app.repo.bookings_repo import AdminBookingsRepo
from app.models.booking import Bookings
from app.models.user import Users
from app.repo.hotels_repo import AdminBotHotelRepo
from app.repo.users_repo import AdminUsersRepo
from app.schemas.bookings_schemas import BookingStatus
from app.schemas.bot_schemas import BookingApproveProcessSchema, BookingApproveRequestSchema, BookingApproveResponseSchema
from app.settings.database import async_session_factory

from app.bot.keyboard.inline_buttons import generate_approving_inline_buttons, ApprovingResCB


async def send_approving_email(result: bool, booking_id: int) -> None:

    async with async_session_factory.begin() as session:
        booking: Bookings | None = await AdminBookingsRepo.admin_find_by_id(session=session, booking_id=booking_id)

        if booking:

            user: Users | None = await AdminUsersRepo.admin_find_by_id(session=session, id_to_find=booking.user_id)

            if user:
                user_email = user.email

            else:
                return
    
        else:
            return
        

    message = EmailMessage()
    message['From'] = email_settings.EMAIL
    message['To'] = user_email
    message['Subject'] = f"Booking Request Results 🏡"

    if result:
        message.set_content(f"Your booking request (№{booking_id}) has been approved! ✅\n\nWe are waiting for you! ⌛")

    else:
        message.set_content(f"Your booking request (№{booking_id}) has been rejected! ❌\n\nReason: Hotel personal reasons. Please, try later. ⌛")


    try:

        await aiosmtplib.send(
            message,
            hostname="smtp.gmail.com",
            port=465,
            use_tls=True,
            username=email_settings.EMAIL,
            password=email_settings.PASSWORD
        )

    except Exception as e:
        print(f"Email sending error: {e}")