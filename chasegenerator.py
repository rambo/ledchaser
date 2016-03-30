# -*- coding: utf-8 -*-
from __future__ import print_function
import chroma

try:
    from collections.abc import Iterator
except ImportError:
    from collections import Iterator


class Chasepattern(Iterator):
    """Generates chase patterns for N LEDs, operates in chroma.Color"""

    i = 0
    numleds = None
    basecolor = chroma.Color('#0E1024')
    chasecolor = chroma.Color('#FF8FFF')
    forever = False
    

    def __init__(self, numleds):
        self.numleds = numleds

    def next(self):
        return self.__next__()

    def __next__(self):
        pattern = [self.basecolor] * self.numleds
        chasepos = self.i % (self.numleds-1)
        pattern[chasepos] = self.chasecolor
        
        # TODO: add tail blending
        
        self.i += 1
        if self.i > self.numleds and not self.forever:
            raise StopIteration

        return pattern
