from aiogram import F, types, Router
from telegram.library_bot.keyboards.catalog import generate_catalog_kb, CategoryCBdata, BookCBdata, generate_books_kb, back_to_category_books
from telegram.library_bot.info_catalog import CATALOG

router = Router()

@router.callback_query(F.data == 'catalog')
@router.message(F.text == 'Catalog')
async def catalog(message: types.Message | types.CallbackQuery):
    if isinstance(message, types.Message):
        await message.answer(
            "Our catalog: ",
            reply_markup=generate_catalog_kb(CATALOG)
            )
    else:
        await message.message.edit_text(
            "Our catalog: ",
            reply_markup=generate_catalog_kb(CATALOG)
        )

@router.callback_query(CategoryCBdata.filter())
async def category_info(callback: types.CallbackQuery, callback_data: CategoryCBdata):
    category = CATALOG.get(callback_data.category)
    await callback.message.edit_text(
        text=category['description'],
        reply_markup=generate_books_kb(category["books"], callback_data.category)
    )

@router.callback_query(BookCBdata.filter())
async def book_info(callback: types.CallbackQuery, callback_data:BookCBdata):
    book_id = callback_data.id
    category = CATALOG.get(callback_data.category)
    book = None
    for bk in category['books']:
        if bk['id'] == book_id:
            book = bk
            break

    if not book:
        return await callback.answer("Book was not found")
    await callback.message.edit_text(
        f"Book name: {book['name']}\nDescription: {book['description']}\nPrice: {book['price']}\n\nDo you want to buy?", reply_markup=back_to_category_books(callback_data.category)
        )


