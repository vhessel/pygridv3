"""
    Grid+ V3 Communication Module
"""

import sys
import usb.core
import logging
from SingletonDecorator import Singleton
import Settings as stt

""" FAN Class - Keep Fan propeties """
class FanState(object):
    def __init__(self, fan_id):
        self.fan_id = fan_id
        self.rpm = 0
        self.voltage = 0
        self.current = 0
        self.__pins = 0
    
    @property
    def pins(self):
        return self.__pins
    @pins.setter
    def pins(self,p):
        if p==1:
            self.__pins = 3
        elif p==2:
            self.__pins = 4
        else:
            self.__pins = 0
    
    @property
    def wattage(self):
        return self.voltage*self.current
    
    def __str__(self):
        return "Fan #{}: ({} RPM, {:.2f} V, {:.2f} a, {:.2f} W, {} Pins Connected)".format(self.fan_id,self.rpm,self.voltage,self.current,self.wattage,self.pins)
    
@Singleton
class GridV3(object):
    def __init__(self, grid_id_vendor=0x1e71, grid_id_product=0x1711):
        logging.basicConfig(filename=stt.LOG_FILENAME, level=stt.LOG_LEVEL)
        self.__logger = logging.getLogger(__name__)
        
        self.__dict_fan = {k:FanState(k) for k in range(6)}
        
        self.dev = usb.core.find(idVendor=grid_id_vendor, idProduct=grid_id_product)
        
        #RELEASE DEVICE
        try:
            if self.dev.is_kernel_driver_active(0) is True:
                self.dev.detach_kernel_driver(0)
        except usb.core.USBError as e:
            self.__logger.error("Kernel driver won't give up control over device: %s" % str(e), exc_info=True)
            sys.exit("Kernel driver won't give up control over device: %s" % str(e))
        
        #CONFIG DEVICE
        try:
            self.dev.set_configuration()
        except usb.core.USBError as e:
            self.__logger.error("Cannot set configuration the device: %s" % str(e), exc_info=True)
            sys.exit("Cannot set configuration the device: %s" % str(e))   
            
        #Get an endpoint instance
        cfg = self.dev.get_active_configuration()
        intf = cfg[(0,0)]

        #Get a writable endpoint 
        self.ep_out = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_OUT)

        #Get a readable endpoint 
        self.ep_in = usb.util.find_descriptor(
            intf,
            # match the first IN endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)
    def reset(self):
        self.dev.reset()

    def set_fan_speed(self, fan_id, fan_speed):
        command = bytes([0x02,0x4d,fan_id,0x00,fan_speed]+[0]*60)
        self.ep_out.write(command)

    def update_fan_data(self):
        data = self.ep_in.read(self.ep_in.wMaxPacketSize)
        
        #Read readme_grid.txt for more details        
        fan_id = data[15]//16
        pins = data[15]%16
        voltage = data[7]+data[8]/100
        current = data[10]/100
        rpm = data[3]*16**2+data[4]
        
        fan_state = self.__dict_fan.get(fan_id,None)
        if fan_state:
            fan_state.rpm = rpm
            fan_state.pins = pins
            fan_state.voltage = voltage
            fan_state.current = current
        
            self.__logger.debug('%s'%(fan_state))
            
    def get_fan_state(self, fan_id):
        return self.__dict_fan.get(fan_id,None)
