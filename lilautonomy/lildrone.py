
import time as timelib

from sensors import sensor_test
from SE import se_test
from mapping import mapping_test
from planning import planning_test

timestep = 0.1
start_time = timelib.time()
time = start_time
while time < start_time + 10:
    print(f'time = {time}')
    sensor_test()
    se_test()
    mapping_test()
    planning_test()
    print('')

    timelib.sleep(time + timestep - timelib.time())

    time = time + timestep
