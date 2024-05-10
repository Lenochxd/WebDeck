import subprocess


def set_microphone_by_name(name):
    # TODO: (not working rn)
    # Find the recording device with the specified name
    command = f"PowerShell -Command \"Get-WmiObject Win32_SoundDevice | Where-Object {{ $_.Name -like '*{name}*' -and $_.ConfigManagerErrorCode -eq 0 }} | Select-Object -First 1 | Invoke-CimMethod -MethodName SetDefault\""
    subprocess.run(command, shell=True)