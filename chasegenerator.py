# -*- coding: utf-8 -*-
from __future__ import division, print_function

import math

import chroma
import numpy as np

try:
    from collections.abc import Iterator
except ImportError:
    from collections import Iterator

APA102_FRAME_START_SIZE = 4


class Chasepattern(Iterator):
    """Generates chase patterns for N LEDs, operates in chroma.Color"""

    i = 0
    _numleds = None
    _basecolor = chroma.Color('#000000')
    _chasecolor = chroma.Color('#000000')
    _tailsize = 5
    _tailinterval = 0
    _numtails = 1
    forever = False
    pattern = None
    chasepattern = None
    frame = None
    reverse = False

    def __init__(self, numleds):
        self.numleds = numleds
        self.basecolor = chroma.Color('#0E1024')
        self.chasecolor = chroma.Color('#FF8FFF')
        self._tailinterval = self._numleds / self._numtails

    @property
    def basecolor(self):
        return self._basecolor

    @basecolor.setter
    def basecolor(self, value):
        self._basecolor = value
        # TODO: Gamma-correct ??
        rgbbytes = self._basecolor.rgb256
        self.pattern[:] = [0xff, rgbbytes[2], rgbbytes[1], rgbbytes[0]]
        self.recalculate_chase_mix()

    @property
    def chasecolor(self):
        return self._chasecolor

    @chasecolor.setter
    def chasecolor(self, value):
        self._chasecolor = value
        self.recalculate_chase_mix()

    @property
    def tailsize(self):
        return self._tailsize

    @tailsize.setter
    def tailsize(self, value):
        self._tailsize = value
        self.recalculate_chase_mix()

    @property
    def numtails(self):
        return self._numtails

    @numtails.setter
    def numtails(self, value):
        self._numtails = value
        # Trigger base refill
        self.basecolor = self.basecolor
        self._tailinterval = self._numleds / self._numtails

    def recalculate_chase_mix(self):
        self.chasepattern = np.zeros([1 + self._tailsize, 4], np.uint8)
        # TODO: Gamma-correct ??
        rgbbytes = self._chasecolor.rgb256
        self.chasepattern[-1] = [0xff, rgbbytes[2], rgbbytes[1], rgbbytes[0]]
        for x in range(self._tailsize):
            tailcolor = chroma.Color(self._chasecolor)
            tailcolor.alpha = 1.0 / self._tailsize * x
            blended = self._basecolor + tailcolor
            rgbbytes = blended.rgb256
            self.chasepattern[x] = [0xff, rgbbytes[2], rgbbytes[1], rgbbytes[0]]

    @property
    def numleds(self):
        return self._numleds

    @numleds.setter
    def numleds(self, value):
        self._numleds = value
        self.pattern = np.zeros([value, 4], np.uint8)
        self.initialize_frame()

    def initialize_frame(self):
        eofbits = self._numleds / 2.0
        eofbytes = int(math.ceil(eofbits / 8.0))
        self.frame = np.zeros(self.pattern.size + APA102_FRAME_START_SIZE + eofbytes, np.uint8)
        self.frame[-eofbytes:] = 0xff

    def next(self):
        return self.__next__()

    def _position_single_tail(self, chasepos):
        # TODO make this case work too.
        if chasepos < 0:
            return
        tailend = chasepos - len(self.chasepattern)
        # TODO: Gamma-correct ??
        rgbbytes = self._basecolor.rgb256
        self.pattern[tailend - 1] = [0xff, rgbbytes[2], rgbbytes[1], rgbbytes[0]]
        if tailend < 0:
            self.pattern[tailend:] = self.chasepattern[0:abs(tailend)]
            self.pattern[0:chasepos] = self.chasepattern[abs(tailend):]
        else:
            self.pattern[tailend:chasepos] = self.chasepattern

    def __next__(self):
        chasepos = self.i % (self._numleds - 1)
        for x in range(self._numtails):
            self._position_single_tail(chasepos - x*self._tailinterval)

        if self.reverse:
            self.frame[APA102_FRAME_START_SIZE:self.pattern.size + APA102_FRAME_START_SIZE] = np.flipud(self.pattern).flatten()
        else:
            self.frame[APA102_FRAME_START_SIZE:self.pattern.size + APA102_FRAME_START_SIZE] = self.pattern.flatten()

        self.i += 1
        if self.i > self.numleds and not self.forever:
            raise StopIteration

        return self.frame
