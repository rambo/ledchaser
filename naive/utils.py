# -*- coding: utf-8 -*-
from __future__ import print_function

def rgb_floats2bytes(r,g,b):
    return [ int(round(x*255)) for x in [r,g,b]]
