import sys
import os
import win32com.client
import subprocess
import signal
from .logger import log


def exit_program(force=True):
    log.info("Exiting WebDeck...")
    if sys.platform == "win32":
        wmi = win32com.client.GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")

        process_names_to_terminate = ["nircmd.exe"]
        if force:
            process_names_to_terminate.append("webdeck.exe")
            if not getattr(sys, 'frozen', False):
                log.debug("Curently not running in a frozen state (not compiled). Adding python executables to termination list.")
                os.kill(os.getpid(), signal.SIGINT)
                process_names_to_terminate.append("python.exe")
                process_names_to_terminate.append("py.exe")

        for process in processes:
            process_name = process.Properties_('Name').Value.lower().strip()
            if process_name in process_names_to_terminate:
                log.debug(f"Stopping process: {process.Properties_('Name').Value}")
                try:
                    result = process.Terminate()
                    if result == 0:
                        log.success(f"Process terminated successfully: {process.Properties_('Name').Value}")
                    else:
                        log.debug(f"Failed to terminate process {process_name} using WMI. Attempting taskkill.")
                        subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
                except Exception as e:
                    log.exception(e, f"Failed to terminate process '{process_name}'")

    if not force:
        log.debug("Force exit not enabled. Sending SIGINT to current process.")
        os.kill(os.getpid(), signal.SIGINT)