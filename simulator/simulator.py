#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function

import os
import sys

import numpy as np
import visual
import zmq
from apa102parse import apa102parse
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream

ioloop.install()


DEBUG = False


class led(object):

    def __init__(self, radius, **kwargs):
        self.container = visual.frame(**kwargs)
        self.ledsphere = visual.sphere(
            frame=self.container, pos=(0, 0, 0),
            radius=radius, color=visual.color.white,
            material=visual.materials.emissive
        )
        self.ledlight = visual.local_light(frame=self.container, pos=(0, 0, 0), color=visual.color.white)

    @property
    def color(self):
        return self.ledlight.color

    @color.setter
    def color(self, value):
        self.ledsphere.color = value
        self.ledlight.color = value


class ledscene(object):

    def __init__(self, numleds, zmqstream, spacing=33, ledradius=15):
        self.numleds = numleds
        self.stream = zmqstream
        self.stream.on_recv_stream(self.frame_recv)

        visual.scene.width = 1500
        visual.scene.height = 80
        visual.scene.autoscale = True
        visual.scene.title = "Simulating %d LEDs" % self.numleds
        self.strip = visual.frame(pos=(self.numleds / 2 * spacing * -1, 0, 0))
        self.leds = []
        for x in xrange(self.numleds):
            self.leds.append(
                led(ledradius, frame=self.strip, pos=(x * spacing, 0, 0))
            )

    def frame_recv(self, stream, msg):
        ledquads = apa102parse(np.fromstring(msg[0], dtype=np.uint8))
        i = 0
        for quad in ledquads:
            self.leds[i].color = (quad[1] / 255.0, quad[2] / 255.0, quad[3] / 255.0)
            i += 1
            if i >= self.numleds:
                break
        stream.send("")

    def run(self):
        print("Running")
        try:
            visual.scene.visible = True
            visual.scene.autoscale = False
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            self.quit()

    def quit(self):
        print("Quitting")
        ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage ./simulator.py tcp://whatever:6969 numleds")
        sys.exit(1)

    DEBUG = bool(int(os.environ.get('DEBUG', '0')))

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(sys.argv[1])
    stream = ZMQStream(socket)

    ls = ledscene(int(sys.argv[2]), stream)
    ls.run()
