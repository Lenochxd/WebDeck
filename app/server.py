# Standard library imports
import re
import random
import json
import os
import sys
import ipaddress
import ast

# Third-party library imports
from deepdiff import DeepDiff
from PIL import Image
from flask import Flask, request, jsonify, render_template, send_file, make_response
from flask_socketio import SocketIO
from flask_minify import Minify
from engineio.async_drivers import gevent # DO NOT REMOVE
from win32com.client import Dispatch
import easygui

# WebDeck imports
from .on_start import on_start, check_json_update
from .utils.global_variables import set_global_variable, get_global_variable

config, text, commands, local_ip = on_start()
folders_to_create = []
set_global_variable("text", text)
set_global_variable("config", config)

from .utils.themes.parse_themes import parse_themes
from .utils.plugins.load_plugins import load_plugins
from .utils.settings.audio_devices import get_audio_devices
from .utils.settings.gridsize import update_gridsize
from .utils.settings.create_folders import create_folders
from .utils.firewall import fix_firewall_permission, check_firewall_permission
from .utils.load_lang_file import load_lang_file
from .utils.merge_dicts import merge_dicts
from .buttons.usage import get_usage
from .buttons.obs import reload_obs

from .buttons import soundboard
from .buttons import handle_command as command


def save_config(config):
    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    set_global_variable("config", config)
    return config


def print_dict_differences(dict1, dict2):
    diff = DeepDiff(dict1, dict2, ignore_order=True)

    print("Differences found :")
    for key, value in diff.items():
        print(f"Key : {key}")
        print(f"Difference : {value}")
        print("----------------------")
        


# for folder_name, folder_content in config["front"]["buttons"].items():
#     for button in folder_content:
#         if 'action' not in button.keys():
#             button['action'] = {
#                 "touch_start": "click",
#                 "touch_keep": "None",
#                 "touch_end": "none",
#             }


#         if 'image' in button.keys() and not button['image'].strip() == '' and ':' in button['image'] and not button['image'].startswith('http'):
#             button['image'] = button['image'].replace('/', '\\')
#             splitted = button['image'].split('\\')
#             try:
#                 copyfile(button['image'],f'static/files/images/{splitted[-1]}')
#             except Exception:
#                 pass


if getattr(sys, "frozen", False):
    app = Flask(__name__, template_folder='../../../templates', static_folder='../../../static')
else:
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.jinja_env.globals.update(get_audio_devices=get_audio_devices)
if getattr(sys, "frozen", False):
    Minify(app=app, html=True, js=True, cssless=True)
app.config["SECRET_KEY"] = "secret!"

socketio = SocketIO(app)


@app.route("/usage", methods=["POST"])
def usage():
    return jsonify(get_usage())


# Middleware to check request IP address
@app.before_request
def check_local_network():
    remote_ip = request.remote_addr    

    netmask = '255.255.255.0'

    ip_local = ipaddress.IPv4Network(local_ip + '/' + netmask, strict=False)
    ip_remote = ipaddress.IPv4Network(remote_ip + '/' + netmask, strict=False)
    
    # print(f"local IP is: {local_ip}")
    # print(f"remote: {remote_ip}")
    # print(f"IP1: {ip_local} == IP2: {ip_remote} {ip_local == ip_remote}")
    
    # print(f'new connection established: {remote_ip}')
    
    if ip_remote != ip_local:
        # check if in allowed network list in config
        for network in config["allowed_networks"]:
            if ipaddress.IPv4Address(remote_ip) in ipaddress.IPv4Network(network):
                return
            
        return (
            "Unauthorized access: you are not on the same network as the server.",
            403,
        )


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(message)

    return dict(mdebug=print_in_console)


# Function to get all the svgs from the theme file, so we can load them during the loading screen
def get_svgs():
    svgs = []

    with open("static/css/style.css", "r") as f:
        content = f.read()

        # url(...)
        matches = re.findall(r"url\(([^)]+)\)", content)

        for match in matches:
            if match.endswith(".svg"):
                svgs.append(match)

    return svgs


