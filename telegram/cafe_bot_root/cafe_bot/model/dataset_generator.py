import pandas as pd
import random

# --- НАЛАШТУВАННЯ ГЕНЕРАЦІЇ ---
NUM_SAMPLES = 100000  # Кількість рядків, які хочеш отримати

# База даних продуктів (з твоїх скріншотів)
# ID: {Name, Size_modifier (Small=-0.5, Medium=0, Big=+1), Base_time_min}
PRODUCTS = {
    # Americano (Base time: 3 min)
    1001: {"name": "Americano", "size_mod": -0.5, "base_time": 3},  # Small
    1002: {"name": "Americano", "size_mod": 0, "base_time": 3},  # Medium
    1003: {"name": "Americano", "size_mod": 1, "base_time": 3},  # Big

    # Espresso (Base time: 2 min)
    1004: {"name": "Espresso", "size_mod": -0.5, "base_time": 2},  # Standard
    1005: {"name": "Espresso", "size_mod": 0.5, "base_time": 2},  # Dopio

    # Cacao (Base time: 6 min - довше мішати)
    1006: {"name": "Cacao", "size_mod": -0.5, "base_time": 6},  # Small
    1007: {"name": "Cacao", "size_mod": 0, "base_time": 6},  # Medium
    1008: {"name": "Cacao", "size_mod": 1, "base_time": 6},  # Big

    # Cappuccino (Base time: 5 min - пінка)
    1009: {"name": "Cappuccino", "size_mod": -0.5, "base_time": 5},  # Small
    1010: {"name": "Cappuccino", "size_mod": 0, "base_time": 5},  # Medium
    1011: {"name": "Cappuccino", "size_mod": 1, "base_time": 5},  # Big

    # Latte (Base time: 5 min - пінка)
    1012: {"name": "Latte", "size_mod": -0.5, "base_time": 5},  # Small
    1013: {"name": "Latte", "size_mod": 0, "base_time": 5},  # Medium
    1014: {"name": "Latte", "size_mod": 1, "base_time": 5},  # Big
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
TIMES = ["Morning", "Lunchtime", "Evening"]

WINTER_MONTHS = ["December", "January", "February"]

data = []

print(f"Генерую {NUM_SAMPLES} записів...")

for _ in range(NUM_SAMPLES):
    # 1. Рандомний вибір вхідних параметрів
    variant_id = random.choice(list(PRODUCTS.keys()))
    product_info = PRODUCTS[variant_id]

    day = random.choice(DAYS)
    month = random.choice(MONTHS)
    day_time = random.choice(TIMES)

    # 2. Логіка визначення кількості барист
    # Правило: 2 баристи завжди вранці та в обід.
    # Ввечері 2 баристи ТІЛЬКИ якщо це вихідні АБО зима (сезон).
    is_weekend = day in ["Saturday", "Sunday"]
    is_winter = month in WINTER_MONTHS

    if day_time in ["Morning", "Lunchtime"]:
        staff_qty = 2
    elif day_time == "Evening":
        if is_weekend or is_winter:
            staff_qty = 2
        else:
            staff_qty = 1

    # 3. Розрахунок часу (Simulation Logic)

    # А. Базовий час напою + розмір
    prep_time = product_info["base_time"] + product_info["size_mod"]

    # Б. Час на чергу (залежить від часу доби та дня)
    queue_time = 0
    if day_time == "Morning":
        queue_time += 10  # Ранкова кава перед роботою - велика черга
    elif day_time == "Lunchtime":
        queue_time += 5  # Обід
    else:  # Evening
        queue_time += 2  # Ввечері спокійніше
        if is_winter:
            queue_time += 3  # Але взимку ввечері люди гріються

    if is_weekend:
        queue_time += 5  # На вихідних завжди більше людей

    # В. Підсумок "брудного" часу
    total_time = prep_time + queue_time

    # Г. Ефект від кількості персоналу
    if staff_qty == 2:
        total_time = total_time * 0.6  # Працюють на 40% швидше

    # Д. Додаємо "людський фактор" (Random Noise)
    # Реальний час ніколи не буває ідеальним, додаємо +/- 1-2 хвилини
    noise = random.uniform(-1.5, 2.5)
    final_time = round(total_time + noise)

    # Час не може бути менше 2 хвилин (фізично неможливо)
    if final_time < 2:
        final_time = 2

    # 4. Запис рядка
    row = {
        "Coffee_name": product_info["name"],
        "Variant Id": variant_id,
        "Coffee maker qty": staff_qty,
        "day": day,
        "day time": day_time,
        "month": month,
        "Time to wait (min)": final_time
    }
    data.append(row)

df = pd.DataFrame(data)
df.to_csv("coffee_shop_data.csv", index=False)

print("Готово! Файл 'coffee_shop_data.csv' створено.")
print(df.head(10))