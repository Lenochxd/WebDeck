from cx_Freeze import setup, Executable
build_options = {
                    'packages': ['webdeck', 'app', 'static', 'templates'],
                    'excludes': ['cx_Freeze', 'pathspec'],
                    "zip_include_packages": "*",
                    "zip_exclude_packages": [
                        "_sounddevice_data",
                        "pygame",
                        "soundfile", "_soundfile", "_soundfile_data",
                        "vlc", "python-vlc",
                        "numpy",
                        "jaraco",
                    ]
                }

import urllib.request
import zipfile
import pathspec
import sys, os, json, shutil
import time
start_time = time.time()
sys.setrecursionlimit(10000)
base = 'Win32GUI' if sys.platform=='win32' else None
# base = 'console' if sys.platform=='win32' else None

executables = [
    Executable('run.py', base=base, target_name='WebDeck', icon='static/icons/icon.ico'),
    Executable('app/updater/updater.py', base='console', target_name='update')
]

with open('webdeck/version.json', encoding="utf-8") as f:
    version = json.load(f)['versions'][0]['version']

setup(name='WebDeck',
    description='WebDeck',
    author='bishokus.fr',
    version = version,
    options = {'build_exe': build_options},
    executables = executables)

def download_nircmd():
    zippath = "temp/nircmd.zip"
    
    url = "https://www.nirsoft.net/utils/nircmd.zip"
    urllib.request.urlretrieve(url, zippath)

    with zipfile.ZipFile(zippath, "r") as zip_ref:
        zip_ref.extractall("temp")

    os.remove(zippath)

def is_excluded(file_path, exclude_list):
    rel_path = os.path.relpath(file_path)
    spec = pathspec.PathSpec.from_lines("gitwildmatch", exclude_list)

    if spec.match_file(rel_path):
        print(f"EXCLUDED: {file_path}")
        return True

    print(f"NOT EXCLUDED: {file_path}")
    return False


ignored_files = [
    '.git', '.github', '.vscode', '__pycache__', '%.html%WebDeck',
    'WebDeck.exe', 'update.exe', 'build', 'build.bat',
    'requirements.txt', 'temp', 'tests/*', 'README*', '*.py'
]

if os.path.isfile('.gitignore'):
    with open('.gitignore', 'r') as gitignore_file:
        for line in gitignore_file:
            if line.strip() != '' and not line.strip().startswith('#'):
                if line.startswith("\\"):
                    line = line.replace('\\', '', 1)
                if not line == '*copy.*':
                    ignored_files.append(line.strip())

print('IGNORED:', ignored_files)

script_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(script_dir, 'build')

if os.path.exists(build_dir):
    first_folder = next(entry for entry in os.listdir(build_dir) if os.path.isdir(os.path.join(build_dir, entry)))
    target_dir = os.path.join(build_dir, first_folder)
    
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        if os.path.isdir(item_path):
            if not is_excluded(item_path, ignored_files):
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if not is_excluded(file_path.replace(f'{script_dir}\\', ''), ignored_files):
                            target_file_path = os.path.join(target_dir, os.path.relpath(file_path, script_dir))
                            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                            shutil.copy(file_path, target_file_path)
                            print(f'copying {file_path} -> {target_file_path}')
        else:
            if not is_excluded(item_path, ignored_files):
                shutil.copy(item_path, target_dir)
                print(f'copying {item_path} -> {target_dir}')


    # NIRCMD
    if not os.path.isfile("temp/nircmd.exe"):
        download_nircmd()
    
    lib_dir = os.path.join(target_dir, "lib")
    os.makedirs(lib_dir, exist_ok=True)
    for file in ['nircmd.exe', 'nircmdc.exe', 'NirCmd.chm']:
        file_path = os.path.join(script_dir, f'temp/{file}')
        target_file_path = os.path.join(lib_dir, file)
        shutil.copy(file_path, target_file_path)
        print(f'copying {file_path} -> {target_file_path}')
    
    
    # READMEs
    docs_dir = os.path.join(target_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        if os.path.isfile(item_path) and item.startswith("README"):
            target_file_path = os.path.join(docs_dir, item)
            shutil.copy(item_path, target_file_path)
            print(f'copying {item_path} -> {target_file_path}')
        
    

end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

print(f'build done! {minutes}m{seconds}s')