
import threading
import time as timelib

class RSTracker:
    _lock = threading.Lock()
    _running = False
    _loop_dt = 0.01 #0.005
    _image_dt = 1 #0.1
    _loop_last = timelib.time()
    _image_last = _loop_last
    _sb = None

    def __init__(self, sb):
        print('Initializing RSTracker')
        self._sb = sb.getInstance()
        # what you will do:
        # two image test will get split into init and process image
        # enable_stream will be in init or start
        # anything we expect to see in the loop needs to be a member in this init
        # define last_image and ir_np etc. in init, will be used in process image
        # next time... FLY

    def start(self):
        with self._lock:
            print('RSTracker Start Running')
            self._running = True

    def stop(self):
        with self._lock:
            print('RSTracker Stop Running')
            self._running = False

    def process_image(self):
        #do all the stuff
        print("of some kind")
        pass

    def loop(self):
        while True:
            with self._lock:
                if self._running:
                    self._loop_last = timelib.time()

                    if self._loop_last > (self._image_last + self._image_dt):
                        self._image_last = self._loop_last
                        self.process_image()
                    
                    if timelib.time() < (self._loop_last + self._loop_dt):
                        timelib.sleep(self._loop_last + self._loop_dt - timelib.time())
                    else:
                        print('RSTracker loop took too long')
                else:
                    print('Exiting RSTracker loop')
                    break
