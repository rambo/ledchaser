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
    pattern.forever = True
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(sys.argv[1])

    if len(sys.argv) >= 4:
        pattern.basecolor = chroma.Color(sys.argv[3])

    if len(sys.argv) >= 5:
        pattern.chasecolor = chroma.Color(sys.argv[4])
    
    delay = 0.005
    if len(sys.argv) >= 6:
        delay = float(sys.argv[5])

    try:
        doread = False
        while True:
            tstart = time.time()
            if doread:
                # We must read the reply even though it's empty
                socket.recv()
                doread = False
            try:
                frame = colors2frame(pattern.__next__())
            except StopIteration:
                break
            adelay = (tstart+delay) - time.time()
            if adelay > 0:
                time.sleep(adelay)
            else:
                if DEBUG:
                    print("%f: Missed deadline!" % time.time())
            if DEBUG:
                print("%f: sending: %s" % (tstart, repr(frame)))
            socket.send(frame)
            doread = True
    except KeyboardInterrupt:
        pass

    if doread:
        socket.recv()
        doread = False
    socket.send(colors2frame([chroma.Color("#000000")]*pattern.numleds))
    # We must read the reply even though it's empty
    socket.recv()
