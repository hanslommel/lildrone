
import time as timelib

from multiwii import MultiWiiInterface, MultiWiiSim
from SE import se_test
from mapping import mapping_test
from planning import planning_test

# some settings
simulation = True
timestep = 0.1

# some setup
if simulation:
    FCInterface = MultiWiiSim()
else:
    FCInterface = MultiWiiInterface()

#SE = stateEstimator()

start_time = timelib.time()
time = start_time
while time < start_time + 10:
    print(f'time = {time}')

    FCInterface.get()
    se_test()
    mapping_test()
    planning_test()
    FCInterface.set()

    print('')

    timelib.sleep(time + timestep - timelib.time())

    time = time + timestep
