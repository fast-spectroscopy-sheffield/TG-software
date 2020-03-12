#import os
#import ctypes as ct
import time
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Acquisition(QObject):
    
    def __init__(self, camera):
        super(QObject, self).__init__()
        self.camera = camera
        
    start_acquire = pyqtSignal()
    data_ready = pyqtSignal(np.ndarray)
    @pyqtSlot()
    def acquire(self):
        self.camera.single_acquisition()
        self.data_ready.emit(self.camera.data)
        return
        

class Camera(QObject):
    
    def __init__(self):
        super(QObject, self).__init__()
        self.ready = False
        self.dll = None  # ct.WinDLL(os.path.join())
        self.temperature_setpoint = -30.0
        self.num_pixels = 1024
        self.data = np.zeros(self.num_pixels)
        self.exposure_time = 0.05
        self.gain = 0
        self.num_accumulations = 1
        self.gate_delay = 2840
        self.gate_width = 2
    
    def initialise(self):
        self.start_cooldown()
        # set up the camera with the correct settings for TG acquisition
        self.ready = True
        return
    
    def start_cooldown(self):
        self.set_temperature(self.temperature_setpoint)
        self.peltier_on()
        return
    
    def start_warmup(self):
        self.peltier_off()
        return
    
    def apply_acquisition_settings(self):
        self.set_exposure_time()
        self.set_gain()
        self.set_num_accumulations()
        self.set_gate_delay()
        self.set_gate_width()
        return
    
    _exit = pyqtSignal()
    @pyqtSlot()
    def shutdown(self):
        self.ccdexit()
        return
        
    ###########################################################################
    ###########################################################################
    ###########################################################################
        
    # library methods from DLL will go here (pyAndor?)
    
    def set_temperature(self, temperature_setpoint):
        return
        
    def get_temperature(self):
        return -30.0
    
    def peltier_on(self):
        return
    
    def peltier_off(self):
        return
    
    def set_exposure_time(self):
        return
    
    def set_gain(self):
        return
    
    def set_num_accumulations(self):
        return
    
    def set_gate_delay(self):
        return
    
    def set_gate_width(self):
        return
    
    def single_acquisition(self):
        time.sleep(self.exposure_time)
        x = np.linspace(0, self.num_pixels, self.num_pixels, endpoint=False)
        y = 1e4*(np.exp(-((x-600)**2)/(2*40**2)) + 0.3*(np.random.rand(self.num_pixels)-0.5))
        self.data[:] = y
        return
    
    def ccdexit(self):
        return
        
          