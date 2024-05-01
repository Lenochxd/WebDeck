import os

def check_json_update(config):
    
    # Set default background if not present
    if "background" not in config["front"]:
        config["front"]["background"] = ["#141414"]
        
    # Set default auto-updates setting if not present  
    if "auto-updates" not in config["settings"]:
        config["settings"]["auto-updates"] = "true"
        
    # Set default windows startup setting if not present
    if "windows-startup" not in config["settings"]:
        config["settings"]["windows-startup"] = "false"
        
    # Set default flask debug setting if not present
    if "flask-debug" not in config["settings"]:
        config["settings"]["flask-debug"] = "true"
        
    # Remove open settings in browser setting if present
    if "open-settings-in-browser" in config["settings"]:
        del config["settings"]["open-settings-in-browser"]
        
    # Set default open settings in integrated browser setting if not present
    if "open-settings-in-integrated-browser" not in config["settings"]:
        config["settings"]["open-settings-in-integrated-browser"] = "false"
        
    # Set default portrait rotate setting if not present
    if "portrait-rotate" not in config["front"]:
        config["front"]["portrait-rotate"] = "90"
        
    # Set default edit buttons color setting if not present
    if "edit-buttons-color" not in config["front"]:
        config["front"]["edit-buttons-color"] = "false"
        
    # Set default buttons color setting if not present
    if "buttons-color" not in config["front"]:
        config["front"]["buttons-color"] = ""
        
    # Set default soundboard settings if not present
    if "soundboard" not in config["settings"]:
        config["settings"]["soundboard"] = {
            "mic_input_device": "",
            "vbcable": "cable input",
        }
        
    # Set default mic input device if not present
    if "mic_input_device" not in config["settings"]["soundboard"]:
        config["settings"]["soundboard"]["mic_input_device"] = ""
        
    # Set default vbcable if not present
    if "vbcable" not in config["settings"]["soundboard"]:
        config["settings"]["soundboard"]["vbcable"] = "cable input"
        
    # Set default soundboard enabled based on mic input device
    if "enabled" not in config["settings"]["soundboard"]:
        if config["settings"]["soundboard"]["mic_input_device"] != "":
            config["settings"]["soundboard"]["enabled"] = "false"
        else:
            config["settings"]["soundboard"]["enabled"] = "true"
            
    # Set default OBS settings if not present
    if "obs" not in config["settings"]:
        config["settings"]["obs"] = {"host": "localhost", "port": 4455, "password": ""}
        
    # Set default automatic firewall bypass setting if not present
    if "automatic-firewall-bypass" not in config["settings"]:
        config["settings"]["automatic-firewall-bypass"] = "false"
        
    # Set default fix stop soundboard setting if not present
    if "fix-stop-soundboard" not in config["settings"]:
        config["settings"]["fix-stop-soundboard"] = "false"
        
    # Set default optimized usage display setting if not present
    if "optimized-usage-display" not in config["settings"]:
        config["settings"]["optimized-usage-display"] = "false"

    # Set default theme if not present or invalid
    if "theme" not in config["front"] or not os.path.isfile(f'static/themes/{config["front"]["theme"]}'):
        config["front"]["theme"] = "default_theme.css"

    # Get available theme files
    themes = [
        f"//{file_name}"
        for file_name in os.listdir("static/themes/")
        if file_name.endswith(".css") and not file_name.startswith("default_theme") and not file_name == config["front"]["theme"]
    ]
    
    # Add current theme file
    themes.append(config["front"]["theme"])
    
    # Set themes list
    config["front"]["themes"] = themes
    
    # Remove deleted themes
    config["front"]["themes"] = [
        theme for theme in config["front"]["themes"] if os.path.isfile(f"static/themes/{theme.replace('//', '')}")
    ]
    
    # Remove duplicate themes
    theme_set = set()
    config["front"]["themes"] = [
        theme for theme in config["front"]["themes"] 
        if not (theme in theme_set or theme_set.add(theme))
    ]
    
    # Move default theme to end
    if config["front"]["theme"] in config["front"]["themes"]:
        config["front"]["themes"].remove(config["front"]["theme"])
    config["front"]["themes"].append(config["front"]["theme"])

    return config
