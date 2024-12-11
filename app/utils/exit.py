import sys
import os
import subprocess
import signal
if sys.platform == "win32": import win32com.client
from .logger import log
from .platform import is_windows, is_linux


def exit_program(force=True, from_timeout=False):
    if from_timeout:
        log.info("Timeout reached. Exiting WebDeck...")
    else:
        log.info("Exiting WebDeck...")
    
    if is_windows:
        wmi = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
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
                    log.exception(e, f"Failed to terminate process '{process_name}'", print_log=False)

    if not force:
        log.debug("Force exit not enabled. Sending SIGINT to current process.")
        os.kill(os.getpid(), signal.SIGINT)