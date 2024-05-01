import os
import urllib.request
import zipfile

def check_json_update(config):
    if "background" in config["front"]:
        if type(config["front"]["background"]) == "str" and len(config["front"]["background"]) > 3:
            config["front"]["background"] = [config["front"]["background"]]
        if type(config["front"]["background"]) == "list" and config["front"]["background"] in [[], [""]]:
            config["front"]["background"] = ["#141414"]
    else:
        # Set default background if not present
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
    if "themes" not in config["front"]:
        themes.append(config["front"]["theme"])
        config["front"]["themes"] = themes
    else:
        # check if there's new themes installed
        installed_themes = config["front"]["themes"]
        new_themes = [theme for theme in themes if not any(theme.endswith(name) for name in installed_themes)]
        if new_themes:
            print("new themes:", new_themes)
            config["front"]["themes"].extend(iter(new_themes))

    # Check for deleted themes
    try:
        config["front"]["themes"] = eval(config["front"]["themes"])
    except TypeError:
        pass
    for theme in config["front"]["themes"][:]:
        theme_file = theme.replace('//', '')
        if not os.path.isfile(f"static/themes/{theme_file}"):
            config["front"]["themes"].remove(theme)

    # Check for duplicates
    temporary_list = [theme.replace("//", "") for theme in config["front"]["themes"]]
    duplicates = {
        theme for theme in temporary_list if temporary_list.count(theme) > 1
    }

    # Remove duplicates
    for theme in duplicates:
        while temporary_list.count(theme) > 1:
            temporary_list.remove(theme)
            if f"//{theme}" in config["front"]["themes"]:
                config["front"]["themes"].remove(f"//{theme}")
            if theme in config["front"]["themes"]:
                config["front"]["themes"].remove(theme)

            if theme == config["front"]["theme"]:
                config["front"]["themes"].append(theme)
            else:
                config["front"]["themes"].insert(0, f"//{theme}")
                

    # move the default theme to the bottom
    if os.path.isfile(f'static/themes/{config["front"]["theme"]}'):
        if config["front"]["theme"] in config["front"]["themes"]:
            config["front"]["themes"].remove(config["front"]["theme"])
            
        config["front"]["themes"].append(config["front"]["theme"])

    return config


def download_nircmd():
    url = "https://www.nirsoft.net/utils/nircmd.zip"
    urllib.request.urlretrieve(url, "nircmd.zip")

    with zipfile.ZipFile("nircmd.zip", "r") as zip_ref:
        zip_ref.extractall("")

    os.remove("nircmd.zip")
    os.remove("NirCmd.chm")
    os.remove("nircmdc.exe")