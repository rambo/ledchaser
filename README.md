# Led chase pattern thingy for APA102 strips

Uses spidev and <https://github.com/HelsinkiHacklab/ledmatrix/tree/master/spidev_zmq> to command the LEDs

save yourself some trouble and `apt-get install python-zmq python-numpy` (or `apt-get install python3-zmq python3-numpy`) 
and `toggleglobalsitepackages` (you *ARE* using virtualenvwrapper, right ?), instead of compiling them via pip.

## APA102 info

<https://cpldcpu.wordpress.com/2014/11/30/understanding-the-apa102-superled/> is probably best source.

## Simulator

To test your own patterns there's a [VPython](http://vpython.org/) based simulation, it takes the same frame format
as the real LED strip over ZMQ socket like the spidev bridge does. Use with `./simulator.py ipc:///tmp/zmqspi n_leds`.

## Player

A simple rainbow rotation and chase animation, use with `./play.py ipc:///tmp/zmqspi n_leds`

## 3D models of regulator cases

In the cloud <http://a360.co/1T23AY5> allows for download in various formats. Original design in Autodesk Fusion 360

## Slides of the PyMeetup talk

<./pymeetup_20160601.pdf>

The weird disc thing on slide 16 is a video, see <https://www.youtube.com/watch?v=mgMRCToBlbo>
