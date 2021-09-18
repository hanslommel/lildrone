
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
    someState = 0

class MultiWiiController(ControllerBase):
    someGain = 0

def multiwii_get_test():
    print('MultiWii Get Test')

def multiwii_set_test():
    print('MultiWii Set Test')
