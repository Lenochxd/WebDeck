from .platform import is_win

import sys
import subprocess
if is_win: from win32com.client import Dispatch
from .logger import log

def fix_firewall_permission():
    if not is_win:
        log.info("Skipping firewall permission fix on non-Windows system.")
        return
    
    command = [
        "powershell",
        "-NoProfile",
        "New-NetFirewallRule",
        "-DisplayName",
        '"WebDeck"',
        "-Direction",
        "Inbound",
        "-Program",
        f'"{sys.executable}"',
        "-Action",
        "Allow",
    ]
    subprocess.run(command)
    log.info("Firewall permission should be fixed.")
    
def check_firewall_permission():
    if not is_win:
        log.info("Skipping firewall permission check on non-Windows system.")
        return True
    
    try:
        firewall_manager = Dispatch("HNetCfg.FwMgr")
        policy = firewall_manager.LocalPolicy.CurrentProfile
        authorized_applications = policy.AuthorizedApplications

        for app in authorized_applications:
            if app.ProcessImageFileName.lower() == sys.executable.lower():
                log.debug(f"The application ({sys.executable}) has permission to pass through the firewall.")
                return True

        log.debug(f"The application ({sys.executable}) does not have permission to pass through the firewall.")
        return False
    except Exception as e:
        log.exception(e, "Error checking firewall permissions.")
        return True