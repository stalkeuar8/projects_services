from ..database.filling_getting_user_info import add_to_cart_db, add_order_to_db, clear_user_cart, del_last_line_cart, get_coffee_name_by_type_id, get_cart_info, \
    get_variant_info, get_coffee_names, get_coffee_slugs, get_id_of_coffee_type, get_variants_by_id, check_cart_db_limit
from aiogram import types, Router, F
from cafe_bot.keyboards.menu import generate_menu_kb
from cafe_bot.keyboards.catalog_menu import BuyingFromCartCB, ClearCartCB, DeleteElCB ,generate_cart_bts, generate_menu_catalog_kb, generate_sizes_prices_kb, CoffeeNameCBdata, SizePriceCBdata, generate_buying_menu, BuyingOperationCB
from cafe_bot.other_funcs import list_to_str_json
from cafe_bot.logs.logging import logger

router = Router()
path = r"D:\coding\python\telegram\cafe_bot\database\cafe_bot_info.db"

@router.message(F.text == 'Contacts 📞')
async def show_contacts(message: types.Message):
    await message.answer('Bot username: @cafetheria_bot\nOur email: cafetheria_bot@gmail.com\nPhone us: +380777777777')

@router.message(F.text == "Main Page")
async def come_back_to_main_page(message: types.Message):
    await message.answer(text="Continue using our coffee bot! ☕", reply_markup=generate_menu_kb())

@router.callback_query(F.data == 'Back to menu')
@router.message(F.text == 'Menu ☕')
async def show_menu(message: types.Message | types.CallbackQuery):
    coffee_names = get_coffee_names()
    coffee_slugs = get_coffee_slugs()
    if isinstance(message, types.Message):
        await message.answer(
            "Menu: \n",
            reply_markup=generate_menu_catalog_kb(coffee_names, coffee_slugs))
    else:
        await message.message.edit_text(
            "Menu: \n",
            reply_markup=generate_menu_catalog_kb(coffee_names, coffee_slugs)
        )

@router.callback_query(CoffeeNameCBdata.filter())
async def choose_coffee(callback: types.CallbackQuery, callback_data: CoffeeNameCBdata):
    coffee_slug = callback_data.category
    coffee_name = get_coffee_names(slug=coffee_slug)[0]
    coffee_type_id = get_id_of_coffee_type(coffee_slug)
    variants = get_variants_by_id(coffee_type_id)
    await callback.message.edit_text(
        text=f"{coffee_name} ☕:", reply_markup=generate_sizes_prices_kb(variants, coffee_slug)
    )

@router.callback_query(SizePriceCBdata.filter())
async def choose_size_buy(callback: types.CallbackQuery, callback_data: SizePriceCBdata):
    coffee_slug = callback_data.coffee_slug
    coffee_name = get_coffee_names(slug=coffee_slug)[0]
    var_info = get_variant_info(callback_data.variant_id)
    chosen_line = f"{coffee_name} | {var_info[2]} - {var_info[3]} ml | Price: {var_info[4]} Uah"
    await callback.message.edit_text(text=f"{chosen_line}", reply_markup=generate_buying_menu(callback_data.variant_id, coffee_name, coffee_slug))


@router.callback_query(BuyingOperationCB.filter())
async def buying_operation(callback: types.CallbackQuery, callback_data: BuyingOperationCB):
    if callback_data.operation_type == 'buying menu':
        user_id = str(callback.from_user.id)
        var_info = get_variant_info(callback_data.variant_id)
        order_id = add_order_to_db(user_id, var_info[3], str(var_info[0]))
        logger.bind(type='sale').info(f"User {callback.from_user.username} ({user_id}) ordered (order id: {order_id}) | Variant id: {var_info[0]}")
        logger.bind(type='payment').info(f"User {callback.from_user.username} ({user_id}) made a payment: SUCCESSFUL. | Order id: {order_id}")
        await callback.message.edit_text(text='Here will be a payment page. Use btn to come back to menu', reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
                        ]
                    )
                )
#         # await callback.message.edit_text(text="Please, make a payment! (Send 💋)", reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='Back to payment menu', callback_data=SizePriceCBdata(variant_id=callback_data.variant_id, coffee_name=callback_data.coffee_name).pack())]]))
#         # @router.message()
#         # async def buying(message: types.Message):
#         #     if message.text == '💋':
#         #         await callback.message.edit_text(text='Receiving payment.. 💸\n\nIt may take few seconds.')
#         #         await asyncio.sleep(3)
#         #         await callback.message.answer(
#         #             text='Payment successfully received! Thank you for using our cafe bot! ☕ \n\nUse button below to come back to menu:',
#         #             reply_markup=types.InlineKeyboardMarkup(
#         #                 inline_keyboard=[
#         #                     [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
#         #                 ]
#         #             )
#         #         )
#         #     else:
#         #         await message.edit_text(text='Receiving payment... 💸\n\nIt may take few seconds.')
#         #         await callback.message.edit_text(
#         #             text='Wrong payment details received. Payment canceled. ❌\n\nPlease try more later.\n\nUse button below to come back to menu:',
#         #             reply_markup=types.InlineKeyboardMarkup(
#         #                 inline_keyboard=[
#         #                     [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
#         #                 ]
#         #             )
#         #         )
    elif callback_data.operation_type == 'add to cart':
        user_id = str(callback.from_user.id)
        if check_cart_db_limit(user_id):
            logger.bind(type='cart').info(f"User {callback.from_user.username} ({callback.from_user.id}) added to cart variant {callback_data.variant_id}")
            var_info = get_variant_info(callback_data.variant_id)
            add_to_cart_db(user_id, var_info[1], var_info[0])
            await callback.message.edit_text(
                text=f"Added to cart:\n\n{callback_data.coffee_name} ☕ | {var_info[2]} - {var_info[3]} ml | Price: {var_info[4]} Uah 💸",
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
                ])
            )
        else:
            logger.bind(type='cart').info(f"User {callback.from_user.username} ({callback.from_user.id}) RICHES LIMIT (6) and was unable to add to cart variant {callback_data.variant_id}")
            await callback.message.edit_text(
                text=f"Unfortunately, you cant add something to cart now, because you are out of cart element limit (6 elements)\n\n"
                     f"Please, make an order or remove some elements from cart to add new elements! 🛒",
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
                ])
            )
    else:
        raise ValueError("ERROR: Wrong operation type. Must be ('add to cart' or 'buying menu').")


