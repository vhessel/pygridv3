#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Pooling thread for Grid+ and sensors data
"""

import psutil
import time
import logging
from PyQt5.QtCore import QThread, pyqtSignal

from SingletonDecorator import Singleton
from GridV3 import GridV3
import Settings as stt
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetTemperature

@Singleton
class SensorsThread(QThread):
    #QT Signal for fan rpm
    signal_rpm_fan_0 = pyqtSignal(int)
    signal_rpm_fan_1 = pyqtSignal(int)
    signal_rpm_fan_2 = pyqtSignal(int)
    signal_rpm_fan_3 = pyqtSignal(int)
    signal_rpm_fan_4 = pyqtSignal(int)
    signal_rpm_fan_5 = pyqtSignal(int)
    
    #QT Signal for fan wattage
    signal_watt_fan_0 = pyqtSignal(float)
    signal_watt_fan_1 = pyqtSignal(float)
    signal_watt_fan_2 = pyqtSignal(float)
    signal_watt_fan_3 = pyqtSignal(float)
    signal_watt_fan_4 = pyqtSignal(float)
    signal_watt_fan_5 = pyqtSignal(float)
    
    #QT Signal for fan pins
    signal_pins_fan_0 = pyqtSignal(int)
    signal_pins_fan_1 = pyqtSignal(int)
    signal_pins_fan_2 = pyqtSignal(int)
    signal_pins_fan_3 = pyqtSignal(int)
    signal_pins_fan_4 = pyqtSignal(int)
    signal_pins_fan_5 = pyqtSignal(int)
    
    #QT Signal for CPU/GPU temperatures
    signal_temp_cpu = pyqtSignal(float)
    signal_temp_gpu = pyqtSignal(float)
    
    def __init__(self, pooling_interval=250):
        super().__init__()
        
        logging.basicConfig(filename=stt.LOG_FILENAME, level=stt.LOG_LEVEL)
        self.__logger = logging.getLogger(__name__)
        
        #QT Signal for fan pins
        #self.signal_pins_fan = [pyqtSignal(int) for _ in range(6)]
        nvmlInit()
        
        self.pooling_interval = pooling_interval        
        
        self.__logger.debug("Sensors Thread Created")
    

    def stop(self):
        self.__logger.debug("Stopping SensorsThread")
        self.is_running = False
        self.wait()
        self.__logger.debug("SensorsThread Stopped")
    
    def set_fan_speed(self, fan_id, speed):
        if self.is_running:
            speed = max(0,min(speed,100))
            self.grid.set_fan_speed(fan_id,speed)
    
    def run(self):
        try:
            self.__logger.debug("Starting SensorsThread")
            
            self.grid = GridV3(grid_id_vendor = stt.GRIDV3_ID_VENDOR, grid_id_product = stt.GRIDV3_ID_PRODUCT)
            
            self.is_running = True
            
            while self.is_running:
            
                self.grid.update_fan_data()
                
                fan_state = self.grid.get_fan_state(0)
                self.signal_rpm_fan_0.emit(fan_state.rpm)
                self.signal_watt_fan_0.emit(fan_state.wattage)
                self.signal_pins_fan_0.emit(fan_state.pins)
                fan_state = self.grid.get_fan_state(1)
                self.signal_rpm_fan_1.emit(fan_state.rpm)
                self.signal_watt_fan_1.emit(fan_state.wattage)
                self.signal_pins_fan_1.emit(fan_state.pins)
                fan_state = self.grid.get_fan_state(2)
                self.signal_rpm_fan_2.emit(fan_state.rpm)
                self.signal_watt_fan_2.emit(fan_state.wattage)
                self.signal_pins_fan_2.emit(fan_state.pins)
                fan_state = self.grid.get_fan_state(3)
                self.signal_rpm_fan_3.emit(fan_state.rpm)
                self.signal_watt_fan_3.emit(fan_state.wattage)
                self.signal_pins_fan_3.emit(fan_state.pins)
                fan_state = self.grid.get_fan_state(4)
                self.signal_rpm_fan_4.emit(fan_state.rpm)
                self.signal_watt_fan_4.emit(fan_state.wattage)
                self.signal_pins_fan_4.emit(fan_state.pins)
                fan_state = self.grid.get_fan_state(5)
                self.signal_rpm_fan_5.emit(fan_state.rpm)
                self.signal_watt_fan_5.emit(fan_state.wattage)
                self.signal_pins_fan_5.emit(fan_state.pins)
                
                cpu_temp = self.get_cpu_temp()
                if cpu_temp:
                    self.signal_temp_cpu.emit(cpu_temp)
                    
                gpu_temp = self.get_gpu_temp()
                if gpu_temp:
                    self.signal_temp_gpu.emit(gpu_temp)
                
                self.__logger.debug("Waiting timer")
                time.sleep(self.pooling_interval/1000)
        except Exception:
            self.__logger.error("SensorsThread Exception",exc_info=True)
        self.__logger.debug("Thread Finished")
            
    #Implementing temperature monitoring right here (Should I write a separate class?)
    def get_cpu_temp(self):
        try:
            temp_data = psutil.sensors_temperatures().get(stt.CPU_TEMP_SENSOR,None)
            if temp_data:
                return temp_data[0].current
        except Exception:
            self.__logger.error("SensorsThread.get_cpu_temp Exception", exc_info=True)
        return None
    
    def get_gpu_temp(self):
        try:
            gpu_handle = nvmlDeviceGetHandleByIndex(0)
            temp_data = nvmlDeviceGetTemperature(gpu_handle,0)
            if temp_data:
                return temp_data
        except Exception:
            self.__logger.error("SensorsThread.get_cpu_temp Exception", exc_info=True)
        return None
        