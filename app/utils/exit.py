import sys
import os
import win32com.client
import subprocess
import signal
from .logger import log


def exit_program(force=False):
    if sys.platform == "win32":
        wmi = win32com.client.GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")

        process_names_to_terminate = ["nircmd.exe"]
        if force:
            process_names_to_terminate.append("webdeck.exe")

        for process in processes:
            process_name = process.Properties_('Name').Value.lower().strip()
            if process_name in process_names_to_terminate:
                log.debug(f"Stopping process: {process.Properties_('Name').Value}")
                try:
                    result = process.Terminate()
                    if result == 0:
                        log.success(f"Process terminated successfully: {process.Properties_('Name').Value}")
                    else:
                        subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
                except Exception as e:
                    log.exception(e, f"Failed to terminate process '{process_name}'")

    log.info("Exiting WebDeck...")
    os.kill(os.getpid(), signal.SIGINT)