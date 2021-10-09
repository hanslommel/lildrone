
from yamspy import MSPy
import threading
import time as timelib
import shared_buffer
from .imu_stream import IMUMessage, IMUStream

class FCInterfaceBase:
    _lock = threading.Lock()
    _running = False
    _loop_dt = 0.1 #0.005
    _get_dt = 5 #0.01
    _set_dt = 3 #0.01
    _loop_last = timelib.time()
    _get_last = _loop_last
    _set_last = _loop_last
    _sb = None
    _imu_stream = None

    def __init__(self, sb):
        print('Initializing FCInterfaceBase')
        self._sb = sb.getInstance()
        self._imu_stream = IMUStream()
        self._sb.register(self._imu_stream, "IMU")

    def get(self):
        print('FCInterfaceBase.get()')
    
    def set(self):
        print('FCInterfaceBase.set()')
    
    def start(self):
        with self._lock:
            print('FCInterface Start Running')
            self._running = True
    
    def stop(self):
        with self._lock:
            print('FCInterface Stop Running')
            self._running = False
    
    def loop(self):
        while True:
            with self._lock:
                if self._running:
                    self._loop_last = timelib.time()

                    if self._loop_last > (self._get_last + self._get_dt):
                        self._get_last = self._loop_last
                        self.get()
                    
                    if self._loop_last > (self._set_last + self._set_dt):
                        self._set_last = self._loop_last
                        self.set()
                    
                    if timelib.time() < (self._loop_last + self._loop_dt):
                        timelib.sleep(self._loop_last + self._loop_dt - timelib.time())
                    else:
                        print('FCInterfaceBase loop took too long')
                else:
                    print('Exiting FCInterfaceBase loop')
                    break

class MultiWiiInterface(FCInterfaceBase):
    board = None

    def __init__(self, sb):
        print('MultiWiiInterface init')
        self.board = MSPy(device="/dev/serial0", loglevel='WARNING', baudrate=500000)
        self._loop_dt = 0.05 #0.005
        self._get_dt = 0.1 #0.01
        self._set_dt = 1 #0.01
        super(MultiWiiInterface, self).__init__(sb)

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
    
    
    # def start(self):  -- using base class
    # def stop(self):   -- using base class
    
    def loop(self):
        while True:
            with self._lock:
                if self._running:
                    self._loop_last = timelib.time()

                    if self._loop_last > (self._get_last + self._get_dt):
                        self._get_last = self._loop_last
                        self.get()
                    
                    if self._loop_last > (self._set_last + self._set_dt):
                        self._set_last = self._loop_last
                        self.set()
                    
                    if timelib.time() < (self._loop_last + self._loop_dt):
                        timelib.sleep(self._loop_last + self._loop_dt - timelib.time())
                    else:
                        print('MultiWiiInterface loop took too long')
                else:
                    print('Exiting MultiWiiInterface loop')
                    break



class MultiWiiSim(FCInterfaceBase):
    """MultiWii simulation class.

    In fact, this is the entire simulation for now.  Later we should reorganize and just have the 
    MultiWii sim here and move the rest to a simulation package.
    """

    def __init__(self, sb):
        print('MultiWiiSim init')
        self._get_dt = 1.0
        super(MultiWiiSim, self).__init__(sb)

    def get(self):
        print('MultiWiiSim get')
        acceleration = [0, 0, 9.8]
        rate = [0, 0, 0]
        msg = IMUMessage(timelib.time(), acceleration, rate)
        self._imu_stream.addOne(msg)
    
    def set(self):
        print('MultiWiiSim set')
        print(self._sb)
    
    def loop(self):
        while True:
            with self._lock:
                if self._running:
                    self._loop_last = timelib.time()

                    if self._loop_last > (self._get_last + self._get_dt):
                        self._get_last = self._loop_last
                        self.get()
                    
                    if self._loop_last > (self._set_last + self._set_dt):
                        self._set_last = self._loop_last
                        self.set()
                    
                    if timelib.time() < (self._loop_last + self._loop_dt):
                        timelib.sleep(self._loop_last + self._loop_dt - timelib.time())
                    else:
                        print('MultiWiiSim loop took too long')
                else:
                    print('Exiting MultiWiiSim loop')
                    break