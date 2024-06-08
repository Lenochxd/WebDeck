import json
import os.path

def load_config():
    global config
    
    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)
        
    if os.path.exists("config.json"):
        os.remove("config.json")
        
    return config