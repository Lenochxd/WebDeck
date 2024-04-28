import sys
import subprocess

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