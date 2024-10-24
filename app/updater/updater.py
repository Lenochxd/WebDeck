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
from tqdm import tqdm
from app.utils.show_error import show_error
from app.utils.logger import Logger

log = Logger(from_updater=True)


def get_base_dir():
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    if os.path.exists(os.path.join(parent_dir, "WebDeck.exe")):
        return parent_dir
    return current_dir
        
def check_files():
    wd_dir = get_base_dir()
    version_path = os.path.join(wd_dir, "webdeck/version.json")
    temp_json_path = os.path.join(wd_dir, "temp.json")

    # Get version from the versions JSON file
    with open(version_path, encoding="utf-8") as f:
        versions = json.load(f)
        current_version = versions["versions"][0]["version"]

    # Load or initialize the temporary JSON file
    try:
        with open(temp_json_path, encoding="utf-8") as f:
            temp_json = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        temp_json = {}

    temp_json.setdefault("checked-versions", [])

    # Iterate over versions
    for version in reversed(versions["versions"]):
        if version["version"] not in temp_json["checked-versions"]:
            temp_json["checked-versions"].append(version["version"])

            # Handle deleted files
            if "deleted_files" in version:
                for file_entry in version["deleted_files"]:
                    if isinstance(file_entry, str):
                        file_entry = [file_entry, "99.99.99"]

                    file_to_delete, update_limit = file_entry[0], file_entry[1]
                    file_to_delete = os.path.join(wd_dir, file_to_delete)

                    if compare_versions(update_limit, current_version) > 0:
                        try:
                            os.remove(file_to_delete)
                            log.info(f'UPDATER: Deleted {file_to_delete}')
                        except Exception as e:
                            log.exception(e, f"UPDATER: Error deleting {file_to_delete}")

            # Handle moved or renamed files
            files_to_move = version.get("moved_files", []) + version.get("renamed_files", [])
            for move in files_to_move:
                source = os.path.join(wd_dir, move[0])
                destination = os.path.join(wd_dir, move[1])
                update_limit = move[2] if len(move) == 3 else "99.99.99"

                if compare_versions(update_limit, current_version) > 0:
                    try:
                        os.makedirs(os.path.dirname(destination), exist_ok=True)
                        shutil.move(source, destination)
                        log.info(f'Moved {source} -> {destination}')
                    except FileNotFoundError:
                        print(f'File not found: {source}')

    # Save the updated temporary JSON file
    with open(temp_json_path, "w", encoding="utf-8") as f:
        json.dump(temp_json, f, ensure_ascii=False, indent=4)
        

def move_folder_content(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    elements = []
    for root, dirs, files in os.walk(source):
        for name in files:
            elements.append(os.path.join(root, name))
        for name in dirs:
            elements.append(os.path.join(root, name))

    total_elements = len(elements)
    with tqdm(total=total_elements, desc="Moving files") as pbar:
        for element in elements:
            source_path = element
            destination_path = os.path.join(destination, os.path.relpath(element, source))

            if os.path.isfile(source_path):
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.copy2(source_path, destination_path)

            elif os.path.isdir(source_path):
                os.makedirs(destination_path, exist_ok=True)
            
            pbar.update(1)


def close_process(process_name):
    try:
        for proc in psutil.process_iter(["pid", "name"]):
            if process_name.lower() in proc.info["name"].lower():
                try:
                    proc.terminate()
                    proc.wait(timeout=3)
                    print(f"Terminated process {proc.info['name']} with PID {proc.info['pid']}")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
    except Exception as e:
        print(f"Error terminating process with psutil: {e}")
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            processes = wmi.InstancesOf("Win32_Process")
            for process in processes:
                if process.Properties_('Name').Value.lower() == process_name.lower():
                    print(f"Stopping process: {process.Properties_('Name').Value}")
                    result = process.Terminate()
                    if result == 0:
                        print("Process terminated successfully.")
                    else:
                        print("Failed to terminate process.")
        except Exception as e:
            print(f"Error terminating process with WMI: {e}")
            try:
                subprocess.run(f"taskkill /f /IM {process_name}", shell=True, check=True)
                print(f"Process {process_name} terminated using taskkill.")
            except subprocess.CalledProcessError as e:
                print(f"Error terminating process with taskkill: {e}")


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

    if not compare_versions(latest_version, current_version) > 0:
        print("No updates available.")
    else:
        print(f"New version available: {latest_version}")

        close_process("WebDeck.exe")
        for file_url in latest_release["assets"]:
            if (
                file_url["browser_download_url"].endswith("portable.zip")
                and file_url["state"] == "uploaded"
            ):
                download_and_extract(file_url["browser_download_url"])
                break

        # Removing update files
        files_to_remove = [
            os.path.join(update_dir, "WebDeck"),
            os.path.join(update_dir, "WD-update"),
            os.path.join(update_dir, "WD-update.zip")
        ]

        with tqdm(total=len(files_to_remove), desc="Removing update files") as pbar:
            for file_path in files_to_remove:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path, ignore_errors=True)
                    else:
                        os.remove(file_path)
                pbar.update(1)

        # Launch WebDeck.exe from the wd_dir (root) directory
        print("\nRestarting WebDeck.exe")
        os.chdir(wd_dir)
        os.startfile("WebDeck.exe")
        


