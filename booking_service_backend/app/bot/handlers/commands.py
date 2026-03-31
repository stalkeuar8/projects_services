from typing import Sequence

from aiogram import F, Router, types
from aiogram.filters import Command, CommandObject

from app.models.booking import Bookings
from app.repo.bookings_repo import AdminBookingsRepo
from app.repo.hotels_repo import AdminBotHotelRepo
from app.settings.database import async_session_factory

commands_router = Router()


@commands_router.message(Command("start"))
async def start_response(message: types.Message) -> None:
    await message.answer(text="hello")


@commands_router.message(Command("bookings"))
async def current_hotel_bookins(message: types.Message, command: CommandObject) -> None:
    chat_id = str(message.chat.id)

    limit = 10

    if command.args:
        try:
            limit = int(command.args.split(" ")[0])
            await message.answer(text=f"num: {str(limit)}, type: {type(limit)}")
        except Exception:
            await message.answer(text=f"Wrong command args, must be a number (Used the default = 10)")

    async with async_session_factory.begin() as session:
        hotel = await AdminBotHotelRepo.get_hotel_info_by_chat_id(chat_id=chat_id, session=session)

        hotel_bookings: Sequence[Bookings] | None = None

        if hotel is not None:
            hotel_bookings = await AdminBookingsRepo.admin_find_by_hotel_id(hotel_id=hotel.hotel_id, session=session, limit=limit)

        else:
            await message.answer(text="You are not logined, you can not check bookings.")
            return

    if hotel_bookings:
        for booking in hotel_bookings:
            await message.answer(
                text=f"ID: {booking.id}, Room id: {booking.room_id}, total price: {booking.total_price}, STATUS: {booking.status}, created at: {booking.created_at}"
            )
        return

    else:
        await message.answer(text="No bookings found")
        return