@app.route("/")
def home():
    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)

    new_config = check_json_update(config)
    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(new_config, json_file, indent=4)
    config = new_config

    with open("webdeck/commands.json", encoding="utf-8") as f:
        commands = json.load(f)
        commands, all_func = load_plugins(commands)
        set_global_variable("all_func", all_func)
        
    text = load_lang_file(config['settings']['language'])
    set_global_variable("text", text)
        
    with open("webdeck/version.json", encoding="utf-8") as f:
        versions = json.load(f)
    is_exe = bool(getattr(sys, "frozen", False))

    random_bg = "//"
    while random_bg.startswith("//") == True:
        random_bg = random.choice(config["front"]["background"])
        if random_bg.startswith("**uploaded/"):
            random_bg_path = random_bg.replace("**uploaded/", ".config/user_uploads/")
            if os.path.exists(random_bg_path):
                file_name, extension = os.path.splitext(
                    os.path.basename(random_bg_path)
                )
                random_bg_90_path = f".config/user_uploads/{file_name}-90{extension}"
                if not os.path.exists(random_bg_90_path):
                    try:
                        img = Image.open(random_bg_path)
                        img_rotated = img.rotate(-90, expand=True)
                        file_name, extension = os.path.splitext(
                            os.path.basename(random_bg_path)
                        )
                        img_rotated.save(random_bg_90_path)
                    except Exception as e:
                        print(e)
    print(f"random background: {random_bg}")

    themes = [
        file_name
        for file_name in os.listdir(".config/themes/")
        if file_name.endswith(".css")
    ]
    langs = [
        file_name.replace(".lang", "")
        for file_name in os.listdir("webdeck/translations/")
        if file_name.endswith(".lang")
    ]

    return render_template(
        "index.jinja",
        config=config, themes=themes, parsed_themes=parse_themes(text),
        commands=commands, versions=versions, random_bg=random_bg, usage_example=get_usage(True),
        langs=langs, text=text,
        svgs=get_svgs(), is_exe=is_exe, portrait_rotate=config['front']['portrait-rotate'],
        int=int, str=str, dict=dict, json=json, type=type, eval=eval, open=open,
        isfile=os.path.isfile
    )
    

@app.route("/save_config", methods=["POST"])
def saveconfig():
    global config, folders_to_create, obs_host, obs_port, obs_password, obs

    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)

    # Retrieve form data
    new_config = request.get_json()

    new_height = new_config["front"]["height"]
    new_width = new_config["front"]["width"]
    config = update_gridsize(config, new_height, new_width)
    config["front"]["height"] = new_height
    config["front"]["width"] = new_width

    soundboard_restart = (
        not config["settings"]["soundboard"] == new_config["settings"]["soundboard"]
    )
    obs_reload = not config["settings"]["obs"] == new_config["settings"]["obs"]

    soundboard_start = False
    soundboard_stop = False
    if (
        not config["settings"]["soundboard"]["enabled"]
        == new_config["settings"]["soundboard"]["enabled"]
    ):
        if new_config["settings"]["soundboard"]["enabled"] == "true":
            soundboard_start = True
        else:
            soundboard_stop = True

    config = check_json_update(config)
    new_config = check_json_update(new_config)

    if (
        config["settings"]["windows-startup"].lower().strip() == "false"
        and new_config["settings"]["windows-startup"].lower().strip() == "true"
    ):
        if getattr(sys, "frozen", False):
            dir = (
                os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\Startup"
            )
            path = os.path.join(dir, "WebDeck.lnk")
            target = os.getcwd() + r"\\WebDeck.exe"
            working_dir = os.getcwd()
            icon = os.getcwd() + r"\\WebDeck.exe"

            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = working_dir
            shortcut.IconLocation = icon
            shortcut.save()
    elif (
        config["settings"]["windows-startup"].lower().strip() == "true"
        and new_config["settings"]["windows-startup"].lower().strip() == "false"
    ):
        if getattr(sys, "frozen", False):
            file_path = (
                os.getenv("APPDATA")
                + r"\Microsoft\Windows\Start Menu\Programs\Startup\WebDeck.lnk"
            )
            if os.path.exists(file_path):
                os.remove(file_path)

    config = merge_dicts(config, new_config)
    config = create_folders(config, folders_to_create)
    folders_to_create = []
    config = save_config(config)

    try:
        config["front"]["background"] = config["front"]["background"].replace("['", '["').replace("']", '"]').replace("', '", "','").replace("','", '","')
        config["front"]["background"] = ast.literal_eval(config["front"]["background"])
    except TypeError:
        pass

    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)

    if soundboard_stop:
        soundboard.mic.stop()
    elif soundboard_restart or soundboard_start:
        soundboard.mic.restart()

    if obs_reload:
        obs_host, obs_port, obs_password, obs = reload_obs()

    return jsonify({"success": True})


# Save the config ENTIRELY, it does not merge anything
@app.route("/COMPLETE_save_config", methods=["POST"])
def complete_save_config():
    global folders_to_create
    
    old_height = config["front"]["height"]
    old_width = config["front"]["width"]
    config = request.get_json()
    new_height = config["front"]["height"]
    new_width = config["front"]["width"]

    config = create_folders(config, folders_to_create)
    folders_to_create = []
    config = save_config(config)

    config["front"]["height"] = old_height
    config["front"]["width"] = old_width
    config = update_gridsize(config, new_height, new_width)
    config["front"]["height"] = new_height
    config["front"]["width"] = new_width
    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)

    return jsonify({"success": True})


