# -*- coding: utf-8 -*-
from __future__ import print_function

import math


def apa102parse(framedata):
    """We assume the framedata is already a numpy array"""
    # How many groups of 4 bytes do we have ?
    wholequads = math.floor(len(framedata) / 4.0)
    # Slice and reshape the raw data to get the led values and lose the start-of-frame
    return framedata[:wholequads * 4].reshape(wholequads, 4)[1:]
