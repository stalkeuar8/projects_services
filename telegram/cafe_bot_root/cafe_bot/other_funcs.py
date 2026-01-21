import json

def list_to_str_json(list_to_convert):
    converted_list = json.dumps(list_to_convert)
    return converted_list

def str_to_list_json(str_to_convert):
    converted_str = json.loads(str_to_convert)
    return converted_str
