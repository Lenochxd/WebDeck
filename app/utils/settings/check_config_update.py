import os
import json
from app.utils.logger import log


def check_config_update(config):
    config = check_config_hyphen_case(config)
    
    # Rename 'black_theme' to 'dark_theme'
    if "black_theme" in config.get("front", {}):
        config["front"]["dark_theme"] = config["front"].pop("black_theme")
        
    # Rename 'open-settings-in-browser' to 'open_settings_in_integrated_browser'
    if "open_settings_in_browser" in config["settings"]:
        config["settings"]["open_settings_in_integrated_browser"] = config["settings"].pop("open_settings_in_browser")
    
    # Make every key in settings.spotify_api lowercase
    if "spotify_api" in config["settings"]:
        config["settings"]["spotify_api"] = {k.lower(): v for k, v in config["settings"]["spotify_api"].items()}

    # Move allowed_networks to settings.allowed_networks
    if "allowed_networks" in config:
        if "allowed_networks" not in config["settings"]:
            config["settings"]["allowed_networks"] = []
        config["settings"]["allowed_networks"].extend(config["allowed_networks"])
        del config["allowed_networks"]
    
    
    with open("webdeck/config_default.json", "r", encoding="utf-8") as f:
        default_config = json.load(f)

    def update_config_with_defaults(config, default_config):
        for section, section_value in default_config.items():
            if section not in config:
                config[section] = section_value
            elif isinstance(section_value, dict):
                for key, value in section_value.items():
                    if key not in config[section]:
                        config[section][key] = value
                    elif isinstance(value, dict) and key != "buttons":
                        if key not in config[section]:
                            config[section][key] = value
                        else:
                            update_config_with_defaults(config[section][key], value)

    update_config_with_defaults(config, default_config)

    config = check_config_themes(config)
    config = check_config_booleans(config)

    return config


def check_config_themes(config):
    # Get available theme files
    themes = [
        f"//{file_name}"
        for file_name in os.listdir(".config/themes/")
        if file_name.endswith(".css")
    ]
    if "themes" not in config["front"]:
        config["front"]["themes"] = themes
    else:
        # check if there's new themes installed
        installed_themes = config["front"]["themes"]
        new_themes = [theme for theme in themes if not any(theme.endswith(name) for name in installed_themes)]
        if new_themes:
            log.debug(f"New themes found: {new_themes}")
            config["front"]["themes"].extend(iter(new_themes))

    # Check for deleted themes
    try:
        config["front"]["themes"] = eval(config["front"]["themes"])
    except TypeError:
        pass
    for theme in config["front"]["themes"][:]:
        theme_file = theme.replace('//', '')
        if not os.path.isfile(f".config/themes/{theme_file}"):
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

            config["front"]["themes"].insert(0, f"//{theme}")
            
    return config


def check_config_booleans(config):
    for category, settings in config.items():
        for key, value in settings.items():
            
            if isinstance(value, str):
                if value.lower() == "true":
                    config[category][key] = True
                elif value.lower() == "false":
                    config[category][key] = False
                    
            elif isinstance(value, dict):
                for setting_name, setting in value.items():
                    if isinstance(setting, str):
                        if setting.lower() == "true":
                            config[category][key][setting_name] = True
                        elif setting.lower() == "false":
                            config[category][key][setting_name] = False
    return config


def check_config_hyphen_case(config):
    def convert_to_snake_case(text):
        return text.replace('-', '_')

    new_config = {}
    for category, settings in config.items():
        new_category = convert_to_snake_case(category)
        if not isinstance(settings, dict):
            new_config[new_category] = settings
        else:
            new_config[new_category] = {}
            for key, value in settings.items():
                new_key = convert_to_snake_case(key)
                if isinstance(value, dict):
                    new_value = {convert_to_snake_case(k): v for k, v in value.items()}
                else:
                    new_value = value
                new_config[new_category][new_key] = new_value

    # Update background-color to background_color in buttons
    if 'front' in new_config and 'buttons' in new_config['front']:
        for page_name, page_content in new_config['front']['buttons'].items():
            if isinstance(page_content, list):
                for button in page_content:
                    if isinstance(button, dict) and 'background-color' in button:
                        button['background_color'] = button.pop('background-color')

    return new_config