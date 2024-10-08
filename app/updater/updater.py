import ctypes
import sys
import os
import shutil
import json
import requests
import psutil
import win32com
import subprocess
import ctypes
import zipfile
from app.utils.show_error import show_error

def check_files(versions_json_path, temp_json_path):
    with open(versions_json_path, encoding="utf-8") as f:
        versions = json.load(f)
        current_version = versions["versions"][0]["version"]
        
    if os.path.isfile(temp_json_path):
        with open(temp_json_path, encoding="utf-8") as f:
            temp_json = json.load(f)
    else:
        temp_json = {"checked-versions": []}
    
    if not "checked-versions" in temp_json.keys():
        temp_json["checked-versions"] = []
        
    for version in reversed(versions["versions"]):
        if not version["version"] in temp_json["checked-versions"]:
            temp_json["checked-versions"].append(version["version"])
            
            if "deleted_files" in version.keys():
                for file_to_delete in version["deleted_files"]:
                    if type(file_to_delete) == "str":
                        file_to_delete = [file_to_delete, "99.99.99"]
                    update_limit = file_to_delete[1] if len(file_to_delete) == 2 else "99.99.99"
                    if compare_versions(update_limit, current_version) > 0:
                        try:
                            os.remove(file_to_delete)
                        except Exception as e:
                            print(e)
                        print(f'deleted {file_to_delete}')

            files_to_move = version.get("moved_files", []) + version.get("renamed_files", [])
            for move in files_to_move:
                source, destination = move[0], move[1]
                update_limit = move[2] if len(move) == 3 else "99.99.99"
                if compare_versions(update_limit, current_version) > 0:
                    try:
                        os.makedirs(os.path.dirname(destination), exist_ok=True)
                        shutil.move(source, destination)
                    except FileNotFoundError:
                        pass
                    print(f'moved {source} -> {destination}')

    with open(temp_json_path, "w", encoding="utf-8") as f:
        json.dump(temp_json, f, ensure_ascii=False, indent=4)
        

def move_folder_content(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for element in os.listdir(source):
        source_path = os.path.join(source, element)
        destination_path = os.path.join(destination, element)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)

        elif os.path.isdir(source_path):
            move_folder_content(source_path, destination_path)


def close_process(process_name):
    try:
        for proc in psutil.process_iter(["pid", "name"]):
            if process_name.lower() in proc.info["name"].lower():
                try:
                    pid = proc.info["pid"]
                    os.kill(pid, psutil.signal.SIGTERM)
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    pass

    except:
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            processes = wmi.InstancesOf("Win32_Process")
            for process in processes:
                if process.Properties_('Name').Value.replace('.exe','').lower().strip() in ["webdeck"]:
                    print(f"Stopping process: {process.Properties_('Name').Value}")
                    result = process.Terminate()
                    if result == 0:
                        print("Process terminated successfully.")
                    else:
                        print("Failed to terminate process.")
        except:
            try:
                subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
            except:
                pass


def compare_versions(version1, version2):
    v1_components = list(map(int, version1.split(".")))
    v2_components = list(map(int, version2.split(".")))

    for v1, v2 in zip(v1_components, v2_components):
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1

    if len(v1_components) > len(v2_components):
        return 1
    elif len(v1_components) < len(v2_components):
        return -1

    return 0


# TESTING
# def compare_versions(version1, version2):
#     return 1


def check_updates(current_version):
    url = "https://api.github.com/repos/Lenochxd/WebDeck/releases?per_page=1"
    response = requests.get(url)
    releases = response.json()
    try:
        latest_release = next(
            (release for release in releases if not release["draft"]), None
        )
    except Exception:
        latest_release = None
    latest_version = "0.1"
    if latest_release is not None and "tag_name" in latest_release:
        latest_version = latest_release["tag_name"].replace("v", "")

    if compare_versions(latest_version, current_version) > 0:
        print(f"New version available: {latest_version}")

        close_process("WebDeck.exe")
        for file_url in latest_release["assets"]:
            if (
                file_url["browser_download_url"].endswith("portable.zip")
                and file_url["state"] == "uploaded"
            ):
                download_and_extract(file_url["browser_download_url"])
                break

        # Remove the WebDeck directory
        print("Removing WebDeck directory")
        update_dir_path = os.path.join(update_dir, "WebDeck")
        shutil.rmtree(update_dir_path, ignore_errors=True)

        # Remove the WD-update directory
        print("Removing WD-update directory")
        update_dir_path = os.path.join(update_dir, "wd-update")
        shutil.rmtree(update_dir_path, ignore_errors=True)

        # Delete the WD-update.zip file
        print("Removing wd-update.zip")
        zip_file_path = os.path.join(update_dir, "wd-update.zip")
        os.remove(zip_file_path)

        # Launch WebDeck.exe from the wd_dir (root) directory
        print("Restarting WebDeck.exe")
        os.chdir(wd_dir)
        os.startfile("WebDeck.exe")
        


def download_and_extract(download_url):
    response = requests.get(download_url, stream=True)
    if response.status_code != 200:
        show_error("Failed to download update ZIP file.", title="WebDeck Updater Error")
    else:
        with open("WD-update.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        with zipfile.ZipFile("WD-update.zip", "r") as zip_ref:
            zip_ref.extractall("WD-update")

        source = os.path.join(update_dir, "WD-update/WebDeck")
        destination = wd_dir

        move_folder_content(source, destination)


# TESTING
# def download_and_extract(download_url):
#     shutil.copyfile("E:/Users/81len/Downloads/WD-fake-update.zip", "WD-update.zip")
#     with zipfile.ZipFile('WD-update.zip', 'r') as zip_ref:
#         zip_ref.extractall(wd_dir)
#
#     source = os.path.join(wd_dir, "WebDeck")
#     destination = wd_dir
#
#     move_folder_content(source, destination)


if __name__ == "__main__" and getattr(sys, "frozen", False):   # This ensures the script only runs when executed as a built executable, not when run as a Python script
    print("Starting updater...")

    wd_dir = os.getcwd()
    if os.path.exists(os.path.join(os.path.dirname(wd_dir), "WebDeck.exe")):
        wd_dir = os.path.dirname(wd_dir)
    update_dir = os.path.join(wd_dir, 'update')
    
    if not os.path.exists(os.path.join(wd_dir, 'WebDeck.exe')):
        show_error("WebDeck.exe not found in the parent directory. The updater is not properly installed.", title="WebDeck Updater Error")
        sys.exit(1)
    
    if not os.getcwd().endswith("update"):
        sys.exit()
    
    version_path = os.path.join(wd_dir, "webdeck/version.json")
    temp_json_path = os.path.join(wd_dir, "temp.json")

    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
        
    with open(version_path, encoding="utf-8") as f:
        current_version = json.load(f)["versions"][0]["version"]

    check_files(version_path, temp_json_path)
    check_updates(current_version)