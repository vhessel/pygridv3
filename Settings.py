#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Define project settings
"""
import logging

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = "log/log.txt"

RED_LED = ":/resources/red_led.png"
BLUE_LED = ":/resources/blue_led.png"
GREEN_LED = ":/resources/green_led.png"

#NZXT Grid+ V3 ID (lsusb)
GRIDV3_ID_VENDOR = 0x1e71
GRIDV3_ID_PRODUCT = 0x1711

#Cpu sensor name ex:{coretmep, k10temp, ...}
CPU_TEMP_SENSOR = 'k10temp'

