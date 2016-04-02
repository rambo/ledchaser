#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import zmq
import chroma
import sys,os,time

from chasegenerator import Chasepattern
from apa102 import colors2frame

DEBUG=True

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
    
    delay = 0.025
    if len(sys.argv) >= 6:
        delay = float(sys.argv[5])

    try:
        try:
            sent = False
            while True:
                tstart = time.time()
                if sent:
                    # We must read the reply even though it's empty
                    socket.recv()
                frame = colors2frame(pattern.__next__())
                adelay = (tstart+delay) - time.time()
                if adelay > 0:
                    time.sleep(adelay)
                else:
                    if DEBUG:
                        print("%f: Missed deadline!" % time.time())
                if DEBUG:
                    print("%f: sending: %s" % (tstart, repr(frame)))
                socket.send(frame)
                sent = True
        except StopIteration:
            pass
    except KeyboardInterrupt:
        pass

    socket.send(colors2frame([chroma.Color("#000000")]*pattern.numleds))
    # We must read the reply even though it's empty
    socket.recv()
