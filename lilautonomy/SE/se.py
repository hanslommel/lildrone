
import threading
import time as timelib

class StateEstimatorBase:
    _lock = threading.Lock()
    _running = False
    _loop_dt = 0.1 #0.005
    _propagate_dt = 1 #0.01
    _update_dt = 3 #0.1
    _loop_last = timelib.time()
    _propagate_last = _loop_last
    _update_last = _loop_last

    def __init__(self):
        print('Initializing StateEstimatorBase')

    def propagate(self):
        print('StateEstimatorBase.propagate()')
    
    def update(self):
        print('StateEstimatorBase.update()')

    def loop(self):
        print('StateEstimatorBase.loop()')
    
    def start(self):
        with self._lock:
            print('StateEstimatorBase Start Running')
            self._running = True
    
    def stop(self):
        with self._lock:
            print('StateEstimatorBase Stop Running')
            self._running = False
    
    def loop(self):
        while True:
            with self._lock:
                if self._running:
                    self._loop_last = timelib.time()

                    if self._loop_last > (self._propagate_last + self._propagate_dt):
                        self._propagate_last = self._loop_last
                        self.propagate()
                    
                    if self._loop_last > (self._update_last + self._update_dt):
                        self._update_last = self._loop_last
                        self.update()
                    
                    if timelib.time() < (self._loop_last + self._loop_dt):
                        timelib.sleep(self._loop_last + self._loop_dt - timelib.time())
                    else:
                        print('StateEstimatorBase loop took too long')
                else:
                    print('Exiting StateEstimatorBase loop')
                    break

class StateEstimator(StateEstimatorBase):
    def __init__(self):
        print('Initializing StateEstimator')