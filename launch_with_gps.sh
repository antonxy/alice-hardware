#!/bin/bash

cd /home/pi/git/alice-hardware

screen -dmS alice-hardware python main.py
screen -dmS alice-hardware-gps python android_gps_proxy.py
