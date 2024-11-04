from cx_Freeze import setup, Executable

import urllib.request
import zipfile
import pathspec
import sys
import os
import json
import time
import uuid

start_time = time.time()

sys.setrecursionlimit(10000)

with open("webdeck/version.json", encoding="utf-8") as f:
    version_info = json.load(f)
    version = version_info["versions"][0]["version"]



def get_ignored_files():
    ignored_files = [
        ".git",
        ".gitignore",
        ".github",
        "build.bat",
        "requirements.txt",
        "tests/*",
        "*.py",
        "!nircmd*.exe",
    ]

    with open(".gitignore", "r") as gitignore_file:
        for line in gitignore_file:
            line = line.strip()
            if line and not line.startswith("#"):
                if line.startswith("\\"):
                    line = line[1:]
                ignored_files.append(line)

    print("IGNORED:", ignored_files)
    return ignored_files

ignored_files = get_ignored_files()


def is_excluded(file_path):
    rel_path = os.path.relpath(file_path)
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignored_files)

    if spec.match_file(rel_path):
        # Check for negation patterns
        negation_spec = pathspec.PathSpec.from_lines("gitwildmatch", [line[1:] for line in ignored_files if line.startswith("!")])
        if negation_spec.match_file(rel_path):
            print(f"NOT EXCLUDED (negation): {file_path}")
            return False
        print(f"EXCLUDED: {file_path}")
        return True

    # print(f"NOT EXCLUDED: {file_path}")
    return False

def get_include_files():
    include_files = []
    for root, dirs, files in os.walk("."):
        # Check if the directory itself is excluded first
        if is_excluded(root):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if not is_excluded(file_path.replace('\\', '/')):
                if file.lower().startswith("nircmd") and "temp" in root:
                    include_files.append((file_path, os.path.join("lib", file)))
                elif file.startswith("README"):
                    if file == "README.md":
                        include_files.append((file_path, os.path.join("docs", "README-en.md")))
                    else:
                        include_files.append((file_path, os.path.join("docs", file)))
                else:
                    include_files.append((file_path, file_path))
    return include_files

def download_nircmd():
    if os.path.isfile("temp/nircmd.exe"):
        return
    
    zippath = "temp/nircmd.zip"
    url = "https://www.nirsoft.net/utils/nircmd.zip"
    urllib.request.urlretrieve(url, zippath)

    with zipfile.ZipFile(zippath, "r") as zip_ref:
        zip_ref.extractall("temp")

    os.remove(zippath)

if __name__ == "__main__":
    download_nircmd()

    build_exe_options = {
        "excludes": ["cx_Freeze", "pathspec"],
        "packages": [],
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
        "include_msvcr": False,
        "include_files": get_include_files(),
    }

    bdist_msi_options = {
        "upgrade_code": f"{{{uuid.uuid4()}}}",
        "add_to_path": True,
        "initial_target_dir": r"[ProgramFilesFolder]\WebDeck",
        "install_icon": "static/icons/icon.ico",
        "summary_data": {
            "author": "webdeck.app",
            "comments": "WebDeck is an open-source app for managing custom shortcuts.",
            "keywords": "WebDeck, remote control, web application",
        }
    }

    base = "Win32GUI" if sys.platform == "win32" else "gui"
    # base = 'console' if sys.platform=='win32' else None
    executables = [
        Executable(
            script="run.py",
            base=base,
            target_name="WebDeck",
            icon="static/icons/icon.ico",
            shortcut_name="WebDeck",
            shortcut_dir="ProgramMenuFolder",
            copyright="WebDeck",
            trademarks="WebDeck",
            manifest=None,
            uac_admin=True,
        ),
        Executable(
            script="app/updater/updater.py",
            base="console",
            target_name="update",
            icon=None,
            shortcut_name="WebDeck Updater",
            shortcut_dir="ProgramMenuFolder",
            copyright="WebDeck",
            trademarks="WebDeck",
            manifest=None,
            uac_admin=True,
        ),
    ]

    setup(
        name="WebDeck",
        description="WebDeck",
        author="webdeck.app",
        author_email="contact.lenoch@gmail.com",
        url="https://webdeck.app/",
        license="GPLv3",
        version=version,
        options={
            "build_exe": build_exe_options,
            "bdist_msi": bdist_msi_options,
        },
        executables=executables,
    )
    

    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    
    print(f"Build done! {minutes}m {seconds}s")
