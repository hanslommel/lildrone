import os
import signal
from vpython import *
import re
import time

# set up visualization model
ptr = box(up=vector(0,1,0), color=color.blue, length=3, height=0.4, width=3)

log_path = 'imu.log'

with open(log_path, 'r') as imu_log:
    x_val = 0
    y_val = 0
    z_val = 0
    for line in imu_log:
        try:
            entry = imu_log.readline()
            entry_list = [i for i in re.findall(r'[-+]?\d+(?:\.\d+)?', entry) if i]

            print(f'x: {entry_list[0]} y: {entry_list[1]} z: {entry_list[2]}')

            # pete help me with maths plz i don't know how :(
            x_ang = int(entry_list[3]) - x_val
            y_ang = int(entry_list[4]) - y_val
            z_ang = int(entry_list[5]) - z_val

            ptr.rotate(angle=(x_ang / 1800), axis=vector(0,0,1))
            ptr.rotate(angle=(y_ang / 1800), axis=vector(1,0,0))
            ptr.rotate(angle=(z_ang / 1800), axis=vector(0,1,0))

            x_val = x_ang
            y_val = y_ang
            z_val = z_ang
            time.sleep(0.009)

        except IndexError as err:
            print(err)
            print('end of file?')
            os.kill(os.getpid(), signal.SIGINT)
            break