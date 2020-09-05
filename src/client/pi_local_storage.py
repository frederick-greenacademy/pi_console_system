import json
import os

file_name = "config.json"

config = {"items": []}


def read_config():
    # Tao moi file neu ko ton tai
    if not os.path.isfile(file_name):
        save_config()
    # doc thong tin trong file
    with open(file_name, 'r') as f:
        config = json.load(f)


def add_list_data(list_data):
    if len(config["items"]) <= 0:
        for item in list_data:
            config["items"].append(item)
    else:
        for new_item in list_data:
            if new_item not in config["items"]:
                config["items"].append(item)


def save_config():
    with open(file_name, 'w') as f:
        json.dump(config, f)
