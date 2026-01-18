import comtypes
from pycaw.pycaw import AudioUtilities
from pycaw.constants import EDataFlow

def set_speakers_by_name(speakers_name):
    comtypes.CoInitialize()
    devices = AudioUtilities.GetAllDevices(data_flow=EDataFlow.eRender.value)
    for device in devices:
        if device.FriendlyName == speakers_name:
            AudioUtilities.SetDefaultDevice(device.id)