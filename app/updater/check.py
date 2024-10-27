import os
import sys
import json
import shutil
import time
import subprocess
import requests

from app.utils.load_config import load_config
from app.utils.show_error import show_error
from app.utils.languages import text
from app.utils.logger import log
from .updater import compare_versions, prepare_update_directory


def check_for_updates():
    if not getattr(sys, "frozen", False):
        return
    
    if os.path.exists("update"):
        shutil.rmtree("update", ignore_errors=True)

    try:
        with open("webdeck/version.json", encoding="utf-8") as f:
            current_version = json.load(f)["versions"][0]["version"]

        update_repo = load_config().get('update_repo', 'Lenochxd/WebDeck')
        url = f"https://api.github.com/repos/{update_repo}/releases?per_page=1"
        response = requests.get(url)
        releases = response.json()
        latest_release = next((release for release in releases if not release["draft"]), None)
        latest_version = latest_release["tag_name"].replace('v', '')

        if compare_versions(latest_version, current_version) > 0:
            log.info(f"UPDATER: New version available: {latest_version}")
            prepare_update_directory()
            os.chdir("update")
            subprocess.Popen(["update/update.exe"])
            sys.exit()

    except Exception as e:
        log.exception(e, "UPDATER: Error occurred while checking for updates")
        show_error(f"{text('auto_update_error')} \n\n{text('error')}: {e}", title="WebDeck Updater Error")


def check_for_updates_loop():
    while True:
        
        with open(".config/config.json", encoding="utf-8") as f:
            config = json.load(f)
            
        if config["settings"].get("auto-updates", True):
            check_for_updates()

        time.sleep(3600)