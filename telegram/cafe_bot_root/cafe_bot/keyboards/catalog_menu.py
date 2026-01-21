from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from cafe_bot.other_funcs import list_to_str_json


class CoffeeNameCBdata(CallbackData, prefix="coffee_name"):
    category: str

class SizePriceCBdata(CallbackData, prefix="size_price"):
    variant_id: int
    coffee_slug: str

class AddToCartCB(CallbackData, prefix='add to cart'):
    coffee_name: str = None
    variant_id: int = None

class PaymentMenuCB(CallbackData, prefix='payment menu'):
    variant_id: str
    paying_currency_amount: int
    is_cart: bool

class DeleteElCB(CallbackData, prefix='delete last element'):
    user_id: str

class ClearCartCB(CallbackData, prefix='clear cart'):
    user_id: str

class ShowCartCB(CallbackData, prefix="show cart"):
    user_id: str


def generate_menu_catalog_kb(names, slugs):
    builder = InlineKeyboardBuilder()
    for name, slug in zip(names, slugs):
        builder.row(
            InlineKeyboardButton(text=name, callback_data=CoffeeNameCBdata(category=slug).pack())
        )
    return builder.as_markup()

def generate_sizes_prices_kb(variants_list, coffee_slug):
    builder = InlineKeyboardBuilder()
    for i in variants_list:
        builder.row(
            InlineKeyboardButton(text=f"{i[2]} - {i[3]} ml | Price: {i[4]} Uah",
                                 callback_data=SizePriceCBdata(coffee_slug=coffee_slug, variant_id=i[0]).pack())
        )
    builder.row(
        InlineKeyboardButton(text='Back to menu', callback_data="Back to menu")
    )
    return builder.as_markup()


def generate_buying_menu(variant_id: int, coffee_name, coffee_slug, item_price):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Buy now 💸', callback_data=PaymentMenuCB(is_cart=False, paying_currency_amount=item_price, variant_id=list_to_str_json([variant_id])).pack()),
        InlineKeyboardButton(text='Add to cart 🛒', callback_data=AddToCartCB(coffee_name=coffee_name, variant_id=variant_id).pack()),
        InlineKeyboardButton(text='Back to sizes', callback_data=CoffeeNameCBdata(category=coffee_slug).pack()),
        InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')
    )
    builder.adjust(1, 1, 2)
    return builder.as_markup()



def generate_cart_bts(user_id: str, general_price: int, variants_ids: str):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Pay 💸', callback_data=PaymentMenuCB(is_cart=True, paying_currency_amount=general_price, variant_id=variants_ids).pack()))
    builder.row(InlineKeyboardButton(text='Delete last ❌', callback_data=DeleteElCB(user_id=user_id).pack()))
    builder.row(InlineKeyboardButton(text='Clear cart ❌', callback_data=ClearCartCB(user_id=user_id).pack()))
    builder.row(InlineKeyboardButton(text='Back to menu ⬅️', callback_data='Back to menu'))
    builder.adjust(1, 2, 1)
    return builder.as_markup()


def generate_paying_menu_cart_bts(user_id: str):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Cancel payment', callback_data=ShowCartCB(user_id=user_id).pack()))
    return builder.as_markup()

def generate_paying_menu_single_bts(variant_id: int, coffee_slug: str):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Cancel payment', callback_data=SizePriceCBdata(variant_id=variant_id, coffee_slug=coffee_slug).pack()))
    return builder.as_markup()