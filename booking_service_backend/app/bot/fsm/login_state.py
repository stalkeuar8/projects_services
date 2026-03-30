from aiogram.fsm.state import StatesGroup, State

class LoginState(StatesGroup):
    hotel_id = State()
    password = State()