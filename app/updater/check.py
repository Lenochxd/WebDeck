import os
import sys
import json
import shutil
import time
import subprocess
import requests

from .updater import compare_versions, prepare_update_directory
from app.utils.settings.get_config import get_config
from app.utils.show_error import show_error
from app.utils.languages import text
from app.utils.logger import log
from app.utils.args import raw_args


def check_for_updates():
    if not getattr(sys, "frozen", False):
        return
    
    settings = get_config()["settings"]
    
    if os.path.exists("update"):
        shutil.rmtree("update", ignore_errors=True)

    try:
        with open("webdeck/version.json", encoding="utf-8") as f:
            current_version = json.load(f)["versions"][0]["version"]

        update_repo = settings.get('update_repo', 'Lenochxd/WebDeck')
        url = f"https://api.github.com/repos/{update_repo}/releases"
        response = requests.get(url)
        releases = response.json()
        update_channel = settings.get('update_channel', 'stable')

        try:
            latest_release = next(
                (release for release in releases
                if not release["draft"] and
                ((update_channel == 'stable' and not release["prerelease"]) or
                (update_channel == 'beta' and release["prerelease"]))),
                {"tag_name": "v1.0.0"}
            )
        except Exception:
            latest_version = "1.0.0"
        else:
            latest_version = latest_release["tag_name"].replace('v', '')

        if compare_versions(latest_version, current_version) > 0:
            log.info(f"UPDATER: New version available: {latest_version}")
            prepare_update_directory()
            os.chdir("update")
            subprocess.Popen(["update/update.exe"] + raw_args)
            sys.exit()

    except Exception as e:
        log.exception(e, "UPDATER: Error occurred while checking for updates")
        show_error(
            f"{text('auto_update_error')} \n\n{text('error')}: {e}",
            title="WebDeck Updater Error",
            exception=e
        )


def check_for_updates_loop():
    while True:
        config = get_config()
        
        if config["settings"].get("auto-updates", True):
            check_for_updates()

        time.sleep(3600)