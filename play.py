#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import time

import zmq
from chasegenerator import Chasepattern

import chroma

DEBUG = False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage ./play.py tcp://whatever:6969 numleds [basecolor] [chasecolor] [delay_in_seconds]")
        sys.exit(1)

    DEBUG = bool(int(os.environ.get('DEBUG', '0')))

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
            adelay = (tstart + delay) - time.time()
            try:
                frame = pattern.__next__()
                ba = bytearray(frame)
            except StopIteration:
                break
            if adelay > 0:
                time.sleep(adelay)
            else:
                if DEBUG:
                    print("%f: Missed deadline!" % time.time())
            if DEBUG:
                #print("%f: pattern: %s" % (tstart, repr(pattern.pattern)))
                print("%f: sending: %s" % (tstart, repr(ba)))
            socket.send(ba)
            doread = True
    except KeyboardInterrupt:
        pass

    pattern.basecolor = chroma.Color("#000000")
    pattern.chasecolor = chroma.Color("#000000")
    pattern.i = 0
    frame = pattern.__next__()
    if doread:
        socket.recv()
        doread = False
    socket.send(bytearray(frame))
    # We must read the reply even though it's empty
    socket.recv()
