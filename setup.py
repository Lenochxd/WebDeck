from cx_Freeze import setup, Executable

build_options = {
    "excludes": ["cx_Freeze", "pathspec"],
    "packages": ["webdeck", "app", "static", "templates"],
    "zip_exclude_packages": [
        "_sounddevice_data",
        "_soundfile",
        "_soundfile_data",
        "jaraco",
        "numpy",
        "pygame",
        "soundfile",
        "python-vlc",
        "vlc",
    ],
    "zip_include_packages": "*",
}

import urllib.request
import zipfile
import pathspec
import sys
import os
import json
import shutil
import time


start_time = time.time()

sys.setrecursionlimit(10000)

base = "Win32GUI" if sys.platform == "win32" else None
# base = 'console' if sys.platform=='win32' else None
executables = [
    Executable("run.py", base=base, target_name="WebDeck", icon="static/icons/icon.ico"),
    Executable("app/updater/updater.py", base="console", target_name="update"),
]

with open("webdeck/version.json", encoding="utf-8") as f:
    version_info = json.load(f)
    version = version_info["versions"][0]["version"]

setup(
    name="WebDeck",
    description="WebDeck",
    author="bishokus.fr",
    version=version,
    options={"build_exe": build_options},
    executables=executables,
)



def get_ignored_files():
    ignored_files = [
        ".git",
        ".github",
        ".vscode",
        "__pycache__",
        "%.html%WebDeck",
        "WebDeck.exe",
        "update.exe",
        "build",
        "build.bat",
        "requirements.txt",
        "temp",
        "tests/*",
        "README*",
        "*.py",
    ]

    with open(".gitignore", "r") as gitignore_file:
        for line in gitignore_file:
            line = line.strip()
            if line and not line.startswith("#"):
                if line.startswith("\\"):
                    line = line[1:]
                if line != "*copy.*":
                    ignored_files.append(line)

    print("IGNORED:", ignored_files)
    return ignored_files

def is_excluded(file_path, ignored_files):
    rel_path = os.path.relpath(file_path)
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignored_files)

    if spec.match_file(rel_path):
        print(f"EXCLUDED: {file_path}")
        return True

    print(f"NOT EXCLUDED: {file_path}")
    return False

def copy_files(script_dir, target_dir, ignored_files):
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        
        if os.path.isdir(item_path):
            if not is_excluded(item_path, ignored_files):
                for root, _, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = file_path.replace(f"{script_dir}\\", "")
                        
                        if not is_excluded(relative_path, ignored_files):
                            target_file_path = os.path.join(target_dir, os.path.relpath(file_path, script_dir))
                            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                            shutil.copy(file_path, target_file_path)
                            print(f"copying {file_path} -> {target_file_path}")
        else:
            if not is_excluded(item_path, ignored_files):
                shutil.copy(item_path, target_dir)
                print(f"copying {item_path} -> {target_dir}")

def download_nircmd():
    zippath = "temp/nircmd.zip"
    url = "https://www.nirsoft.net/utils/nircmd.zip"
    urllib.request.urlretrieve(url, zippath)

    with zipfile.ZipFile(zippath, "r") as zip_ref:
        zip_ref.extractall("temp")

    os.remove(zippath)

def copy_nircmd(script_dir, target_dir):
    if not os.path.isfile("temp/nircmd.exe"):
        download_nircmd()

    lib_dir = os.path.join(target_dir, "lib")
    os.makedirs(lib_dir, exist_ok=True)
    for file in ["nircmd.exe", "nircmdc.exe", "NirCmd.chm"]:
        file_path = os.path.join(script_dir, f"temp/{file}")
        target_file_path = os.path.join(lib_dir, file)
        shutil.copy(file_path, target_file_path)
        print(f"copying {file_path} -> {target_file_path}")

def copy_readmes(script_dir, target_dir):
    docs_dir = os.path.join(target_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        
        if os.path.isfile(item_path) and item.startswith("README"):
            target_file_path = os.path.join(docs_dir, item)
            shutil.copy(item_path, target_file_path)
            print(f"Copying {item_path} -> {target_file_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(script_dir, "build")

    if os.path.exists(build_dir):
        first_folder = next(
            entry for entry in os.listdir(build_dir) if os.path.isdir(os.path.join(build_dir, entry))
        )
        target_dir = os.path.join(build_dir, first_folder)

        ignored_files = get_ignored_files()
        copy_files(script_dir, target_dir, ignored_files)
        copy_nircmd(script_dir, target_dir)
        copy_readmes(script_dir, target_dir)


main()


end_time = time.time()
elapsed_time = end_time - start_time
minutes, seconds = divmod(int(elapsed_time), 60)

print(f"Build done! {minutes}m {seconds}s")
