#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Implements UI 
"""

import sys
import logging
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow
from ui.gui import Ui_gui
from SensorsThread import SensorsThread
import Settings as stt

class FanComponents(object):
        def __init__(self, fan_id, cb_fan_profile, sld_fan_speed, lbl_fan_speed,
                     lbl_fan_led, lbl_fan_rpm, lbl_fan_watt):
            self.fan_id = fan_id
            self.cb_fan_profile = cb_fan_profile
            self.sld_fan_speed = sld_fan_speed
            self.lbl_fan_speed = lbl_fan_speed
            self.lbl_fan_led = lbl_fan_led
            self.lbl_fan_rpm = lbl_fan_rpm
            self.lbl_fan_watt = lbl_fan_watt
            self.pins = 0
            
        def change_lbl_led(self, pins):
            #4 PINS FAN
            if int(pins) == 4:
                if self.pins != 4:
                    self.lbl_fan_led.setPixmap(QtGui.QPixmap(stt.GREEN_LED))
                    self.lbl_fan_led.setToolTip("4-Pin Fan Connected")
                    if self.sld_fan_speed.isEnabled()==False:
                        self.sld_fan_speed.setEnabled(True)
                        self.sld_fan_speed.setValue(50)
            elif pins == 3:
                if self.pins != 3:
                    self.lbl_fan_led.setPixmap(QtGui.QPixmap(stt.BLUE_LED))
                    self.lbl_fan_led.setToolTip("3-Pin Fan Connected")
                    if self.sld_fan_speed.isEnabled()==False:
                        self.sld_fan_speed.setEnabled(True)
                        self.sld_fan_speed.setValue(50)
            else:
                if self.pins > 0:
                    self.lbl_fan_led.setPixmap(QtGui.QPixmap(stt.RED_LED))
                    self.lbl_fan_led.setToolTip("Fan Disconnected")
                    if self.sld_fan_speed.isEnabled()==False:
                        self.sld_fan_speed.setEnabled(False)
                        self.sld_fan_speed.setValue(0)
                    
        def change_sld_speed(self, speed, thread):
            if self.sld_fan_speed.isEnabled():
                thread.set_fan_speed(self.fan_id,speed)

class pygridv3(QMainWindow):
    """Implemets the Fan components logic"""
    
    def __init__(self, parent=None):
        logging.basicConfig(filename=stt.LOG_FILENAME, level=stt.LOG_LEVEL)
        self.__logger = logging.getLogger(__name__)
        
        
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Ui_gui()
        self.ui.setupUi(self)
        
        self.thread = SensorsThread()
        
        #Initialize states
        self.ui.sld_fan_speed_0.setEnabled(False)
        
        self.ui.sld_fan_speed_1.setEnabled(False)
        self.ui.sld_fan_speed_2.setEnabled(False)
        self.ui.sld_fan_speed_3.setEnabled(False)
        self.ui.sld_fan_speed_4.setEnabled(False)
        self.ui.sld_fan_speed_5.setEnabled(False)
        
        #Create Fan components objects
        self.fan_components = []
        self.fan_components.append(FanComponents(0, self.ui.cb_fan_profile_0, self.ui.sld_fan_speed_0, self.ui.lbl_fan_speed_0,
                     self.ui.lbl_fan_led_0, self.ui.lbl_fan_rpm_0, self.ui.lbl_fan_watt_0))
        self.fan_components.append(FanComponents(1, self.ui.cb_fan_profile_1, self.ui.sld_fan_speed_1, self.ui.lbl_fan_speed_1,
                     self.ui.lbl_fan_led_1, self.ui.lbl_fan_rpm_1, self.ui.lbl_fan_watt_1))
        self.fan_components.append(FanComponents(2, self.ui.cb_fan_profile_2, self.ui.sld_fan_speed_2, self.ui.lbl_fan_speed_2,
                     self.ui.lbl_fan_led_2, self.ui.lbl_fan_rpm_2, self.ui.lbl_fan_watt_2))
        self.fan_components.append(FanComponents(3, self.ui.cb_fan_profile_3, self.ui.sld_fan_speed_3, self.ui.lbl_fan_speed_3,
                     self.ui.lbl_fan_led_3, self.ui.lbl_fan_rpm_3, self.ui.lbl_fan_watt_3))
        self.fan_components.append(FanComponents(4, self.ui.cb_fan_profile_4, self.ui.sld_fan_speed_4, self.ui.lbl_fan_speed_4,
                     self.ui.lbl_fan_led_4, self.ui.lbl_fan_rpm_4, self.ui.lbl_fan_watt_4))
        self.fan_components.append(FanComponents(5, self.ui.cb_fan_profile_5, self.ui.sld_fan_speed_5, self.ui.lbl_fan_speed_5,
                     self.ui.lbl_fan_led_5, self.ui.lbl_fan_rpm_5, self.ui.lbl_fan_watt_5))
        
        #Connect fan slides to speed labels
        self.ui.sld_fan_speed_0.valueChanged.connect(lambda x: self.ui.lbl_fan_speed_0.setText(str(x)+ "%"))
        self.ui.sld_fan_speed_1.valueChanged.connect(lambda x: self.ui.lbl_fan_speed_1.setText(str(x)+ "%"))
        self.ui.sld_fan_speed_2.valueChanged.connect(lambda x: self.ui.lbl_fan_speed_2.setText(str(x)+ "%"))
        self.ui.sld_fan_speed_3.valueChanged.connect(lambda x: self.ui.lbl_fan_speed_3.setText(str(x)+ "%"))
        self.ui.sld_fan_speed_4.valueChanged.connect(lambda x: self.ui.lbl_fan_speed_4.setText(str(x)+ "%"))
        self.ui.sld_fan_speed_5.valueChanged.connect(lambda x: self.ui.lbl_fan_speed_5.setText(str(x)+ "%"))
        
        #Connect fan slides to speed control
        self.ui.sld_fan_speed_0.valueChanged.connect(lambda x : self.fan_components[0].change_sld_speed(x,self.thread))
        self.ui.sld_fan_speed_1.valueChanged.connect(lambda x : self.fan_components[1].change_sld_speed(x,self.thread))
        self.ui.sld_fan_speed_2.valueChanged.connect(lambda x : self.fan_components[2].change_sld_speed(x,self.thread))
        self.ui.sld_fan_speed_3.valueChanged.connect(lambda x : self.fan_components[3].change_sld_speed(x,self.thread))
        self.ui.sld_fan_speed_4.valueChanged.connect(lambda x : self.fan_components[4].change_sld_speed(x,self.thread))
        self.ui.sld_fan_speed_5.valueChanged.connect(lambda x : self.fan_components[5].change_sld_speed(x,self.thread))
    
        #Connect the SensorsThread to gui components
        self.thread.signal_rpm_fan_0.connect(lambda x: self.ui.lbl_fan_rpm_0.setText(str(x)))
        self.thread.signal_rpm_fan_1.connect(lambda x: self.ui.lbl_fan_rpm_1.setText(str(x)))
        self.thread.signal_rpm_fan_2.connect(lambda x: self.ui.lbl_fan_rpm_2.setText(str(x)))
        self.thread.signal_rpm_fan_3.connect(lambda x: self.ui.lbl_fan_rpm_3.setText(str(x)))
        self.thread.signal_rpm_fan_4.connect(lambda x: self.ui.lbl_fan_rpm_4.setText(str(x)))
        self.thread.signal_rpm_fan_5.connect(lambda x: self.ui.lbl_fan_rpm_5.setText(str(x)))
        
        self.thread.signal_watt_fan_0.connect(lambda x: self.ui.lbl_fan_watt_0.setText("{:.1f}".format(x)))
        self.thread.signal_watt_fan_1.connect(lambda x: self.ui.lbl_fan_watt_1.setText("{:.1f}".format(x)))
        self.thread.signal_watt_fan_2.connect(lambda x: self.ui.lbl_fan_watt_2.setText("{:.1f}".format(x)))
        self.thread.signal_watt_fan_3.connect(lambda x: self.ui.lbl_fan_watt_3.setText("{:.1f}".format(x)))
        self.thread.signal_watt_fan_4.connect(lambda x: self.ui.lbl_fan_watt_4.setText("{:.1f}".format(x)))
        self.thread.signal_watt_fan_5.connect(lambda x: self.ui.lbl_fan_watt_5.setText("{:.1f}".format(x)))
        
        self.thread.signal_pins_fan_0.connect(self.fan_components[0].change_lbl_led)
        self.thread.signal_pins_fan_1.connect(self.fan_components[1].change_lbl_led)
        self.thread.signal_pins_fan_2.connect(self.fan_components[2].change_lbl_led)
        self.thread.signal_pins_fan_3.connect(self.fan_components[3].change_lbl_led)
        self.thread.signal_pins_fan_4.connect(self.fan_components[4].change_lbl_led)
        self.thread.signal_pins_fan_5.connect(self.fan_components[5].change_lbl_led)
        
        self.thread.signal_temp_cpu.connect(self.ui.lcd_cpu_temp.display)
        self.thread.signal_temp_cpu.connect(self.ui.pb_cpu_temp.setValue)
        self.thread.signal_temp_gpu.connect(self.ui.lcd_gpu_temp.display)
        self.thread.signal_temp_gpu.connect(self.ui.pb_gpu_temp.setValue)
        
    
        self.thread.start()
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    pygridv3_app = pygridv3()
    pygridv3_app.show()
    sys.exit(app.exec_())
    

