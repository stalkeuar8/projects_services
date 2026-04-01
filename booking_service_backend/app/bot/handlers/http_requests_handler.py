from datetime import datetime, timedelta, timezone

from aiogram import Bot, Router, types
from aiohttp import web
from fastapi import status

from app.bot.keyboard.inline_buttons import ApprovingResCB, generate_approving_inline_buttons
from app.models.booking import Bookings
from app.models.hotel import HotelAdmins
from app.repo.bookings_repo import AdminBookingsRepo
from app.repo.hotels_repo import AdminBotHotelRepo
from app.schemas.bookings_schemas import BookingStatus
from app.schemas.bot_schemas import BookingApproveProcessSchema
from app.settings.database import async_session_factory
from app.utils.email_sender import send_approving_email

approving_handler_router = Router()


async def handle_external_request(request: web.Request) -> web.Response:
    bot: Bot = request.app.get("bot")

    try:
        body = await request.json()

        data = BookingApproveProcessSchema(**body)
        hotel_id = data.hotel_id

        async with async_session_factory.begin() as session:
            logined_admin_info: HotelAdmins | None = await AdminBotHotelRepo.get_hotel_admin_info(hotel_id=hotel_id, session=session)

            if logined_admin_info:
                chat_id = logined_admin_info.chat_id
                message_to_send = (
                    f"🆕 New booking (Room: {data.booking_info.room_id})\n"
                    f"📅 Dates: {data.booking_info.check_in.date()} — {data.booking_info.check_out.date()}\n\n"
                    f"💰 Total price: {data.booking_info.total_price} 💲\n"
                    f"⌛ Created: {data.booking_info.created_at.strftime('%d.%m %H:%M')}"
                )

                await bot.send_message(
                    chat_id=chat_id,
                    text=message_to_send,
                    reply_markup=generate_approving_inline_buttons(booking_id=data.booking_info.id),
                    parse_mode="html",
                )

                return web.Response(status=200, text="OK")

            else:
                return web.Response(status=status.HTTP_401_UNAUTHORIZED, text="Hotel is not authorized, booking can not be accepted")

    except Exception as e:
        return web.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, text=f"Internal server ERROR: {e}")


@approving_handler_router.callback_query(ApprovingResCB.filter())
async def process_approving_result(callback: types.CallbackQuery, callback_data: ApprovingResCB) -> None:

    if not isinstance(callback.message, types.Message):
        await callback.answer("Error, invalid message")
        return

    async with async_session_factory.begin() as session:
        if callback_data.approving_result == 1:
            max_approving_time = datetime.now(tz=timezone.utc) - timedelta(minutes=15)

            booking: Bookings | None = await AdminBookingsRepo.admin_find_by_id(session=session, booking_id=callback_data.booking_id)

            if booking:
                booking_created_at = booking.created_at
                if booking_created_at < max_approving_time:
                    await callback.message.edit_text(
                        text=f"You run out of approving time limit ⌛\n\nBooking {callback_data.booking_id} has been canceled automatically"
                    )
                    await send_approving_email(result=False, booking_id=callback_data.booking_id)
                    return

            approved_booking: Bookings | None = await AdminBookingsRepo.admin_change_booking_status(
                session=session, booking_id=callback_data.booking_id, new_status=BookingStatus("booked")
            )

            if approved_booking:
                await callback.message.edit_text(text=f"Booking ID: {callback_data.booking_id}\n\nSTATUS: Approved ✅")
                await send_approving_email(result=True, booking_id=callback_data.booking_id)
            else:
                await callback.message.edit_text(text="Error occured, booking will be canceled.")
                await send_approving_email(result=False, booking_id=callback_data.booking_id)

        else:
            async with async_session_factory.begin() as session:
                canceled_booking: Bookings | None = await AdminBookingsRepo.admin_change_booking_status(
                    session=session, booking_id=callback_data.booking_id, new_status=BookingStatus("canceled")
                )

                if canceled_booking:
                    await callback.message.edit_text(text=f"Booking ID: {callback_data.booking_id}\n\nSTATUS: Canceled ❌")

                else:
                    await callback.message.edit_text(text="Error occured, booking will be canceled.")

                await send_approving_email(result=False, booking_id=callback_data.booking_id)
