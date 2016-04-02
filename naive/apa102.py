# -*- coding: utf-8 -*-
from __future__ import print_function
import math
from utils import rgb_floats2bytes

def colors2frame(colors):
    """The colors param is array chroma.Color objects"""
    # start frame
    frame = bytearray([0x0, 0x0, 0x0, 0x0])
    # Leds
    for color in colors:
        frame.append(0xff)  # we do not want to use global dimming
        rgbbytes = color.rgb256
        frame.append(rgbbytes[2])
        frame.append(rgbbytes[1])
        frame.append(rgbbytes[0])
    # End frame
    eofbits = len(colors) / 2.0
    eof = bytearray([0xff] * int(math.ceil(eofbits/8.0)))
    return frame + eof
