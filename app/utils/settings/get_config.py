import json
import os
from ..paths import CONFIG_FILE
from ..working_dir import get_base_dir
from ..args import get_arg
from .check_config_update import check_config_update
from .save_config import save_config

base_dir = get_base_dir()
default_config_path = os.path.join(base_dir, "resources/config_default.json")


def ensure_config_exists():
    old_config_path = os.path.join(base_dir, "config.json")
    if os.path.exists(old_config_path):
        os.rename(old_config_path, CONFIG_FILE)
    
    elif not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(default_config_path, "r", encoding="utf-8") as src, open(CONFIG_FILE, "w", encoding="utf-8") as dst:
            dst.write(src.read())
    
    if os.path.exists(old_config_path):
        os.remove(old_config_path)


def get_config(check_updates=False, save_updated_config=False):
    ensure_config_exists()
    
    with open(CONFIG_FILE, encoding="utf-8") as f:
        config = json.load(f)
        
    if check_updates or save_updated_config:
        config = check_config_update(config)
        if save_updated_config:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
    
    return config


def get_port():
    port = get_arg("port")
    if port is None:
        port = get_config().get("url", {}).get("port")
    return port
