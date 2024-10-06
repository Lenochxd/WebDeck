import re
import json


def extract_asked_device(input_string):
    pattern = r"\['(.*?)'\]"
    return re.findall(pattern, input_string)
    
def get_asked_devices():
    devices = []
    
    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)
    
    for folder_id, value in config["front"]["buttons"].items():
        for button in config["front"]["buttons"][folder_id]:
            if "message" in button.keys() and button["message"].startswith("/usage"):
                
                device = extract_asked_device(button["message"])
                if device is not None:
                    devices.append(device)
                    
    return devices