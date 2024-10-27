import json
import os

config_path = ".config/config.json"
default_config_path = "webdeck/config_default.json"

def ensure_config_exists():
    if os.path.exists("config.json"):
        os.rename("config.json", config_path)
    elif not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(default_config_path, "r", encoding="utf-8") as src, open(config_path, "w", encoding="utf-8") as dst:
            dst.write(src.read())
    if os.path.exists("config.json"):
        os.remove("config.json")

def load_config():
    ensure_config_exists()
    
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
        
    return config

def get_port():
    return load_config()["url"]["port"]