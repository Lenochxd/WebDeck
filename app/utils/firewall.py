import sys
import subprocess
from win32com.client import Dispatch

def fix_firewall_permission():
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
    
def check_firewall_permission():
    try:
        firewall_manager = Dispatch("HNetCfg.FwMgr")
        policy = firewall_manager.LocalPolicy.CurrentProfile
        authorized_applications = policy.AuthorizedApplications

        for app in authorized_applications:
            if app.ProcessImageFileName.lower() == sys.executable.lower():
                print(f"The application ({sys.executable}) has permission to pass through the firewall.")
                return True

        print(f"The application ({sys.executable}) does not have permission to pass through the firewall.")
        return False
    except Exception as e:
        print(f"Error checking firewall : {e}")
        return True