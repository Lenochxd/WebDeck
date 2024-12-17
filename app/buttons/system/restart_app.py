from app.utils.platform import is_windows, is_linux
import subprocess
import time
from app.utils.logger import log


def restart_app(message):
    if is_windows:
        app = message.replace("/restart", "")
        if not "." in app:
            app += ".exe"
        subprocess.Popen(f"taskkill /f /im {app}", shell=True)
        if subprocess.Popen(f"start {app}", shell=True).returncode == 0:
            log.success(f"App '{app}' restarted successfully")
        else:
            log.error(f"App '{app}' not found")
            raise RuntimeError(f"App '{app}' not found")
    
    elif is_linux:
        app, restart_command = message.replace("/restart", "").strip().split("---")
        app = app.strip()
        restart_command = restart_command.strip()
        
        # Kill all processes with the app name
        subprocess.Popen(f"pkill -f {app}", shell=True)
        time.sleep(0.5)
        
        # Restart the app
        log.debug(f"Restarting app '{app}' with command '{restart_command}'")
        result = subprocess.Popen(f"nohup {restart_command} > /dev/null 2>&1 &", shell=True, start_new_session=True)
        result.wait()
        log.debug(result)
        if result.returncode == 0:
            log.success(f"App '{app}' restarted successfully")
        else:
            log.error(f"Failed to restart app '{app}'")
            raise RuntimeError(f"Failed to restart app '{app}'")
        
    else:
        raise NotImplementedError("Restart is not implemented for this platform.")