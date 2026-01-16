from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from cafe_bot.other_funcs import json_update, json_reader

path = r'D:\coding\python\telegram\cafe_bot\general_info.json'

class CoffeeNameCBdata(CallbackData, prefix="coffee_name"):
    category: str

class SizePriceCBdata(CallbackData, prefix="size_price"):
    variant_id: int
    coffee_slug: str

class BuyingOperationCB(CallbackData, prefix='buying menu'):
    operation_type: str
    coffee_name: str = None
    variant_id: int = None

class BuyingFromCartCB(CallbackData, prefix='cart buying'):
    user_id: str
    general_price: int
    variants_ids: str

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


def generate_buying_menu(variant_id, coffee_name, coffee_slug):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Buy now 💸', callback_data=BuyingOperationCB(operation_type='buying menu', coffee_name=coffee_name, variant_id=variant_id).pack()),
        InlineKeyboardButton(text='Add to cart 🛒', callback_data=BuyingOperationCB(operation_type='add to cart', coffee_name=coffee_name, variant_id=variant_id).pack()),
        InlineKeyboardButton(text='Back to sizes', callback_data=CoffeeNameCBdata(category=coffee_slug).pack()),
        InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')
    )
    builder.adjust(1, 1, 2)
    return builder.as_markup()


def add_to_cart(cart_line: str, user_id: str):
    info = json_reader(path)
    if len(info) > 0:
        if 'cart' in info.keys() and 'operations_qty' in info.keys():
            if user_id in info["cart"].keys():
                info["operations_qty"] += 1
                info["cart"][user_id][info["operations_qty"]] = cart_line
                json_update(path, info)
            else:
                raise KeyError("ERROR: User not found.")
        else:
            raise KeyError("ERROR: Key not found ('cart' or 'operation_qty').")
    else:
        raise Exception("ERROR: File is empty.")


def generate_cart_bts(user_id: str, general_price: int, variants_ids: str):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Pay 💸', callback_data=BuyingFromCartCB(user_id=user_id, general_price=general_price, variants_ids=variants_ids).pack()))
    builder.row(InlineKeyboardButton(text='Delete last ❌', callback_data=DeleteElCB(user_id=user_id).pack()))
    builder.row(InlineKeyboardButton(text='Clear cart ❌', callback_data=ClearCartCB(user_id=user_id).pack()))
    builder.row(InlineKeyboardButton(text='Back to menu ⬅️', callback_data='Back to menu'))
    builder.adjust(1, 2, 1)
    return builder.as_markup()