@router.callback_query(BuyingFromCartCB.filter())
async def buying_from_cart(callback: types.CallbackQuery, callback_data: BuyingFromCartCB):
    variants_ids = callback_data.variants_ids
    user_id = callback_data.user_id
    general_price = callback_data.general_price
    order_id = add_order_to_db(user_id, general_price, variants_ids)
    clear_user_cart(user_id)
    logger.bind(type='sale').info(f"User {callback.from_user.username} ({user_id}) ordered (order id: {order_id}) | Variant id: {variants_ids}")
    logger.bind(type='payment').info(f"User {callback.from_user.username} ({user_id}) made a payment: SUCCESSFUL. | Order id: {order_id}")
    await callback.message.edit_text(text='Here will be a payment page. Use btn to come back to menu', reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
                        ]
                    )
                )




@router.message(F.text == 'Cart 🛒')
async def show_cart(message: types.Message):
    user_id = str(message.from_user.id)
    info = get_cart_info(user_id)
    if info:
        output = ''
        gen_price = 0
        var_ids_list = []
        for line in info:
            coffee_name = get_coffee_name_by_type_id(line[1])
            var_info = get_variant_info(line[2])
            output += f"{coffee_name} {var_info[2]} - {var_info[3]} ml | Price: {var_info[4]} Uah\n"
            gen_price += var_info[4]
            var_ids_list.append(var_info[0])
        var_ids_str = list_to_str_json(var_ids_list)
        output += f"\n\nGeneral price: {gen_price} Uah"
        logger.bind(type='cart').info(f"User {message.from_user.username} ({message.from_user.id}) opened cart!")
        await message.answer(text=output, reply_markup=generate_cart_bts(user_id, gen_price, var_ids_str))
    else:
        await message.answer("The cart is empty! Add something to cart to see it!")


@router.callback_query(ClearCartCB.filter())
async def clear_cart(callback: types.CallbackQuery, callback_data: ClearCartCB):
    user_id = str(callback.from_user.id)
    clear_user_cart(user_id)
    logger.bind(type='cart').info(f"User {callback.from_user.username} ({user_id}) cleared cart!")
    await callback.message.answer(text='Your cart has been cleared!\n\nContinue using our cafe bot! ☕')

@router.callback_query(DeleteElCB.filter())
async def delete_last_el(callback: types.CallbackQuery, callback_data: DeleteElCB):
    user_id = str(callback.from_user.id)
    del_last_line_cart(user_id)
    logger.bind(type='cart').info(f"User {callback.from_user.username} ({user_id}) deleted last element in cart!")
    await callback.message.answer(text='Last element has been deleted!\n\nUse  "Cart 🛒"  to see cart one more time!\n\nOr use  "Menu ☕"  to see menu!')


#
#
# MENU_CATALOG = {
#     "Americano": {
#         "text": "Americano",
#         "sizes_prices": {
#             1: {'size': 'Small - 150 ml', 'price': 35},
#             2: {'size': 'Medium - 250 ml', 'price': 45},
#             3: {'size': 'Big - 350 ml', 'price': 50}
#         }
#     },
#     "Espresso": {
#         "text": "Espresso",
#         "sizes_prices": {
#             4: {'size': 'Standard - 30 ml', 'price': 20},
#             5: {'size': 'Dopio - 60 ml', 'price': 30}
#         }
#     },
#     "Cacao": {
#         "text": "Cacao",
#         "sizes_prices": {
#             6: {'size': 'Small - 200 ml', 'price': 45},
#             7: {'size': 'Medium - 300 ml', 'price': 55},
#             8: {'size': 'Big - 400 ml', 'price': 65}
#         }
#     },
#     "Capuccino": {
#         "text": "Capuccino",
#         "sizes_prices": {
#             9: {'size': 'Small - 150 ml', 'price': 40},
#             10: {'size': 'Medium - 250 ml', 'price': 55},
#             11: {'size': 'Big - 350 ml', 'price': 70}
#         }
#     },
#     "Latte": {
#         "text": "Latte",
#         "sizes_prices": {
#             12: {'size': 'Small - 200 ml', 'price': 55},
#             13: {'size': 'Medium - 300 ml', 'price': 65},
#             14: {'size': 'Big - 400 ml', 'price': 80}
#         }
#     }
# }