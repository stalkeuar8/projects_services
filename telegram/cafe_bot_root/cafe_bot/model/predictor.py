from pathlib import Path
import joblib
import datetime
import pandas as pd

def day_time_identifier():
    cur_time = datetime.datetime.now().strftime('%H:%M:%S')
    if cur_time < "12:00:00":
        return ("morning", 2)
    elif "12:00:00" < cur_time < "17:00:00":
        return ("lunchtime", 2)
    else:
        return ("evening", 1)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / 'coffee_predictor.pkl'
package = joblib.load(MODEL_PATH)

def predict_time(coffee_name: str, variant_id: int):
    day_time_work_qty = day_time_identifier()
    new_data = {
        "Coffee_name": [coffee_name],
        'Variant Id' : [variant_id],
        'Coffee maker qty' : [day_time_work_qty[1]],
        'day' : [datetime.datetime.now().strftime('%A')],
        'day time' : [day_time_work_qty[0]],
        'month' : [datetime.datetime.now().strftime('%B')]
    }
    model = package['model']
    expected_columns = package['features']
    df_new = pd.DataFrame(new_data)
    df_new_encoded = pd.get_dummies(df_new)
    df_final = df_new_encoded.reindex(columns=expected_columns, fill_value=0)
    pred_time = int(model.predict(df_final)[0].round(0))
    return about_prediction(pred_time)


def about_prediction(time: int):
    if time <= 4:
        return f"Almost no people. Your order will be ready extremely fastly!\nIn {time} minutes!"
    elif 4 < time <= 6:
        return f"There are some people in cafe. Your order will be ready in {time} minutes!"
    elif 6 < time <= 9:
        return f"There are a lot of people in our cafe. You will have to wait for {time-1}-{time} minutes!"
    elif time > 9:
        return f"There are an extreme amount of people in our cafe. You will have to wait for {time - 1}-{time} minutes!"
    else:
        return "Error time calculated"
