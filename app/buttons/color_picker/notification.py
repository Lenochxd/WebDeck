from app.utils.platform import is_windows, is_linux
from app.utils.working_dir import get_base_dir
from app.utils.logger import log

from app.utils.get_process_path import get_process_path
import subprocess
import os
if is_windows:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()


def toast(display_type, typestocopy, color_names_final):
    
    icon = "static\\icons\\icon.ico"
    duration = 5
    message = ""
    if display_type and display_type.lower() != "list":
        message = (
            list(color_names_final.values())[0]
            if typestocopy and len(typestocopy.split(";")) == 1
            else ", ".join(color_names_final.values())
        )
    elif typestocopy and len(typestocopy.split(";")) == 1:
        message = str(color_names_final)[:-2][2:].replace("'", "")
    else:
        message = (
            str(color_names_final)
            .replace("', ", ",\n")[:-2][2:]
            .replace("'", "")
        )

    title = "WebDeck Color Picker"
    
    if is_windows:
        toaster.show_toast(
            title, message, icon_path=icon, duration=duration, threaded=True
        )
        return
        
    elif is_linux:
        icon_path = os.path.join(get_base_dir(), icon.replace('.ico', '.png'))
        log.debug(f"Icon path: {icon_path}")
        subprocess.Popen([
            get_process_path('notify-send'), 
            title, 
            message, 
            '-a', title,
            '-i', icon_path, 
            '-u', 'normal', 
            # '-t', str(duration * 1000), 
        ])
        return
