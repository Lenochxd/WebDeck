import ctypes
import sys
import os
import shutil
import json
import requests
import psutil
import subprocess
import ctypes
import zipfile

def error(message):
    print(message)
    ctypes.windll.user32.MessageBoxW(None, message, u"WebDeck Updater Error", 0)

def close_processes(process_names):
    for process_name in process_names:
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if process_name.lower() in proc.info['name'].lower():
                    try:
                        pid = proc.info['pid']
                        os.kill(pid, psutil.signal.SIGTERM)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
        except:
            try:
                wmi = win32com.client.GetObject("winmgmts:")
                processes = wmi.InstancesOf("Win32_Process")
                for process in processes:
                    if process.Properties_('Name').Value.replace('.exe','').lower().strip() in ["wd_main","wd_start","nircmd","webdeck"]:
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
                    

def open_process(process_path):
    try:
        subprocess.Popen(process_path, shell=True)
    except Exception as e:
        error(f"Error reopening process: {e}")

def compare_versions(version1, version2):
    v1_components = list(map(int, version1.split('.')))
    v2_components = list(map(int, version2.split('.')))

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
    latest_release = next((release for release in releases if not release["draft"]), None)
    latest_version = latest_release["tag_name"].replace('v', '')
    
    if compare_versions(latest_version, current_version) > 0:
        print(f"New version available: {latest_version}")

        if os.path.exists("WebDeck-update"):
            open_process("WebDeck.exe")
            shutil.rmtree("WebDeck-update")
            if os.path.exists("WebDeck-update.zip"):
                os.remove("WebDeck-update.zip")
        else:

            process_names = ["WebDeck.exe", "WD_main.exe"]
            close_processes(process_names)
            for file_url in latest_release["assets"]:
                if file_url["browser_download_url"].endswith('portable.zip') and file_url["state"] == "uploaded":
                    download_and_extract(file_url["browser_download_url"])
                    break
                    
            delete_files = []
            try:
                version_json_url = "https://raw.githubusercontent.com/Lenochxd/WebDeck/master/static/files/version.json"
                for version in version_json_url.json():
                    if version['version'] == latest_version and "deleted_files" in version:
                        delete_files = version["deleted_files"]
                        break
            except Exception:
                pass
                    
            for filename in delete_files:
                if os.path.exists(filename):
                    if os.path.isfile(filename):
                        os.remove(filename)
                    elif os.path.isdir(filename):
                        os.rmdir(filename)

            replace_files()

            open_process("WebDeck.exe")

def download_and_extract(download_url):
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open('WebDeck-update.zip', 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        with zipfile.ZipFile('WebDeck-update.zip', 'r') as zip_ref:
            zip_ref.extractall('WebDeck-update')
        return
    else:
        error("Failed to download update ZIP file.")

#TESTING
# def download_and_extract(download_url):
#     shutil.copyfile("E:/Users/81len/Downloads/WebDeck-fake-update.zip", "WebDeck-update.zip")
#     with zipfile.ZipFile('WebDeck-update.zip', 'r') as zip_ref:
#         zip_ref.extractall('WebDeck-update')
#     return

def replace_files():
    # Move files and folders from WebDeck-update/WebDeck to the wd_dir directory
    print('Moving static/updates/WebDeck-update/WebDeck to root')
    update_dir = os.path.join(current_dir, "WebDeck-update", "WebDeck")
    for root, _, files in os.walk(update_dir):
        for item in files:
            source = os.path.join(root, item)
            relative_path = os.path.relpath(source, update_dir)
            destination = os.path.join(wd_dir, relative_path)
            try:
                os.makedirs(os.path.dirname(destination), exist_ok=True)
                shutil.move(source, destination)
            except (PermissionError, shutil.Error) as e:
                print(e)

    # Remove the WebDeck-update directory
    print('Removing WebDeck-update directory')
    update_dir_path = os.path.join(current_dir, "WebDeck-update")
    shutil.rmtree(update_dir_path, ignore_errors=True)

    # Delete the WebDeck-update.zip file
    zip_file_path = os.path.join(current_dir, "WebDeck-update.zip")
    os.remove(zip_file_path)
    print('WebDeck-update.zip deleted')

    # Launch WebDeck.exe from the wd_dir (root) directory
    print('Restarting WebDeck.exe')
    exe_path = os.path.join(wd_dir, "WebDeck.exe")
    os.system(exe_path)


if __name__ == "__main__":
    print('Starting updater...')
    
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()
    
    current_dir = os.path.abspath(os.path.dirname(__file__))
    wd_dir = os.path.abspath(os.path.join(current_dir, *([".."] * 2)))
    version_path = os.path.join(wd_dir, 'static/files/version.json')
    
    with open(version_path, encoding="utf-8") as f:
        current_version = json.load(f)['versions'][0]['version']
        
    check_updates(current_version)