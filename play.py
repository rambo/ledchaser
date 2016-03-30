#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import zmq
import chroma
import sys,os,time

from chasegenerator import Chasepattern
from apa102 import colors2frame

DEBUG=False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage ./play.py tcp://whatever:6969 numleds [basecolor] [chasecolor] [delay_in_seconds]")
        sys.exit(1)
    
    pattern = Chasepattern(int(sys.argv[2]))
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(sys.argv[1])

    if len(sys.argv) >= 4:
        pattern.basecolor = chroma.Color(sys.argv[3])

    if len(sys.argv) >= 5:
        pattern.chasecolor = chroma.Color(sys.argv[4])
    
    delay = 0.1
    if len(sys.argv) >= 6:
        delay = float(sys.argv[5])

    for colordata in pattern:
        tstart = time.time()
        if DEBUG:
            print("%f: sending: %s" % (tstart, repr(colordata)))
        socket.send(colors2frame(colordata))
        # We must read the reply even though it's empty
        rpl = socket.recv()
        adelay = (tstart+delay) - time.time()
        if adelay > 0:
            time.sleep(adelay)
        else:
            if DEBUG:
                print("%f: Missed deadline!" % time.time())

    socket.send(colors2frame([chroma.Color("#000000")]*pattern.numleds))
    # We must read the reply even though it's empty
    rpl = socket.recv()
