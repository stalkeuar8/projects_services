from aiogram import F, types, Router

router = Router()

@router.message(F.text == 'Profile')
async def info(message: types.Message):
    await message.answer(f"Your name: {message.from_user.first_name}")