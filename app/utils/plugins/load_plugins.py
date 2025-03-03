import os
import importlib
import shutil
from ..logger import log


modules = {}
def load_plugins(commands):
    global all_func
    dict_func = {}
    all_func = {}
    plugins_path = ".config/plugins"
    
    temp_dir = "temp/plugins"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    try:
        os.makedirs(temp_dir)
    except FileExistsError as e:
        log.exception(e, f"Error creating temp plugins directory '{temp_dir}'", expected=False, print_log=False)

    for root, dirs, files in os.walk(plugins_path):
        for file in files:
            src = os.path.join(root, file)
            dst = os.path.join(temp_dir, file)
            shutil.copy(src, dst)
            
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, temp_dir).replace(os.sep, "."))[0]
                
                try:
                    if module_name in modules.keys():
                        modules[module_name] = importlib.reload(modules[module_name])
                    else:
                        modules[module_name] = __import__(f"temp.plugins.{module_name}", fromlist=[""])
                    

                    dict_doc, dict_func, plugin_name = (
                        modules[module_name].WebDeckAddon.instance._dict_doc,
                        modules[module_name].WebDeckAddon.instance._dict_func,
                        modules[module_name].WebDeckAddon.instance._addon_name
                    )
                    log.info(f"Loaded plugin: {plugin_name}")

                    all_func[plugin_name] = dict_func
                    dict_doc = {x: y._to_dict() for x, y in dict_doc.items()}

                    commands[plugin_name] = dict_doc
                    
                except Exception as e:
                    log.exception(e, f"Error importing module '{module_name}'")
                    continue
                
    return commands, all_func