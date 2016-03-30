# -*- coding: utf-8 -*-
from __future__ import print_function
import math

def rgb2frame(RGBData):
    """The RGBData param is array of arrays with R G and B elements in that order"""
    # start frame
    frame = bytearray([0x0, 0x0, 0x0, 0x0])
    # Leds
    for ledcolors in RGBData:
        frame.append(0xff)  # we do not want to use global dimming
        frame.append(ledcolors[2])
        frame.append(ledcolors[1])
        frame.append(ledcolors[0])
    # End frame
    eofbits = len(RGBData) / 2.0
    eof = bytearray([0xff] * int(math.ceil(eofbits/8.0)))
    return frame + eof
