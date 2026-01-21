import pandas as pd
import random


NUM_SAMPLES = 100000

PRODUCTS = {
    1001: {"name": "Americano", "size_mod": -0.5, "base_time": 3},
    1002: {"name": "Americano", "size_mod": 0, "base_time": 3},
    1003: {"name": "Americano", "size_mod": 1, "base_time": 3},
    1004: {"name": "Espresso", "size_mod": -0.5, "base_time": 2},
    1005: {"name": "Espresso", "size_mod": 0.5, "base_time": 2},
    1006: {"name": "Cacao", "size_mod": -0.5, "base_time": 6},
    1007: {"name": "Cacao", "size_mod": 0, "base_time": 6},
    1008: {"name": "Cacao", "size_mod": 1, "base_time": 6},
    1009: {"name": "Cappuccino", "size_mod": -0.5, "base_time": 5},
    1010: {"name": "Cappuccino", "size_mod": 0, "base_time": 5},
    1011: {"name": "Cappuccino", "size_mod": 1, "base_time": 5},
    1012: {"name": "Latte", "size_mod": -0.5, "base_time": 5},
    1013: {"name": "Latte", "size_mod": 0, "base_time": 5},
    1014: {"name": "Latte", "size_mod": 1, "base_time": 5},
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
TIMES = ["Morning", "Lunchtime", "Evening"]

WINTER_MONTHS = ["December", "January", "February"]

data = []

print(f"Генерую {NUM_SAMPLES} записів...")

for _ in range(NUM_SAMPLES):
    variant_id = random.choice(list(PRODUCTS.keys()))
    product_info = PRODUCTS[variant_id]
    day = random.choice(DAYS)
    month = random.choice(MONTHS)
    day_time = random.choice(TIMES)
    is_weekend = day in ["Saturday", "Sunday"]
    is_winter = month in WINTER_MONTHS

    if day_time in ["Morning", "Lunchtime"]:
        staff_qty = 2
    elif day_time == "Evening":
        if is_weekend or is_winter:
            staff_qty = 2
        else:
            staff_qty = 1
    prep_time = product_info["base_time"] + product_info["size_mod"]
    queue_time = 0
    if day_time == "Morning":
        queue_time += 10
    elif day_time == "Lunchtime":
        queue_time += 5
    else:
        queue_time += 2
        if is_winter:
            queue_time += 3

    if is_weekend:
        queue_time += 5

    total_time = prep_time + queue_time


    if staff_qty == 2:
        total_time = total_time * 0.6

    noise = random.uniform(-1.5, 2.5)
    final_time = round(total_time + noise)

    if final_time < 2:
        final_time = 2

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

print(df.head(10))