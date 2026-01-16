import json
import os
from functools import wraps
import datetime

def list_to_str_json(list_to_convert):
    converted_list = json.dumps(list_to_convert)
    return converted_list

def str_to_list_json(str_to_convert):
    converted_str = json.loads(str_to_convert)
    return converted_str


def is_file_exists(func):
    @wraps(func)
    def wrapper(filename: str, dict_to_update: dict = None):
        if os.path.exists(filename) and os.stat(filename).st_size > 0:
            if func.__name__ == 'json_reader':
                return func(filename)
            return func(filename, dict_to_update)
        else:
            raise FileExistsError("File does not exist or empty.")
    return wrapper

@is_file_exists
def json_reader(filename):
    with open(filename, "r", encoding='utf-8') as file:
        return json.load(file)

@is_file_exists
def json_update(filename, dict_to_update):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(fp=file, obj=dict_to_update, indent=4)
        return True

