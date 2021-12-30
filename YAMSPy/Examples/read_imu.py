import sys
import struct
from yamspy import MSPy
import logging
import time


serial_port = "/dev/ttyAMA1"
logging.basicConfig(
    filename='imu.log',
    level=logging.INFO
    )

with MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200) as board:
    if board == 1:
        print("An error ocurred... probably the serial port is not available")
        sys.exit(1)
    else:
        i = 0
        while i <= 10000:
            if board.send_RAW_msg(MSPy.MSPCodes['MSP_RAW_IMU']):
                time_start = time.time()
                # $ + M + < + data_length + msg_code + data + msg_crc
                # 6 bytes + data_length
                # data_length: 9 x 2 = 18 bytes
                data_length = 18
                msg = board.receive_raw_msg(size = (6+data_length))[5:]
                converted_msg = struct.unpack('<%dh' % (data_length/2) , msg[:-1])

                # /512 for mpu6050, /256 for mma
                # currently we are unable to differentiate between the sensor types, so we are going with 512
                # And what about SENSOR_CONFIG???
                board.SENSOR_DATA['accelerometer'][0] = converted_msg[0]
                board.SENSOR_DATA['accelerometer'][1] = converted_msg[1]
                board.SENSOR_DATA['accelerometer'][2] = converted_msg[2]

                # properly scaled (INAV and BF use the same * (4 / 16.4))
                # but this is supposed to be RAW, so raw it is!
                board.SENSOR_DATA['gyroscope'][0] = converted_msg[3]
                board.SENSOR_DATA['gyroscope'][1] = converted_msg[4]
                board.SENSOR_DATA['gyroscope'][2] = converted_msg[5]

                # add timestamp
                timestamp = time.time()

                imu_rate = time.time() - time_start

                print([converted_msg[:6], timestamp, imu_rate])
                logging.info([converted_msg[:6], timestamp, imu_rate])
                i += 1
