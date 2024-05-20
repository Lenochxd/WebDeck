import win32com
import time
import sys


def is_opened():
    if not getattr(sys, 'frozen', False):
        return False
    else:
        wmi = win32com.client.GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")
        
        wd_count = sum(1 for process in processes if 'webdeck' in process.Properties_('Name').Value.lower().strip() or 'wd_' in process.Properties_('Name').Value.lower().strip())
        if wd_count > 1:
            time.sleep(1)
            processes = wmi.InstancesOf("Win32_Process")
            
            wd_count = sum(1 for process in processes if 'webdeck' in process.Properties_('Name').Value.lower().strip())
            if wd_count > 1:
                wd_count = sum(1 for process in processes if 'wd_' in process.Properties_('Name').Value.lower().strip())
                return wd_count == 0
    
    return True