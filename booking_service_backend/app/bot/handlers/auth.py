from typing import Any

import bcrypt
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.bot.fsm.login_state import LoginState
from app.models.hotel import HotelAdmins
from app.repo.hotels_repo import AdminBotHotelRepo
from app.schemas.auth.hotel_bot_schemas import HotelLoginSchema
from app.settings.database import async_session_factory

auth_router = Router()


@auth_router.message(Command("login"))
async def login_bot(message: types.Message, state: FSMContext) -> None:
    async with async_session_factory.begin() as session:
        admin_info: HotelAdmins | None = await AdminBotHotelRepo.get_hotel_info_by_chat_id(chat_id=str(message.chat.id), session=session)

        if admin_info is not None:
            await message.answer(text=f"You are already logined as admin of hotel {admin_info.hotel_id}\n\nLog out to login one more time. ❌")
            return

    await message.answer(text="🏡 Enter hotel id: ")
    await state.set_state(LoginState.hotel_id)


@auth_router.message(LoginState.hotel_id)
async def process_hotel_id(message: types.Message, state: FSMContext) -> None:
    await state.update_data(hotel_id=message.text)

    await message.answer(text="Hotel id received! ✅\n\n🎰 Enter password: ")
    await state.set_state(LoginState.password)


@auth_router.message(LoginState.password)
async def process_password(message: types.Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)

    received_data: dict[str, Any] = await state.get_data()

    hotel_id: int = int(received_data.get("hotel_id"))
    password: str = received_data.get("password")
    chat_id: str = str(message.chat.id)

    login_dto = HotelLoginSchema(hotel_id=hotel_id, chat_id=chat_id)

    await state.clear()

    async with async_session_factory.begin() as session:
        hotel = await AdminBotHotelRepo.get_hotel_admin_info(hotel_id=hotel_id, session=session)

        if hotel:
            if hotel.chat_id:
                await message.answer(text="Log out from another device, only one admin session is allowed ❌")

            else:
                if bcrypt.checkpw(password.encode("utf-8"), hotel.bot_hashed_password):
                    await AdminBotHotelRepo.bot_login(session=session, login_info=login_dto)
                    await message.answer(text=f"Successfully logined by hotel {hotel_id} ✅")

                else:
                    await message.answer(text="Wrong password provided. Access Denied ❌")
        else:
            await message.answer(text="Hotel was not found, try more ❌")


@auth_router.message(Command("logout"))
async def bot_logout(message: types.Message) -> None:
    chat_id = str(message.chat.id)

    async with async_session_factory.begin() as session:
        hotel_info: HotelAdmins | None = await AdminBotHotelRepo.get_hotel_info_by_chat_id(chat_id=chat_id, session=session)

        if hotel_info is not None:
            hotel_admin: HotelAdmins | None = await AdminBotHotelRepo.bot_logout(session=session, hotel_id=hotel_info.hotel_id)

        else:
            await message.answer("You are not logined, you can not logout. ❌")

    if hotel_admin is not None:
        await message.answer("Logout successful! ✅")

    else:
        await message.answer("Error. Hotel was not found. 📛")
