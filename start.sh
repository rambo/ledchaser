#!/bin/bash
source /root/.virtualenvs/ledchaser-34/bin/activate  && cd /usr/src/ledchaser/ && nohup python play.py ipc:///tmp/zmqspi 1500 &

