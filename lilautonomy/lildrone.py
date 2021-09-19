#!/usr/bin/python

import logging
import threading
import time as timelib

from multiwii import MultiWiiInterface, MultiWiiSim
from SE import StateEstimator
from mapping import mapping_test
from planning import planning_test

# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     for ii in range(10):
#         timelib.sleep(2)
#         logging.info("Thread %s: running", name)
#     logging.info("Thread %s: finishing", name)

# format = "%(asctime)s: %(message)s"
# logging.basicConfig(format=format, level=logging.INFO,
#                     datefmt="%H:%M:%S")

# logging.info("Main    : before creating thread")
# x = threading.Thread(target=thread_function, args=(1,))
# y = threading.Thread(target=thread_function, args=(2,))
# logging.info("Main    : before running threads")
# x.start()
# y.start()
# logging.info("Main    : wait for the threads to finish")
# # x.join()
# logging.info("Main    : all done")




# some settings
simulation = True
main_loop_dt = 1

# some setup
if simulation:
    FCInterface = MultiWiiSim()
else:
    FCInterface = MultiWiiInterface()

FCInterfaceThread = threading.Thread(target=FCInterface.loop) # could probably move thread into the Interface class
FCInterface.start()
FCInterfaceThread.start()

SE = StateEstimator()
SEThread = threading.Thread(target=SE.loop) # could probably move thread into the StateEstimator class
SE.start()
SEThread.start()

start_time = timelib.time()
time = start_time
while time < start_time + 10:
    print(f'time = {time}')

    # FCInterface.get()
    # se_test()
    # mapping_test()
    # planning_test()
    # FCInterface.set()

    # print('')

    timelib.sleep(time + main_loop_dt - timelib.time())

    time = time + main_loop_dt

FCInterface.stop()
FCInterfaceThread.join()
SE.stop()
SEThread.join()