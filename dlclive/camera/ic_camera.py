"""
Camera Control
Copyright M. Mathis Lab
Written by  Gary Kane - https://github.com/gkane26
post-doctoral fellow @ the Adaptive Motor Control Lab
https://github.com/AdaptiveMotorControlLab

camera class for imaging source cameras - helps load correct settings
"""

from . import Camera
from . import tisgrabber as ic
import numpy as np
import os
import json
import cv2
import ctypes as C

# path = os.path.dirname(os.path.realpath(__file__))
# dets_file = os.path.normpath(path + '/camera_details.json')
# cam_details = json.load(open(dets_file, 'r'))

class ICCam(Camera):

    def __init__(self, serial_number, exposure=.005, rotate=0, crop={'top':0,'left':0,'height':540,'width':720}, fps=100):
        '''
        Params
        ------
        serial_number = string; serial number for imaging source camera
        crop = dict; contains ints named top, left, height, width for cropping
            default = None, uses default parameters specific to camera
        '''

        self.cam = ic.TIS_CAM()
        self.serial_number = serial_number
        #self.cam.open(self.serial_number)
        self.im_size = (720, 540)
        self.crop_filter = None
        self.rotation_filter = None
        super().__init__(exposure=exposure, rotate=rotate, crop=crop, fps=fps)

    def set_exposure(self, val):
        val = 1 if val > 1 else val
        val = 0 if val < 0 else val
        self.cam.SetPropertyAbsoluteValue("Exposure", "Value", val)

    def get_exposure(self):
        exposure = [0]
        self.cam.GetPropertyAbsoluteValue("Exposure", "Value", exposure)
        return round(exposure[0], 3)

    def set_crop(self, top, left, height, width):
        if not self.crop_filter:
            self.crop_filter = self.cam.CreateFrameFilter(b'ROI')
            self.cam.AddFrameFilter(self.crop_filter)
        self.cam.FilterSetParameter(self.crop_filter, b'Top', top)
        self.cam.FilterSetParameter(self.crop_filter, b'Left', left)
        self.cam.FilterSetParameter(self.crop_filter, b'Height', height)
        self.cam.FilterSetParameter(self.crop_filter, b'Width', width)
        self.im_size = (width, height)

    def set_rotation(self, rotate):
        if not self.rotation_filter:
            self.rotation_filter = self.cam.CreateFrameFilter(b'Rotate Flip')
            self.cam.AddFrameFilter(self.rotation_filter)
        self.cam.FilterSetParameter(self.rotation_filter, b'Rotation Angle', rotate)

    def set_fps(self, fps):
        super().set_fps(fps)
        self.cam.SetFrameRate(fps)

    def get_image(self):
        self.cam.SnapImage()
        frame = self.cam.GetImageEx()
        frame = cv2.flip(frame, 0)
        return frame

    def open(self, show_display=1):
        self.cam.open(self.serial_number)
        self.cam.SetContinuousMode(0)
        self.cam.StartLive(show_display)

    def close(self):
        super().close()
        self.cam.StopLive()
