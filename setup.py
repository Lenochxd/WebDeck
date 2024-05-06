from cx_Freeze import setup, Executable
build_options = {
                    'packages': [],
                    'excludes': ["cx_Freeze"],
                    "zip_include_packages": "*",
                    "zip_exclude_packages": [
                        "_sounddevice_data",
                        "pygame",
                        "soundfile", "_soundfile", "_soundfile_data",
                        "vlc", "python-vlc",
                        "jaraco"
                    ]
                }

import sys, os, json, shutil
import fnmatch
import time
start_time = time.time()
sys.setrecursionlimit(10000)
base = 'Win32GUI' if sys.platform=='win32' else None
# base = 'console' if sys.platform=='win32' else None

executables = [
    # tray icon
    Executable('main.py', base=base, target_name='WebDeck', icon='static/files/icon.ico'),
    # bishokus.fr/webdeck/start
    #Executable('start_server.py', base=base, target_name='WD_start'),
    # actual code
    Executable('main_server.py', base=base, target_name='WD_main'),
    Executable('updater.py', base=base, target_name='WD_updater')
]

with open('static/files/version.json', encoding="utf-8") as f:
    version = json.load(f)['versions'][0]['version']

setup(name='WebDeck',
    description='WebDeck',
    author='bishokus.fr',
    version = version,
    options = {'build_exe': build_options},
    executables = executables)


def is_excluded(file_path, exclude_list):
    rel_path = os.path.relpath(file_path)
    
    for exclude_pattern in exclude_list:
        if fnmatch.fnmatch(rel_path, exclude_pattern):
            return True
        
    return False

ignored_files = [
    '!buttons', 'addons', 'plugins', '.git', '.github', '.vscode', '__pycache__', 'build', 'requirements.txt',
    'webdeck', '%.html%WebDeck', 'testmic', 'build.bat',
    'WD_main.exe', 'WebDeck.exe', 'WD_updater.exe'
]

if os.path.isfile('.gitignore'):
    with open('.gitignore', 'r') as gitignore_file:
        for line in gitignore_file:
            if line.strip() != '' and not line.strip().startswith('#'):
                if line.startswith("\\"):
                    line = line.replace('\\', '', 1)
                ignored_files.append(line.strip())


script_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(script_dir, 'build')

if os.path.exists(build_dir):
    first_folder = next(entry for entry in os.listdir(build_dir) if os.path.isdir(os.path.join(build_dir, entry)))
    target_dir = os.path.join(build_dir, first_folder)
    
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        if item != target_dir and not is_excluded(item, ignored_files) and item.endswith('.py') == False and item.endswith('.md') == False:
            if os.path.isdir(item_path):
                shutil.copytree(item_path, os.path.join(target_dir, item))
            else:
                shutil.copy2(item_path, target_dir)
            print(f'copying {item_path} -> {target_dir}')


end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f'build done! {minutes}m{seconds}s')