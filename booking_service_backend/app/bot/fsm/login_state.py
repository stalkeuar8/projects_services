from aiogram.fsm.state import State, StatesGroup


class LoginState(StatesGroup):
    hotel_id = State()
    password = State()
