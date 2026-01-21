from cafe_bot.database.filling_getting_user_info import add_to_cart_db, add_order_to_db, clear_user_cart, del_last_line_cart, get_coffee_name_by_type_id, get_cart_info, \
    get_variant_info, get_coffee_names, get_coffee_slugs, get_id_of_coffee_type, get_variants_by_id, check_cart_db_limit, get_coffee_info
from aiogram import types, Router, F
from cafe_bot.keyboards.menu import generate_menu_kb
from cafe_bot.keyboards.catalog_menu import ShowCartCB, generate_paying_menu_single_bts, generate_paying_menu_cart_bts, AddToCartCB, ClearCartCB, DeleteElCB ,generate_cart_bts, generate_menu_catalog_kb, generate_sizes_prices_kb, CoffeeNameCBdata, SizePriceCBdata, generate_buying_menu, PaymentMenuCB
from cafe_bot.other_funcs import list_to_str_json, str_to_list_json
from cafe_bot.logs.logging import logger
from cafe_bot.fsm.states import ValidatePayment
from aiogram.fsm.context import FSMContext
from cafe_bot.fsm.paying_menu import payment_validator
from cafe_bot.model.predictor import predict_time
from typing import Union

router = Router()

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
    await callback.message.edit_text(text=f"{chosen_line}", reply_markup=generate_buying_menu(callback_data.variant_id, coffee_name, coffee_slug, var_info[4]))


@router.callback_query(PaymentMenuCB.filter())
async def paying_process(callback: types.CallbackQuery, callback_data: ValidatePayment, state: FSMContext):
    amount = callback_data.paying_currency_amount
    var_info = get_variant_info(str_to_list_json(callback_data.variant_id)[0])
    coffee_info = get_coffee_info(var_info[1])
    coffee_name = coffee_info[1]
    coffee_slug = coffee_info[2]
    user_id = str(callback.from_user.id)
    await state.update_data(is_cart=callback_data.is_cart, variant_id = callback_data.variant_id, total_price = callback_data.paying_currency_amount, coffee_name=coffee_name)
    await state.set_state(ValidatePayment.paying_currency)
    if not callback_data.is_cart:
        await callback.message.edit_text(
            text=f"This is payment menu 💸\nYou ordered: {coffee_name} | {var_info[2]} - {var_info[3]} ml | Price: {var_info[4]} Uah"
                 f"\nTotal price: {amount} Uah\n\nPlease, pay using 💋 ", reply_markup=generate_paying_menu_single_bts(coffee_slug=coffee_slug, variant_id=var_info[0]))
    else:
        await callback.message.edit_text(
            text=f"This is payment menu 💸\n"
                 f"\nTotal price: {amount} Uah\n\nPlease, pay using 💋 ", reply_markup=generate_paying_menu_cart_bts(user_id))



@router.message(ValidatePayment.paying_currency)
async def receiving_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = str(message.from_user.id)
    if payment_validator(message.text):
        is_cart = data.get("is_cart")
        variant_id = data.get("variant_id")
        total_price = data.get("total_price")
        coffee_name = data.get("coffee_name")
        time_to_wait_message = predict_time(coffee_name, variant_id)
        order_id = add_order_to_db(user_id, total_price, variant_id)
        logger.bind(type='sale').info(
            f"User {message.from_user.username} ({user_id}) ordered (order id: {order_id}) | Variant id: {variant_id}")
        logger.bind(type='payment').info(
            f"User {message.from_user.username} ({user_id}) made a payment: SUCCESSFUL. | Order id: {order_id}")
        await state.clear()
        if is_cart:
            logger.bind(type='cart').info(
                f"User {message.from_user.username} ({user_id}) ordered (order id: {order_id}) from cart. CART IS EMPTY NOW. | Variant id: {variant_id}")
            clear_user_cart(user_id)
        await message.answer(text=f"Payment received successfully! 💸\nOrder ID: {order_id}\n\n{time_to_wait_message}"
                                     "\n\nThank you for using our bot!", reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [types.InlineKeyboardButton(text='Open menu', callback_data='Back to menu')]
                        ]
                    ))
    else:
        await state.clear()
        logger.bind(type='payment').info(
            f"User {message.from_user.username} ({user_id}) had an attempt to make a payment: FATAL. Reason: Invalid payment.")
        await message.answer(text="Invalid payment received, please try more!", reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
                        ]
                    ))


@router.callback_query(AddToCartCB.filter())
async def add_to_cart(callback: types.CallbackQuery, callback_data: AddToCartCB):
    user_id = str(callback.from_user.id)
    if check_cart_db_limit(user_id):
        logger.bind(type='cart').info(
            f"User {callback.from_user.username} ({callback.from_user.id}) added to cart variant {callback_data.variant_id}")
        var_info = get_variant_info(callback_data.variant_id)
        add_to_cart_db(user_id, var_info[1], var_info[0])
        await callback.message.edit_text(
            text=f"Added to cart:\n\n{callback_data.coffee_name} ☕ | {var_info[2]} - {var_info[3]} ml | Price: {var_info[4]} Uah 💸",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
            ])
        )
    else:
        logger.bind(type='cart').info(
            f"User {callback.from_user.username} ({callback.from_user.id}) RICHES LIMIT (6) and was unable to add to cart variant {callback_data.variant_id}")
        await callback.message.edit_text(
            text=f"Unfortunately, you cant add something to cart now, because you are out of cart element limit (6 elements)\n\n"
                 f"Please, make an order or remove some elements from cart to add new elements! 🛒",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text='Back to menu', callback_data='Back to menu')]
            ])
        )


@router.callback_query(ShowCartCB.filter())
@router.message(F.text == 'Cart 🛒')
async def show_cart(event: Union[types.Message, types.CallbackQuery], callback_data: ShowCartCB = None):
    user_id = str(event.from_user.id)
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
        logger.bind(type='cart').info(f"User {event.from_user.username} ({event.from_user.id}) opened cart!")
        if isinstance(event, types.CallbackQuery):
            await event.message.edit_text(text=output, reply_markup=generate_cart_bts(user_id, gen_price, var_ids_str))
        else:
            await event.answer(text=output, reply_markup=generate_cart_bts(user_id, gen_price, var_ids_str))
    else:
        await event.answer("The cart is empty! Add something to cart to see it!")


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

