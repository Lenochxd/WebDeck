import json
import os
from app.utils.args import get_arg
from app.utils.settings.check_config_update import check_config_update
from app.utils.working_dir import get_base_dir

base_dir = get_base_dir()
config_path = os.path.join(base_dir, ".config/config.json")
default_config_path = os.path.join(base_dir, "webdeck/config_default.json")


def ensure_config_exists():
    if os.path.exists("config.json"):
        os.rename("config.json", config_path)
    elif not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(default_config_path, "r", encoding="utf-8") as src, open(config_path, "w", encoding="utf-8") as dst:
            dst.write(src.read())
    if os.path.exists("config.json"):
        os.remove("config.json")


def get_config(check_updates=False, save_updated_config=False):
    ensure_config_exists()
    
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
        
    if check_updates or save_updated_config:
        config = check_config_update(config)
        if save_updated_config:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
    
    return config


def get_port():
    port = get_arg("port")
    if port is None:
        port = get_config().get("url", {}).get("port")
    return port