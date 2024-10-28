# Standard library imports
import re
import random
import json
import os
import sys
import ipaddress
import ast
import logging

# Third-party library imports
from PIL import Image
from werkzeug.serving import make_server
from flask import Flask, request, jsonify, render_template, send_file, make_response
from flask.wrappers import Response
from flask_socketio import SocketIO
from flask_minify import Minify
from engineio.async_drivers import gevent # DO NOT REMOVE
from win32com.client import Dispatch
import easygui

# WebDeck imports
from .on_start import on_start, check_config_update
from .utils.global_variables import set_global_variable, get_global_variable

config, commands, local_ip = on_start()
folders_to_create = []
set_global_variable("config", config)

from app.tray import change_tray_language, change_server_state
from .utils.themes.parse_themes import parse_themes
from .utils.plugins.load_plugins import load_plugins
from .utils.working_dir import get_base_dir
from .utils.load_config import get_port
from .utils.settings.save_config import save_config
from .utils.settings.audio_devices import get_audio_devices
from .utils.settings.gridsize import update_gridsize
from .utils.settings.create_folders import create_folders
from .utils.firewall import fix_firewall_permission, check_firewall_permission
from .utils.languages import text, set_default_language, get_languages_info, get_language
from .utils.logger import log
from .utils.merge_dicts import merge_dicts
from .buttons.usage import get_usage
from .buttons.obs import reload_obs
from .buttons import soundboard
from .buttons import handle_command as command


change_server_state(0)  # Tray icon: server loading


base_dir = get_base_dir()
template_folder = os.path.join(base_dir, 'templates')
static_folder = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

logging.getLogger("werkzeug").disabled = True
app.jinja_env.globals.update(
    get_audio_devices=get_audio_devices,
    mdebug=log.debug
)
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
    """
    Checks if the remote IP address of the incoming request is within the same local network
    as the server or within the allowed networks specified in the configuration.
    The function compares the remote IP address with the server's local IP address using a 
    specified netmask. If the remote IP is not within the same network, it checks if the 
    remote IP is within any of the allowed networks defined in the configuration settings.
    
    Returns:
        None: If the remote IP is within the same network or an allowed network.
        tuple: A tuple containing an error message and an HTTP status code 403 if the remote 
               IP is not authorized.
    """
    
    remote_ip = request.remote_addr    

    netmask = '255.255.255.0'

    ip_local = ipaddress.IPv4Network(local_ip + '/' + netmask, strict=False)
    ip_remote = ipaddress.IPv4Network(remote_ip + '/' + netmask, strict=False)
    
    # log.debug(f"Local IP is: {local_ip}")
    # log.debug(f"Remote IP is: {remote_ip}")
    # log.debug(f"IP1: {ip_local} == IP2: {ip_remote} -> {ip_local == ip_remote}")
    # log.info(f"New connection established from: {remote_ip}")
    
    if ip_remote != ip_local:
        # check if in allowed network list in config
        for network in config["settings"].get("allowed_networks", []):
            if ipaddress.IPv4Address(remote_ip) in ipaddress.IPv4Network(network):
                return
            
        return (
            "Unauthorized access: you are not on the same network as the server.",
            403,
        )

