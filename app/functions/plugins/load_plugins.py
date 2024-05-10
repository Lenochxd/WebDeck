import os
import importlib


modules = {}
def load_plugins(commands):
    global all_func
    dict_func = {}
    all_func = {}
    folder_path = "./plugins"

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, folder_path).replace(os.sep, "."))[0]
                
                try:
                    if module_name in modules.keys():
                        modules[module_name] = importlib.reload(modules[module_name])
                    else:
                        modules[module_name] = __import__(f"plugins.{module_name}", fromlist=[""])
                    

                    dict_doc, dict_func, addon_name = (
                        modules[module_name].WebDeckAddon.instance._dict_doc,
                        modules[module_name].WebDeckAddon.instance._dict_func,
                        modules[module_name].WebDeckAddon.instance._addon_name
                    )
                    print('addon name: ', addon_name)

                    all_func[addon_name] = dict_func
                    dict_doc = {x: y._to_dict() for x, y in dict_doc.items()}

                    commands[addon_name] = dict_doc
                    
                except Exception as e:
                    print(f"Error importing module {module_name}: {e}")
                    continue
                
    return commands, all_func