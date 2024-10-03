import json
from ..global_variables import set_global_variable


def save_config(config):
    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    set_global_variable("config", config)
    return config