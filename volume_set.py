from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


def set_audio_volume(length, min_v=-65.25, max_v=.0):
    min_hand_gape, max_hand_gape = 20, 250
    cur_vol = np.interp(length, [min_hand_gape, max_hand_gape], [min_v, max_v])
    volume.SetMasterVolumeLevel(cur_vol, None)


if __name__ == '__main__':
    volume.GetMute()
    volume.GetMasterVolumeLevel()
    print(volume.GetVolumeRange())
