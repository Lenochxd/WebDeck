import os
import sys
import json
import shutil
import time
import subprocess
import requests

from app.utils.show_error import show_error
from app.updater.updater import check_files, compare_versions


def check_for_updates(text):
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
            shutil.copyfile("WD_updater.exe", "update/WD_updater.exe")
            shutil.copytree("lib", "update/lib")

            subprocess.Popen(["update/WD_updater.exe"])

            sys.exit()

    except Exception as e:
        show_error(f"{text['auto_update_error']} \n\n{text['error']}: {e}")


def check_for_updates_loop(text):
    while True:

        with open(".config/config.json", encoding="utf-8") as f:
            config = json.load(f)
        if "auto-updates" in config["settings"].keys():
            if config["settings"]["auto-updates"].lower().strip() == "true":
                check_for_updates(text)
        else:
            config["settings"]["auto-updates"] = "true"
            check_for_updates(text)
        with open(".config/config.json", "w", encoding="utf-8") as json_file:
            json.dump(config, json_file, indent=4)

        time.sleep(3600)