@app.after_request
def after_request(response):
    if request.path != "/usage":
        log.httprequest(request, response)
    return response


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

    new_config = check_config_update(config)
    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(new_config, json_file, indent=4)
    config = new_config

    with open("webdeck/commands.json", encoding="utf-8") as f:
        commands = json.load(f)
        commands, all_func = load_plugins(commands)
        set_global_variable("all_func", all_func)
        
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
                        log.exception(e, f"Failed to rotate image {random_bg_path}")
    log.debug(f"Selected random background image: {random_bg}")

    themes = [
        file_name
        for file_name in os.listdir(".config/themes/")
        if file_name.endswith(".css")
    ]

    return render_template(
        "index.jinja",
        config=config, themes=themes, parsed_themes=parse_themes(),
        commands=commands, versions=versions, random_bg=random_bg, usage_example=get_usage(True),
        langs=get_languages_info(), svgs=get_svgs(), is_exe=is_exe, portrait_rotate=config['front']['portrait_rotate'],
        int=int, str=str, dict=dict, json=json, type=type, eval=eval, open=open,
        isfile=os.path.isfile, text=text, get_language=get_language,
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
    
    language_changed = not config["settings"]["language"] == new_config["settings"]["language"]

    soundboard_start = False
    soundboard_stop = False
    if (
        not config["settings"]["soundboard"]["enabled"]
        == new_config["settings"]["soundboard"]["enabled"]
    ):
        soundboard_start = new_config["settings"]["soundboard"]["enabled"]
        soundboard_stop = not soundboard_start

    config = check_config_update(config)
    new_config = check_config_update(new_config)

    if (
        config["settings"]["windows_startup"] == False
        and new_config["settings"]["windows_startup"] == True
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
        config["settings"]["windows_startup"] == True
        and new_config["settings"]["windows_startup"] == False
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

    if language_changed:
        set_default_language(new_config["settings"]["language"])
        change_tray_language(new_config["settings"]["language"])

    log.success("Config saved successfully")
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

    log.success("Config saved successfully")
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
    log.debug(
        "FETCH /save_single_button -> before :"
        + str(config["front"]["buttons"][button_folderName][button_index])
    )
    config["front"]["buttons"][button_folderName][button_index] = button_content
    log.debug(
        "FETCH /save_single_button -> after  :"
        + str(config["front"]["buttons"][button_folderName][button_index])
    )

    with open(".config/config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
        set_global_variable("config", config)

    log.success("Button saved successfully")
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
    
    log.success("Buttons saved successfully")
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
    log.debug(f"request: {request}")
    log.debug(f"request.files: {request.files}")
    if "file" not in request.files:
        log.error("No files were found in the request.")
        return jsonify({"success": False, "message": text("no_files_found_error")})

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
            log.exception(e, "Failed to rotate image during upload")

    log.success(f"File '{uploaded_file.filename}' uploaded successfully")
    return jsonify({"success": True, "message": text("downloaded_successfully")})


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
        log.info(f"Folder '{folder_name}' is in the queue to be created")
        return jsonify({"success": True})
    else:
        log.error("Folder already exists")
        return jsonify({"success": False, "message": "Folder already exists"})


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
        log.exception(e, f"An error occurred while trying to get the file '{file_path}'")
        return make_response(f"Error: {str(e)}", 500)


@socketio.on("connect")
def socketio_connect():
    log.info("Socketio client connected")
    with open(".config/config.json", encoding="utf-8") as f:
        config = json.load(f)

@socketio.event
def send(data):
    socketio.emit("json_data", data)

@socketio.on("message_from_socket")
def send_data_socketio(message):
    try:
        result = command(message=message)
    except Exception as e:
        log.exception(e, "An error occurred while handling a command")
        return jsonify({"success": False, "message": str(e)})
    
    if result is False:
        socketio.emit("json_data", {"success": False})
    elif isinstance(result, Response):
        response_data = {
            "status_code": result.status_code,
            "headers": dict(result.headers),
            "data": result.get_json() if result.is_json else result.get_data(as_text=True)
        }
        socketio.emit("json_data", response_data)
    elif not isinstance(result, dict):
        socketio.emit("json_data", {"success": True})
    else:
        socketio.emit("json_data", result)

@app.route("/send-data", methods=["POST"])
def send_data_route():
    try:
        result = command(message=request.get_json()["message"])
    except Exception as e:
        log.exception(e, "An error occurred while handling a command")
        return jsonify({"success": False, "message": str(e)})
    
    if result is False:
        return jsonify({"success": False})
    elif isinstance(result, Response):
        return result
    elif not isinstance(result, dict):
        return jsonify({"success": True})
    
    return jsonify(result)


@app.errorhandler(Exception)
def handle_exception(e):
    log.exception(e, "An error occurred during a request")
    if not config["settings"].get("flask_debug"):
        response = jsonify({"success": False, "message": str(e)})
        response.status_code = 500
        return response


if (
    config["settings"]["automatic_firewall_bypass"] == True
    and check_firewall_permission() == False
):
    fix_firewall_permission()

log.info(f"Local IP address detected: {local_ip}")

def run_server():
    change_server_state(1)
    if config["settings"].get("server") == "werkzeug" and not getattr(sys, "frozen", False):
        server = make_server(local_ip, get_port(), app)
        server.serve_forever()
    else:
        app.run(
            host=local_ip,
            port=get_port(),
            debug=config["settings"].get("flask_debug"),
            use_reloader=config["settings"].get("flask_reloader", False),
        )