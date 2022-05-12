#!/usr/bin/python

import logging
import threading
import time as timelib

from vpython import *
from multiwii import MultiWiiInterface 
from lilsim import LilSim
from SE import StateEstimator
from mapping import Mapping
from planning import Planning
from shared_buffer import SharedBuffer

# some settings
simulation = True
main_loop_dt = 1

# create the shared buffer
sb = SharedBuffer()

# some setup
if simulation:
    FCInterface = LilSim(sb, headless=True)
else:
    FCInterface = MultiWiiInterface(sb)

FCInterfaceThread = threading.Thread(target=FCInterface.loop) # could probably move thread into the Interface class
FCInterface.start()
FCInterfaceThread.start()

SE = StateEstimator(sb)
SEThread = threading.Thread(target=SE.loop) # could probably move thread into the StateEstimator class
SE.start()
SEThread.start()

Map = Mapping(sb)
MapThread = threading.Thread(target=Map.loop) # could probably move thread into the Mapping class
Map.start()
MapThread.start()

Planner = Planning(sb)
PlannerThread = threading.Thread(target=Planner.loop) # could probably move thread into the Planning class
Planner.start()
PlannerThread.start()

start_time = timelib.time()
time = start_time
while time < start_time + 10:
    print(f'time = {time}')
    print('')

    # create a vpython box object above
    # publish vehicle states in lilsim.py
    # add a subscriber to get them here
    # update box states here with box.rotate() or something

    timelib.sleep(time + main_loop_dt - timelib.time())

    time = time + main_loop_dt

FCInterface.stop()
FCInterfaceThread.join()
SE.stop()
SEThread.join()
Map.stop()
MapThread.join()
Planner.stop()
PlannerThread.join()