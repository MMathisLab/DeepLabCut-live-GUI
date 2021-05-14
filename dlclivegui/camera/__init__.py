"""
DeepLabCut Toolbox (deeplabcut.org)
© A. & M. Mathis Labs

Licensed under GNU Lesser General Public License v3.0
"""


import platform
import logging

from dlclivegui.camera.camera import Camera, CameraError
from dlclivegui.camera.opencv import OpenCVCam

if platform.system() == "Windows":
    try:
        from dlclivegui.camera.tiscamera_windows import TISCam
    except Exception as e:
        pass

if platform.system() == "Linux":
    try:
        from dlclivegui.camera.tiscamera_linux import TISCam
    except Exception as e:
        pass
        # print(f"Error importing TISCam on Linux: {e}")

    try:
        from baslerpi.io.cameras.basler_camera import BaslerCameraDLC
    except Exception as e:
        logging.warning("Could not import Basler camera")

if platform.system() in ["Darwin", "Linux"]:
    try:
        from dlclivegui.camera.aravis import AravisCam
    except Exception as e:
        pass
        # print(f"Error importing AravisCam: f{e}")

if platform.system() == "Darwin":
    try:
        from dlclivegui.camera.pseye import PSEyeCam
    except Exception as e:
        pass
