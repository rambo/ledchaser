# Led chase pattern thingy for APA102 strips

Uses spidev and <https://github.com/HelsinkiHacklab/ledmatrix/tree/master/spidev_zmq> to command the LEDs

save yourself some trouble and `apt-get install python-zmq python-numpy` (or `apt-get install python3-zmq python3-numpy`) 
and `toggleglobalsitepackages` (you *ARE* using virtualenvwrapper, right ?), instead of compiling them via pip.
