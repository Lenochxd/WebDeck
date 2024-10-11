import os
import sys
import json
import shutil
import time
import subprocess
import requests

from app.utils.show_error import show_error
from app.utils.languages import text
from .updater import compare_versions


def check_for_updates():
    if not getattr(sys, "frozen", False):
        return
    
    if os.path.exists("update"):
        shutil.rmtree("update", ignore_errors=True)

    try:
        with open("webdeck/version.json", encoding="utf-8") as f:
            current_version = json.load(f)["versions"][0]["version"]

        url = "https://api.github.com/repos/Lenochxd/WebDeck/releases?per_page=1"
        response = requests.get(url)
        releases = response.json()
        latest_release = next((release for release in releases if not release["draft"]), None)
        latest_version = latest_release["tag_name"].replace('v', '')

        if compare_versions(latest_version, current_version) > 0:
            print(f"New version available: {latest_version}")

            os.makedirs("update")
            shutil.copyfile("python3.dll", "update/python3.dll")
            shutil.copyfile("python311.dll", "update/python311.dll")
            shutil.copyfile("update.exe", "update/update.exe")
            shutil.copytree("lib", "update/lib")

            os.chdir("update")
            subprocess.Popen(["update/update.exe"])

            sys.exit()

    except Exception as e:
        show_error(f"{text('auto_update_error')} \n\n{text('error')}: {e}", title="WebDeck Updater Error")


def check_for_updates_loop():
    while True:
        
        with open(".config/config.json", encoding="utf-8") as f:
            config = json.load(f)
            
        if config["settings"].get("auto-updates", True):
            check_for_updates()

        time.sleep(3600)