import os
import json
import requests
import psutil
import subprocess
import time
import ctypes

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
        subprocess.Popen([process_path])
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
    url = "https://raw.githubusercontent.com/LeLenoch/WebDeck/master/static/files/version.json"
    response = requests.get(url)
    data = response.json()
    
    process_names = ["WebDeck.exe", "WD_main.exe"]
    close_processes(process_names)
    
    files_to_update = []
    for version_data in reversed(data["versions"]):
        version = version_data["version"]
        if compare_versions(version, current_version) > 0:
            print(f"New version available: {version}")
            for filename in version_data["updated_files"]:
                files_to_update.append(filename)
            for filename in version_data["deleted_files"]:
                if '.' in filename:
                    os.remove(filename)
                else:
                    os.rmdir(filename)
            current_version = version
    
    update_files = list(set(files_to_update))
    download_and_replace(update_files)

    open_process("WebDeck.exe")

def download_and_replace(file_list):
    base_url = "https://github.com/LeLenoch/WebDeck/raw/master/"
    
    for file_path in file_list:
        url = base_url + file_path
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Updated {file_path}")
        else:
            error(f"Failed to update {file_path}")


with open('static/files/version.json', encoding="utf-8") as f:
    current_version = json.load(f)['versions'][0]['version']
check_updates(current_version)