def download_and_extract(download_url):
    response = requests.get(download_url, stream=True)
    if response.status_code != 200:
        show_error("Failed to download update ZIP file.", title="WebDeck Updater Error")
    else:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        print()
        t = tqdm(total=total_size, unit='iB', unit_scale=True, desc="Downloading")

        with open("WD-update.zip", "wb") as file:
            for chunk in response.iter_content(chunk_size=block_size):
                t.update(len(chunk))
                file.write(chunk)
        t.close()

        if total_size != 0 and t.n != total_size:
            show_error("Failed to download the complete update ZIP file.", title="WebDeck Updater Error")
            return

        with zipfile.ZipFile("WD-update.zip", "r") as zip_ref:
            for file in tqdm(zip_ref.namelist(), desc="Extracting"):
                zip_ref.extract(file, "WD-update")

        source = os.path.join(update_dir, "WD-update/WebDeck")
        destination = wd_dir

        move_folder_content(source, destination)


# TESTING
# def download_and_extract(download_url):
#     shutil.copyfile("E:/Users/81len/Downloads/WD-fake-update.zip", "WD-update.zip")
#
#     with zipfile.ZipFile("WD-update.zip", "r") as zip_ref:
#         zip_ref.extractall("WD-update")
#
#     source = os.path.join(update_dir, "WD-update/WebDeck")
#     destination = wd_dir
#
#     move_folder_content(source, destination)

def prepare_update_directory():
    os.makedirs("update")
    shutil.copyfile("python3.dll", "update/python3.dll")
    shutil.copyfile("python311.dll", "update/python311.dll")
    shutil.copyfile("update.exe", "update/update.exe")
    shutil.copytree("lib", "update/lib")


if __name__ == "__main__" and getattr(sys, "frozen", False):   # This ensures the script only runs when executed as a built executable, not when run as a Python script
    print("Starting updater...")

    wd_dir = get_base_dir()
    update_dir = os.path.join(wd_dir, 'update')
    
    if not os.path.exists(os.path.join(wd_dir, 'WebDeck.exe')):
        show_error("WebDeck.exe not found in the parent directory. The updater is not properly installed.", title="WebDeck Updater Error")
        sys.exit(1)
    
    if not os.getcwd().endswith("update"):
        prepare_update_directory()
        os.chdir("update")
        subprocess.Popen(["update/update.exe"])
        sys.exit()
    

    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    
    version_path = os.path.join(wd_dir, "webdeck/version.json")
    with open(version_path, encoding="utf-8") as f:
        current_version = json.load(f)["versions"][0]["version"]

    check_files()
    check_updates(current_version)