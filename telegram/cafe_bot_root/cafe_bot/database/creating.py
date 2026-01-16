import sqlite3
db = 'cafe_bot_info.db'
# coffee_names = [coffee_name for coffee_name in MENU_CATALOG.keys()]
# slugs = [coffee_name.lower() for coffee_name in coffee_names]
# coffee_ids = [i for i in range(1, len(coffee_names)+1)]
# list_to_insert = []
# for coffee_id, name, slug in zip(coffee_ids, coffee_names, slugs):
#     list_to_insert.append((coffee_id, name, slug))
#
# # products TABLE
# #### CREATING
# with sqlite3.connect(db) as db_file:
#     db_file.execute("""CREATE TABLE IF NOT EXISTS products (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     coffee_name text,
#     slug text
#     )""")
#     c = db_file.cursor()
#     c.executemany("INSERT INTO products (id, coffee_name, slug) VALUES(?, ?, ?)", list_to_insert)
#     db_file.commit()
#
# # product_variants TABLE
# variant_id = [i for i in range(1001, 1015)]
# sizes_list = ['Small', 'Medium', 'Big', 'Standard', 'Dopio', 'Small', 'Medium', 'Big', 'Small', 'Medium', 'Big', 'Small', 'Medium', 'Big']
# volumes_list = [150, 250, 350, 30, 60, 200, 300, 400, 150, 250, 350, 200, 300, 400]
# prices_list = [35, 45, 50, 20, 30, 45, 55, 65, 40, 55, 70, 55, 65, 80]
# new_coffee_ids = [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
#
# vars_list_to_insert = []
# for variant_id, coffee_id, size, volume, price in zip(variant_id, new_coffee_ids, sizes_list, volumes_list, prices_list):
#     vars_list_to_insert.append((variant_id, coffee_id, size, volume, price))
#
# #### CREATING
# with sqlite3.connect(db) as db_file:
#     db_file.execute("""CREATE TABLE IF NOT EXISTS product_variants (
#     variant_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     product_type_id integer,
#     size_name text,
#     volume_ml integer,
#     price integer
#     )""")
#     c = db_file.cursor()
#     c.executemany("INSERT INTO product_variants (variant_id, product_type_id, size_name, volume_ml, price) VALUES(?, ?, ?, ?, ?)", vars_list_to_insert)
#     db_file.commit()
#
#
#
# # USER_INFO
#
# #
# with sqlite3.connect(db) as db_file:
#     c = db_file.cursor()
#     db_file.execute("""CREATE TABLE IF NOT EXISTS users_info (
#         user_tg_id BIGINT,
#         user_tg_username text,
#         user_first_name text
#     )""")
#     db_file.commit()
#
# with sqlite3.connect(db) as db_file:
#     c = db_file.cursor()
#     db_file.execute("""CREATE TABLE IF NOT EXISTS cart_info (
#         user_tg_id BIGINT,
#         coffee_type_id integer,
#         variant_id integer
#     )""")
#     db_file.commit()
#
#
# with sqlite3.connect(db) as db_file:
#     c = db_file.cursor()
#     db_file.execute("""CREATE TABLE IF NOT EXISTS orders (
#         order_id integer,
#         user_tg_id BIGINT,
#         general_price integer,
#         variants_ids text
#     )""")
#     db_file.commit()



    # c.execute("INSERT INTO users_info (line_id, user_tg_id, user_tg_username, user_first_name) VALUES (?, ?, ?, ?)", )