@app.route("/save_single_button", methods=["POST"])
def save_single_button():
    data = request.get_json()
    button_folder = int(data.get("location_Folder"))
    button_index = int(data.get("location_Id"))
    button_content = data.get("content")

    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)

    button_folderName = list(config["front"]["buttons"])[button_folder]
    print(
        "FETCH /save_single_button -> before :"
        + str(config["front"]["buttons"][button_folderName][button_index])
    )
    config["front"]["buttons"][button_folderName][button_index] = button_content
    print(
        "FETCH /save_single_button -> after  :"
        + str(config["front"]["buttons"][button_folderName][button_index])
    )

    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
        set_global_variable("config", config)

    return jsonify({"success": True})


# Save the config but only the buttons
@app.route("/save_buttons_only", methods=["POST"])
def save_buttons_only():
    global folders_to_create

    # Get current config first
    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)

    # Retrieve form data
    new_config = request.get_json()

    new_config = new_config["front"]["buttons"]

    temp_order_list = [key for key, value in config["front"]["buttons"].items()]

    sorted_buttons = {}
    for folder in temp_order_list:
        sorted_buttons[folder] = new_config.get(folder)

    config["front"]["buttons"] = sorted_buttons
    config = create_folders(config, folders_to_create)
    folders_to_create = []
    config = save_config(config)
    return jsonify({"success": True})


@app.route("/get_config", methods=["GET"])
def get_config():
    global folders_to_create, config

    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)

    config = create_folders(config, folders_to_create)
    folders_to_create = []
    set_global_variable("config", config)

    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
        set_global_variable("config", config)

    return jsonify(config)


@app.route("/upload_folderpath", methods=["POST"])
def upload_folderpath():
    path = easygui.diropenbox()
    if path is None:
        path = ""
        
    return path

@app.route("/upload_filepath", methods=["POST"])
def upload_filepath():
    filetypes = request.args.get("filetypes")
    default = '*'
    if filetypes is not None:
        filetypes = filetypes.split('_')
        filetypes = [f"*{item}" for item in filetypes]
        default = filetypes[0]

    path = easygui.fileopenbox(filetypes=filetypes, default=default)
    if path is None:
        path = ""
        
    return path


@app.route("/upload_file", methods=["POST"])
def upload_file():
    print("request:", request)
    print("request.files:", request.files)
    if "file" not in request.files:
        return jsonify({"success": False, "message": text["no_files_found_error"]})

    uploaded_file = request.files["file"]

    save_path = os.path.join(".config/user_uploads", uploaded_file.filename)
    uploaded_file.save(save_path)

    if request.form.get("info") and request.form.get("info") == "background_image":
        try:
            img = Image.open(save_path)
            img_rotated = img.rotate(-90, expand=True)
            file_name, extension = os.path.splitext(os.path.basename(save_path))
            img_rotated.save(f".config/user_uploads/{file_name}-90{extension}")
        except Exception as e:
            print(e)

    return jsonify({"success": True, "message": text["downloaded_successfully"]})


@app.route("/create_folder", methods=["POST"])
def create_folder():
    global folders_to_create
    data = request.get_json()
    folder_name = data.get("name")
    parent_folder_name = data.get("parent_folder")

    if (
        all(item["name"] != folder_name for item in folders_to_create)
        and folder_name not in config["front"]["buttons"].keys()
    ):
        folders_to_create.append(
            {"name": f"{folder_name}", "parent_folder": f"{parent_folder_name}"}
        )
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


# https://stackoverflow.com/a/70555525/17100464
@app.route("/.config/<string:directory>/<string:filename>", methods=["GET"])
def get_config_file(directory, filename):
    if not directory in ['user_uploads', 'themes']:
        return "Unauthorized", 401
    
    try:
        filename = os.path.basename(filename)  # Sanitize the filename
        file_path = os.path.join(app.root_path.replace('app',''), f".config/{directory}", filename)

        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return make_response(f"File '{filename}' not found.", 404)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)


@socketio.on("connect")
def socketio_connect():
    print("Socketio client connected")
    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)

@socketio.event
def send(data):
    socketio.emit("json_data", data)

@socketio.on("message_from_socket")
def send_data_socketio(message):
    return command(message=message)


@app.route("/send-data", methods=["POST"])
def send_data_route():
    return command(message=request.get_json()["message"])


if (
    config["settings"]["automatic-firewall-bypass"] == "true"
    and check_firewall_permission() == False
):
    fix_firewall_permission()

print('local_ip: ', local_ip)

app.run(
    host=local_ip,
    port=config["url"]["port"],
    debug=config["settings"]["flask-debug"] == "true",
    use_reloader=config["settings"]["flask-debug"] == "false",
)
