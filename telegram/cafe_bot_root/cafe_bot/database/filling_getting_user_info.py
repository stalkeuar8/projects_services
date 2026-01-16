import os.path
import sqlite3
from functools import wraps
from random import randint
db_path = r"D:\coding\python\advanced_python\telegram\cafe_bot_root\cafe_bot\database\cafe_bot_info.db"

def is_db_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.path.exists(db_path):
            return func(*args, **kwargs)
        else:
            raise FileExistsError("ERROR: DB File does not exists or broken.")
    return wrapper

@is_db_exists
def register_user_to_db(user_tg_id, user_tg_username, user_first_name) -> bool:
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("INSERT INTO users_info (user_tg_id, user_tg_username, user_first_name) VALUES (?, ?, ?)", (user_tg_id, user_tg_username, user_first_name))
        db_file.commit()
    return True

@is_db_exists
def extract_exact_user_info(user_tg_id: str) -> bool:
    user_id = [user_tg_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT * FROM users_info WHERE user_tg_id = (?)", user_id)
        res = c.fetchall()
        if res:
            return True
        return False


@is_db_exists
def add_to_cart_db(user_tg_id, coffee_type_id, variant_id) -> bool:
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("INSERT INTO cart_info (user_tg_id, coffee_type_id, variant_id) VALUES (?, ?, ?)",
                  (user_tg_id, coffee_type_id, variant_id))
        db_file.commit()
    return True


@is_db_exists
def get_coffee_names(slug: str = None) -> list:
    slug_to_find = [slug]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT coffee_name FROM products") if not slug else c.execute("SELECT coffee_name FROM products WHERE slug = (?)", slug_to_find)
        coffee_names_list = [name[0] for name in c.fetchall()]
    return coffee_names_list

@is_db_exists
def get_coffee_name_by_type_id(coffee_type_id: int) -> str:
    id_to_find = [coffee_type_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT coffee_name FROM products WHERE id = (?)", id_to_find)
        coffee_name = c.fetchall()[0][0]
        return coffee_name


@is_db_exists
def get_coffee_info(slug: str = None) -> list:
    slug_to_find = [slug]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT * FROM products WHERE slug = (?)", slug_to_find)
        coffee_info = c.fetchall()[0]
    return coffee_info

@is_db_exists
def get_variant_info(var_id: int) -> list:
    id_to_find = [var_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT * FROM product_variants WHERE variant_id = (?)", id_to_find)
        variant_info = c.fetchall()[0]
        return variant_info


@is_db_exists
def get_coffee_slugs() -> list:
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT slug FROM products")
        coffee_slugs_list = [name[0] for name in c.fetchall()]
    return coffee_slugs_list


@is_db_exists
def get_id_of_coffee_type(slug: str) -> int:
    slug_to_find = [slug]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT id FROM products WHERE slug = (?)", slug_to_find)
        res = int(c.fetchall()[0][0])
    return res


@is_db_exists
def get_variants_by_id(coffee_type_id: int) -> list:
    id_to_find = [coffee_type_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT * FROM product_variants WHERE product_type_id = (?)", id_to_find)
        res = c.fetchall()
    return res

@is_db_exists
def get_cart_info(user_tg_id: str) -> list:
    id_to_find = [user_tg_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT * FROM cart_info WHERE user_tg_id = (?)", id_to_find)
        res = c.fetchall()
    return res


@is_db_exists
def del_last_line_cart(user_tg_id: str) -> bool:
    user_id = [user_tg_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT MAX(rowid) FROM cart_info WHERE user_tg_id = (?)", user_id)
        row_id = [c.fetchall()[0][0]]
        c.execute("DELETE FROM cart_info WHERE rowid = (?)", row_id)
        db_file.commit()
    return True


@is_db_exists
def clear_user_cart(user_tg_id: str) -> bool:
    user_id = [user_tg_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("DELETE FROM cart_info WHERE user_tg_id = (?)", user_id)
        db_file.commit()
    return True

@is_db_exists
def is_order_id_exists(order_id: int) -> bool:
    id_to_find = [order_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT * FROM orders WHERE order_id = (?)", id_to_find)
        res = c.fetchall()
        if res:
            return True
        return False

@is_db_exists
def add_order_to_db(user_tg_id: str, general_price: int, variants_ids: str) -> int:
    while True:
        order_id = randint(100000, 999999)
        if not is_order_id_exists(order_id): break
        else: continue
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("INSERT INTO orders (order_id, user_tg_id, general_price, variants_ids) VALUES (?, ?, ?, ?)", (order_id, user_tg_id, general_price, variants_ids))
    return order_id

@is_db_exists
def check_cart_db_limit(user_tg_id: str) -> bool:
    user_id = [user_tg_id]
    with sqlite3.connect(db_path) as db_file:
        c = db_file.cursor()
        c.execute("SELECT * FROM cart_info WHERE user_tg_id = (?)", user_id)
        qty = c.fetchall()
        if len(qty) == 6:
            return False
        else:   return True
