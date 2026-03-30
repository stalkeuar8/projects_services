import bcrypt

from typing import Any

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.settings.database import async_session_factory
from app.repo.hotels_repo import AdminBotHotelRepo
from app.bot.fsm.login_state import LoginState
from app.schemas.auth.hotel_bot_schemas import HotelPasswordSchema, HotelLoginSchema


auth_router = Router()

@auth_router.message(Command('login'))
async def login_bot(message: types.Message, state: FSMContext) -> None:
    await message.answer(text='🏡 Enter hotel id: ')
    await state.set_data(LoginState.hotel_id)
    
    await message.answer(text='Hotel id received! ✅\n\n🎰 Enter password: ')
    await state.set_data(LoginState.password)
    
    received_data: dict[str, Any] = state.get_data()

    hotel_id: int = int(received_data.get("hotel_id"))
    password: str = received_data.get("password")
    chat_id: str = message.chat.id

    login_dto = HotelLoginSchema(hotel_id=hotel_id, chat_id=chat_id)

    async with async_session_factory.begin() as session:
        hotel = await AdminBotHotelRepo.get_hotel_admin_info(hotel_id=hotel_id, session=session)

        if hotel: 
            if bcrypt.checkpw(password.encode("utf-8"), hotel.bot_hashed_password):
                updated_hotel_info = await AdminBotHotelRepo.bot_login(session=session, login_info=login_dto)
        else:
            await message.answer(text="Hotel was not found, try more ❌")