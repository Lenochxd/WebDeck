import sys
import os
import win32com.client
import subprocess
import signal


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
                print(f"Stopping process: {process.Properties_('Name').Value}")
                try:
                    result = process.Terminate()
                    if result == 0:
                        print("Process terminated successfully.")
                    else:
                        subprocess.Popen(f"taskkill /f /IM {process_name}", shell=True)
                except Exception as e:
                    print(f"Failed to terminate process {process_name}: {e}")

    os.kill(os.getpid(), signal.SIGINT)