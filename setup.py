from cx_Freeze import setup, Executable

import urllib.request
import zipfile
import pathspec
import sys
import os
import subprocess
import shutil
import json
import time
import uuid

start_time = time.time()

sys.setrecursionlimit(10000)

with open("resources/version.json", encoding="utf-8") as f:
    version_info = json.load(f)
    version = version_info["versions"][0]["version"]

app_description_short = "WebDeck is an open-source software that provides a customizable virtual control deck."
app_description_long = (
    "WebDeck is an open-source virtual control deck that launch applications and manage system functions"
    "from a customizable web-based interface. Designed for flexibility, it adapts to various workflows,"
    "making it a powerful tool for productivity and control."
)


def get_ignored_files():
    ignored_files = [
        ".git",
        ".gitignore",
        ".github",
        "build.bat",
        "build.sh",
        "requirements.txt",
        "tests/*",
        "*.py",
    ]

    if sys.platform == "win32":
        ignored_files.append("!nircmd*.exe")

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
        # print(f"EXCLUDED: {file_path}")
        return True

    # print(f"NOT EXCLUDED: {file_path}")
    return False

missing_dependencies = []
dependencies = [
    "xdotool",       # /superAltF4
    "copyq",         # /clipboard
    "xclip",         # /clearclipboard
    "libnotify",     # /colorpicker (notify-send)
    "libnotify-bin", # /colorpicker (notify-send) (Debian based)
]
def get_include_files():
    include_files = []
    for root, dirs, files in os.walk("."):
        # Check if the directory itself is excluded first
        if is_excluded(root):
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if not is_excluded(file_path.replace('\\', '/')):
                destination_path = file_path
                if sys.platform == "win32" and file.lower().startswith("nircmd") and "temp" in root:
                    destination_path = os.path.join("lib", file)
                elif file.startswith("README"):
                    destination_path = os.path.join("docs", "README-en.md") if file == "README.md" else os.path.join("docs", file)
                
                include_files.append((file_path, destination_path))
    
    # Include necessary dependencies for Linux
    if sys.platform != "win32":
        for dep in dependencies:
            result = subprocess.run(["which", dep], capture_output=True, text=True)
            if result.returncode == 0:
                dep_path = result.stdout.strip()
                include_files.append((dep_path, os.path.join("lib", os.path.basename(dep_path))))
            else:
                missing_dependencies.append(dep)
                print(f"Warning: {dep} not found in system path.")
        
        # Fix for missing Tcl/Tk libraries on some systems
        if not os.environ.get('TCL_LIBRARY') or not os.environ.get('TK_LIBRARY'):
            tcl_path = subprocess.check_output(["which", "tclsh"]).decode().strip()
            if not tcl_path:
                print("error: tclsh not found in system path. Please install Tcl/Tk.")
                sys.exit(1)
            
            tcl_lib_dir = os.path.join(os.path.dirname(tcl_path), "..", "lib")
            tcl_library = os.path.join(tcl_lib_dir, "tcl8.6")
            tk_library = os.path.join(tcl_lib_dir, "tk8.6")

            if not os.path.exists(tcl_library) or not os.path.exists(tk_library):
                tcl_library = os.path.join(tcl_lib_dir, "tcltk")
                tk_library = tcl_library

            os.environ['TCL_LIBRARY'] = tcl_library
            os.environ['TK_LIBRARY'] = tk_library
            include_files.append((os.environ['TCL_LIBRARY'], os.path.join("lib", os.path.basename(tcl_library))))
            include_files.append((os.environ['TK_LIBRARY'], os.path.join("lib", os.path.basename(tk_library))))

        # Fix for missing libpng libraries on some systems
        try:
            libpng_path = subprocess.check_output(["which", "libpng16.so"], stderr=subprocess.STDOUT).decode().strip()
            include_files.append((libpng_path, os.path.join("lib", "libpng16.so")))
        except subprocess.CalledProcessError:
            print("Warning: libpng16 not found in system path.")
        
        try:
            libpng_path = subprocess.check_output(["which", "libpng15.so"], stderr=subprocess.STDOUT).decode().strip()
            include_files.append((libpng_path, os.path.join("lib", "libpng15.so")))
        except subprocess.CalledProcessError:
            print("Warning: libpng15 not found in system path.")
    
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

def sign_executable(file_path):
    if sys.platform == "win32":
        signtool_path = r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe"
        timestamp_url = "http://timestamp.digicert.com"
        command = [
            signtool_path,
            "sign",
            "/a",
            "/fd", "SHA256",
            "/tr", timestamp_url,
            "/td", "SHA256",
            file_path
        ]
    else:
        command = ["echo", "Skipping signing on non-Windows platforms"]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to sign {file_path}: {result.stderr}")
    else:
        if sys.platform == "win32":
            print(f"Successfully signed {file_path}")

def zip_build(build_dir):
    # Create a temporary directory outside the build directory to hold the build directory with the desired structure
    temp_dir = os.path.join("temp", "PortableBuild")
    if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    # Move the build directory into the temporary directory
    shutil.copytree(build_dir, temp_dir, dirs_exist_ok=True)

    # Rename the directory inside PortableBuild to "WebDeck"
    final_dir = os.path.join("temp", "PortableBuild")
    inner_dir = os.path.join(final_dir, os.listdir(final_dir)[0])
    new_inner_dir = os.path.join(final_dir, "WebDeck")
    # Ensure the path doesn't exist before creating it
    if os.path.exists(new_inner_dir):
        shutil.rmtree(new_inner_dir)
    os.rename(inner_dir, new_inner_dir)

    # Create an archive of the temporary directory
    if sys.platform == "win32":
        archive_name = 'WebDeck-win-amd64'
        zip_file = shutil.make_archive(archive_name, 'zip', final_dir)
    else:
        arch = subprocess.check_output(["uname", "-m"]).decode().strip()
        archive_name = f'WebDeck-linux-{arch}'
        zip_file = shutil.make_archive(archive_name, 'gztar', final_dir)

    # Move the zip file to the /dist directory
    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    shutil.move(zip_file, os.path.join(dist_dir, os.path.basename(zip_file)))

    # Remove the PortableBuild directory
    shutil.rmtree(final_dir)

    print(f"Portable build zipped as '{os.path.join(dist_dir, os.path.basename(zip_file))}'")


