import json
from ..global_variables import set_global_variable
from ..paths import CONFIG_FILE


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    set_global_variable("config", config)
    return config
