
from yamspy import MSPy

class SensorBase:
    def __init__(self):
        print('Initializing SensorBase')

    def get(self):
        print('SensorBase.get()')

class ControllerBase:
    def __init__(self):
        print('Initializing ControllerBase')

    def set(self):
        print('ControllerBase.set()')

class MultiWiiSensor(SensorBase):
    board = None

    def __init__(self):
        print('MultiWiiSensor init')
        board = MSPy(device="/dev/serial0", loglevel='WARNING', baudrate=500000)

    def get(self):
        board.fast_read_imu()

        accelerometer = board.SENSOR_DATA['accelerometer']
        gyroscope = board.SENSOR_DATA['gyroscope']
        #voltage = board.ANALOG['voltage']
        #attitude = board.SENSOR_DATA['kinematics']

        print(accelerometer)
        print(gyroscope)

class MultiWiiController(ControllerBase):
    someGain = 0

def multiwii_get_test():
    print('MultiWii Get Test')

def multiwii_set_test():
    print('MultiWii Set Test')