if __name__ == "__main__":
    if sys.platform == "win32":
        download_nircmd()

    build_options = {
        "excludes": ["cx_Freeze", "pathspec"],
        "packages": [
            "tkinter",
            "Xlib" if sys.platform != "win32" else None,
            "pynput.keyboard._xorg" if sys.platform != "win32" else None,
            "pynput.mouse._xorg" if sys.platform != "win32" else None,
        ],
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
            "customtkinter",
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
            "comments": app_description_short,
            "keywords": "WebDeck, remote control, web application",
        }
    }

    bdist_rpm_options = {
        "distribution_name": "WebDeck",
        "packager": "Lenoch <contact.lenoch@gmail.com>",
        "vendor": "webdeck.app",
        "icon": "static/icons/icon.xpm",
        "group": "System/Utilities",
        # "requires": ["python3", "python3-tk", "gtk-update-icon-cache"] + dependencies,
        "requires": dependencies + [
            "libayatana-appindicator-gtk3", # pystray
            "portaudio-devel", # pyaudio
        ],
        "build_requires": dependencies,
        "post_install": "resources/build/rpm/post_install.sh",
        "post_uninstall": "resources/build/rpm/post_uninstall.sh",
        "no_autoreq": True,
    }

    base = "Win32GUI" if sys.platform == "win32" else None
    # base = 'console' if sys.platform=='win32' else None
    executables = [
        Executable(
            script="run.py",
            base=base,
            target_name="WebDeck" if sys.platform == "win32" else "webdeck",
            icon="static/icons/icon.ico" if sys.platform == "win32" else "static/icons/icon.png",
            shortcut_name="WebDeck",
            shortcut_dir="ProgramMenuFolder" if sys.platform == "win32" else None,
            copyright="WebDeck",
            trademarks="WebDeck",
            manifest=None,
            uac_admin=False,
        ),
        Executable(
            script="app/updater/updater.py",
            base="console",
            target_name="update" if sys.platform == "win32" else "webdeck-update",
            icon=None,
            shortcut_name="WebDeck Updater",
            shortcut_dir="ProgramMenuFolder" if sys.platform == "win32" else None,
            copyright="WebDeck",
            trademarks="WebDeck",
            manifest=None,
            uac_admin=False,
        ) if sys.platform == 'win32' else None,
    ]
    executables = [e for e in executables if e is not None]
    
    setup(
        name="WebDeck" if sys.platform == "win32" else "webdeck",
        description="WebDeck" if sys.platform == "win32" else app_description_short,
        long_description=app_description_long,
        author="webdeck.app",
        author_email="contact.lenoch@gmail.com",
        url="https://webdeck.app/",
        license="GPLv3",
        version=version,
        options={
            "build_exe": build_options,
            "bdist_msi": bdist_msi_options if sys.platform == "win32" else {},
            "bdist_rpm": bdist_rpm_options if sys.platform != "win32" else {},
        },
        executables=executables,
    )

    arch = ''
    if sys.platform != "win32":
        arch = '-' + subprocess.check_output(["uname", "-m"]).decode().strip()
    build_dir = f"build/exe.{sys.platform}{arch}-{sys.version_info.major}.{sys.version_info.minor}"

    try:
        # Sign the main executable
        sign_executable(os.path.join(build_dir, "WebDeck.exe" if sys.platform == "win32" else "webdeck"))

        # Sign the updater executable
        sign_executable(os.path.join(build_dir, "update.exe" if sys.platform == "win32" else "webdeck-update"))
    except Exception as e:
        print(f"Failed to sign executables: {e}")

    # Zip the build directory
    zip_build(build_dir)
    
    # Rename the RPM file to match the application name
    if sys.platform != "win32":
        print("Renaming RPM file...")
        rpm_file = next((f for f in os.listdir("dist") if f.endswith(".rpm")), None)
        if rpm_file:
            rpm_file_path = os.path.join("dist", rpm_file)
            os.rename(rpm_file_path, rpm_file_path.replace("webdeck", "WebDeck-linux"))

    # Print missing dependencies
    if missing_dependencies:
        # Don't show libnotify and libnotify-bin as separate dependencies
        if "libnotify" in missing_dependencies and "libnotify-bin" not in missing_dependencies:
            missing_dependencies.remove("libnotify")
        elif "libnotify-bin" in missing_dependencies and "libnotify" not in missing_dependencies:
            missing_dependencies.remove("libnotify-bin")
        
        if "libnotify" in missing_dependencies and "libnotify-bin" in missing_dependencies:
            missing_dependencies.remove("libnotify")
            missing_dependencies.remove("libnotify-bin")
            missing_dependencies.append("libnotify/libnotify-bin")
            
        
        print(f"WARNING: Missing dependencies: {', '.join(missing_dependencies)}")
        print("          Please install the missing dependencies before running the build script again.")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    print(f"Build done! {minutes}m {seconds}s")
