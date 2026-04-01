from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class ApprovingResCB(CallbackData, prefix="appres"):
    booking_id: int
    approving_result: int


def generate_approving_inline_buttons(booking_id: int) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="Approve ✅", callback_data=ApprovingResCB(booking_id=booking_id, approving_result=1).pack()),
        InlineKeyboardButton(text="Reject ❌", callback_data=ApprovingResCB(booking_id=booking_id, approving_result=0).pack()),
    )

    builder.adjust(2)

    return builder.as_markup()
