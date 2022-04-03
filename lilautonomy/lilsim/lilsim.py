import threading
import time as timelib
import shared_buffer
from multiwii import FCInterfaceBase
import time as timelib
from multiwii.imu_stream import IMUMessage, IMUStream


class LilSim(FCInterfaceBase):
    """Simulation class.
        Derived from the FCInterfaceBase class so that interface is identical to MultiWiiInterface base
    """

    def __init__(self, sb):
        print('LilSim init')
        self._get_dt = 1.0
        super(LilSim, self).__init__(sb)

    def get(self):
        print('LilSim get')
        acceleration = [0, 0, 9.8]
        rate = [0, 0, 0]
        msg = IMUMessage(timelib.time(), acceleration, rate)
        self._imu_stream.addOne(msg)
    
    def set(self):
        print('LilSim set')
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
                        print('LilSim loop took too long')
                else:
                    print('Exiting LilSim loop')
                    break
