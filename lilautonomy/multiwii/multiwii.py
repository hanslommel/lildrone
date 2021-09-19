
from yamspy import MSPy

class FCInterfaceBase:
    def __init__(self):
        print('Initializing FCInterfaceBase')

    def get(self):
        print('FCInterfaceBase.get()')
    
    def set(self):
        print('FCInterfaceBase.set()')

class MultiWiiInterface(FCInterfaceBase):
    board = None

    def __init__(self):
        print('MultiWiiInterface init')
        self.board = MSPy(device="/dev/serial0", loglevel='WARNING', baudrate=500000)

    def get(self):
        with self.board:
            self.board.fast_read_imu()

            accelerometer = self.board.SENSOR_DATA['accelerometer']
            gyroscope = self.board.SENSOR_DATA['gyroscope']

            print(accelerometer)
            print(gyroscope)

    def set(self):
        print('MultiWiiInterface.set placeholder')
        #with self.board:
            # disarm
            #CMDS['aux1'] = 1000
            #board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])

            # set throttle
            #CMDS['throttle'] = 988

            # arm
            #CMDS['aux1'] = 1800
            #board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])

            # mode
            #CMDS['aux2'] <= 1300 # Horizon mode
            #1700 > CMDS['aux2'] > 1300 # Flip Mode
            #CMDS['aux2'] >= 1700 # Angle Mode
            #board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])

            # roll
            #CMDS['roll'] = 1500
            #board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])

            # pitch
            #CMDS['pitch'] = 1500
            #board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])

class MultiWiiSim(FCInterfaceBase):

    def __init__(self):
        print('MultiWiiSim init')

    def get(self):
        print('MultiWiiSim get')
    
    def set(self):
        print('MultiWiiSim set')