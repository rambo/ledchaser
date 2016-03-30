#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from future.builtins import next, object
import sys,os,time

from .chasegenerator import Chasepattern
from .apa102 import colors2frame

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage ./play.py tcp://whatever:6969 numleds [basecolor] [chasecolor] [delay_in_seconds]"
        sys.exit(1)
    
    pattern = Chasepattern(int(sys.argv[2]))
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(sys.argv[1])

    if len(sys.argv) >= 4:
        pattern.basecolor = chroma.Color(sys.argv[3])

    if len(sys.argv) >= 5:
        pattern.chasecolor = chroma.Color(sys.argv[4])
    
    delay = 0.25
    if len(sys.argv) >= 6:
        delay = float(sys.argv[5])

    for colordata in pattern:
        print("%f sending: %s" % (time.time(), repr(colordata)))
        socket.send(colors2frame(colordata))
        # We must read the reply even though it's empty
        rpl = socket.recv()
        time.sleep(delay)
