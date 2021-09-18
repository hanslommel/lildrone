
import time as timelib

from multiwii import multiwii_get_test, multiwii_set_test, MultiWiiSensor, MultiWiiController
from SE import se_test
from mapping import mapping_test
from planning import planning_test

# some settings
simulateSensors = False
simulateControls = False
timestep = 0.1

# some setup
#if simulateSensors:
    #getData = sensorsSim()
#else:
getData = MultiWiiSensor()

#if simulateControls:
#    setData = controlsSim()
#else:
setData = MultiWiiController()

#SE = stateEstimator()

start_time = timelib.time()
time = start_time
while time < start_time + 10:
    print(f'time = {time}')

    multiwii_get_test()
    se_test()
    mapping_test()
    planning_test()
    multiwii_set_test()

    print('')

    timelib.sleep(time + timestep - timelib.time())

    time = time + timestep
