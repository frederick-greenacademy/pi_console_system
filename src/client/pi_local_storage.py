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

def save_config():
    with open(file_name, 'w') as f:
        json.dump(config, f)       

# if __name__ == "__main__":
#     read()
#     # config["items"] = []
#     config["items"].append('AAA')
#     config["items"].append('BBB')
#     print(config)
#     save()