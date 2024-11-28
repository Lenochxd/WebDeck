import sys
import os
import shutil
import json
import requests
import ctypes
import subprocess
import zipfile
from tqdm import tqdm
from app.utils.exit import exit_program
from app.utils.working_dir import get_base_dir, get_update_dir, chdir_base, chdir_update
from app.utils.settings.get_config import get_config
from app.utils.show_error import show_error
from app.utils.logger import Logger
from app.utils.args import parse_args, raw_args, get_arg

log = Logger(from_updater=True)
config = get_config()
settings = config["settings"]


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
                        log.error(f'File not found: {source}')

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


def compare_versions(version1, version2):
    """
    Compares two version strings in the format 'x.y.z', 'x.y.z-pre', or 'x.y.z-beta'.
    
    Args:
        version1 (str): The first version string to compare.
        version2 (str): The second version string to compare.
    
    Returns:
        int: 
            1 if version1 is greater than version2,
           -1 if version1 is less than version2,
            0 if both versions are equal.
    """
    def parse_version(version):
        if version.endswith("-pre"):
            return list(map(int, version[:-4].split("."))), "pre"
        elif version.endswith("-beta"):
            return list(map(int, version[:-5].split("."))), "beta"
        return list(map(int, version.split("."))), None
    
    v1_components, v1_suffix = parse_version(version1)
    v2_components, v2_suffix = parse_version(version2)
    
    for v1, v2 in zip(v1_components, v2_components):
        if v1 != v2:
            return 1 if v1 > v2 else -1
    
    if len(v1_components) != len(v2_components):
        return 1 if len(v1_components) > len(v2_components) else -1
    
    suffix_order = {"pre": -1, "beta": -1, None: 0}
    return suffix_order[v1_suffix] - suffix_order[v2_suffix]


def check_updates(current_version):
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

    if not compare_versions(latest_version, current_version) > 0:
        log.info("No updates available.")
    else:
        log.info(f"New version available: {latest_version}")

        exit_program(force=True)
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
        log.success("\nRestarting WebDeck.exe")
        os.chdir(wd_dir)
        os.startfile("WebDeck.exe", " ".join(raw_args))
        


def download_and_extract(download_url):
    response = requests.get(download_url, stream=True)
    if response.status_code != 200:
        show_error(
            f"Failed to download update ZIP file.\n\n{response.json()}",
            title="WebDeck Updater Error"
        )
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
            infos = {
                "Response": response.json(),
                "Downloaded": t.n,
                "Expected": total_size,
                "Difference": total_size - t.n,
                "Percentage": (t.n / total_size) * 100,
            }
            show_error(
                f"Failed to download the complete update ZIP file.\n\n{infos}",
                title="WebDeck Updater Error"
            )
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
    current_dir = os.getcwd()
    chdir_base()
    os.makedirs("update", exist_ok=True)

    files_to_copy = [
        "update.exe"
    ]
    # Copy all python3*.dll files
    for file in os.listdir():
        if file.startswith("python3") and file.endswith(".dll"):
            files_to_copy.append(file)

    for src in files_to_copy:
        dst = os.path.join("update", src)
        if not os.path.exists(dst):
            shutil.copyfile(src, dst)

    shutil.copytree("lib", "update/lib", dirs_exist_ok=True)

    os.chdir(current_dir)

def needs_admin_permissions():
    test_file = os.path.join(get_base_dir(), "test_admin.txt")
    try:
        with open(test_file, "w") as f:
            f.write("This is a test.")
        os.remove(test_file)
        
        # Test making an "update" directory and copying python3.dll in it
        update_dir = os.path.join(get_base_dir(), "update")
        os.makedirs(update_dir, exist_ok=True)
        python_dll_path = os.path.join(get_base_dir(), "python3.dll")
        shutil.copy(python_dll_path, update_dir)
        
        return False
    except PermissionError:
        return True
    except Exception as e:
        log.error(f"Unexpected error during admin permission check: {e}")
        return True

def request_admin_permissions():
    if get_arg('no_admin'):
        log.info("Skipping admin permissions request due to '--no-admin' argument.")
        return

    if not ctypes.windll.shell32.IsUserAnAdmin():
        log.info("Asking for admin permissions...")
        if os.path.exists(os.path.join(get_update_dir(), "update.exe")):
            log.info("Starting update.exe with admin privileges...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", os.path.join(get_update_dir(), "update.exe"), " ".join(raw_args), None, 1)
        else:
            log.info("Starting current script with admin privileges...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}" {" ".join(raw_args)}', None, 1)
        sys.exit()


if __name__ == "__main__" and getattr(sys, "frozen", False):   # This ensures the script only runs when executed as a built executable, not when run as a Python script
    log.info("Starting updater...")
    
    parse_args()
    
    wd_dir = get_base_dir()
    update_dir = os.path.join(wd_dir, 'update')
    
    chdir_update()
    if not os.getcwd().endswith("update"):
        log.info("Preparing update directory...")

        if needs_admin_permissions():
            request_admin_permissions()

        prepare_update_directory()
        log.info("Launching update.exe...")
        
        update_exe_path = os.path.join(get_base_dir(), "update/update.exe")
        subprocess.Popen([update_exe_path] + raw_args)
        
        sys.exit()
    
    if needs_admin_permissions():
        request_admin_permissions()
    
    version_path = os.path.join(wd_dir, "webdeck/version.json")
    with open(version_path, encoding="utf-8") as f:
        current_version = json.load(f)["versions"][0]["version"]

    check_files()
    check_updates(current_version)