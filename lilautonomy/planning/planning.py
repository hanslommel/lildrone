
import threading
import time as timelib

class PlanningBase:
    _lock = threading.Lock()
    _running = False
    _loop_dt = 0.1 #0.005
    _replan_dt = 3 #0.1
    _loop_last = timelib.time()
    _replan_last = _loop_last

    def __init__(self):
        print('Initializing PlanningBase')

    def replan(self):
        print('PlanningBase.update()')

    def loop(self):
        print('PlanningBase.loop()')
    
    def start(self):
        with self._lock:
            print('PlanningBase Start Running')
            self._running = True
    
    def stop(self):
        with self._lock:
            print('PlanningBase Stop Running')
            self._running = False
    
    def loop(self):
        while True:
            with self._lock:
                if self._running:
                    self._loop_last = timelib.time()

                    if self._loop_last > (self._replan_last + self._replan_dt):
                        self._replan_last = self._loop_last
                        self.replan()
                    
                    if timelib.time() < (self._loop_last + self._loop_dt):
                        timelib.sleep(self._loop_last + self._loop_dt - timelib.time())
                    else:
                        print('PlanningBase loop took too long')
                else:
                    print('Exiting PlanningBase loop')
                    break

class Planning(PlanningBase):
    def __init__(self):
        print('Initializing Planning')