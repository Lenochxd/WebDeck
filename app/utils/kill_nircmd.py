from subprocess import Popen

def kill_nircmd():
    try:
        Popen("taskkill /f /IM nircmd.exe", shell=True)
    except:
        pass