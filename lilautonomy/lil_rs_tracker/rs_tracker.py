
import threading
import time as timelib

import numpy as np
import cv2
from scipy import optimize
import pyrealsense2.pyrealsense2 as rs
import scipy.interpolate
import time


# what you will do:
        # two image test will get split into init and process image
        # enable_stream will be in init or start
        # anything we expect to see in the loop needs to be a member in this init
        # define last_image and ir_np etc. in init, will be used in process image
        # next time... FLY

class RSTracker:
    _lock = threading.Lock()
    _running = False
    _loop_dt = 0.2 #0.005
    _image_dt = 1 #0.1
    _loop_last = timelib.time()
    _image_last = _loop_last
    _sb = None

    def __init__(self, sb):
        print('Initializing RSTracker')
        self._sb = sb.getInstance()

    def start(self):
        with self._lock:
            print('RSTracker Start Running')
            # RealSense stream setup
            self.pipeline = rs.pipeline()
            config = rs.config()
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
            pipeline_profile = self.pipeline.start(config)
            device = pipeline_profile.get_device()
            depth_sensor = device.query_sensors()[0]
            depth_sensor.set_option(rs.option.emitter_on_off, 1)

            # params for ShiTomasi corner detection
            self.feature_params = dict(maxCorners = 60,
                            qualityLevel = 0.5,
                            minDistance = 40,
                            blockSize = 7)
            # Parameters for lucas kanade optical flow
            self.lk_params = dict(winSize = (5, 5),
                            maxLevel = 5,
                            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.3),)

            # initialize numpy arrays
            self.last_image = np.array([])
            self.ir_np = np.array([])
            self.scaled_depth = np.array([])
            self.p0 = []
            self.h_x = 0
            self.h_y = 0
            self.h_z = 0
            self.p0_depth = np.array([])
            self.pts_diff = np.array([])

            self._running = True

    def bilinear_interpolate_scipy(self, image, x, y):
        y_indices = np.arange(image.shape[0])
        x_indices = np.arange(image.shape[1])
        interp_func = scipy.interpolate.interp2d(x_indices, y_indices, image, kind='linear')
        return interp_func(x,y)

    def some_function(self, x, image1, image2):
        # this is super slow, maybe numpy has a way to do this?
        # try pyrealsense2.align?
        E = 0
        N = 0
        for iy, ix in np.ndindex(image1.shape):
            depth2_est = image1[iy, ix]
            depth2 = self.bilinear_interpolate_scipy(image2, iy + x[0], ix + x[1])
            E = E + (depth2_est - depth2)**2
            N = N + 1
        return E/N # average squared error

    def optical_flow(self, new_image, old_image, depth, p0):
        print("** optical_flow func start **")
        frame = np.array([])

        # ones_like!
        mask = 255*np.ones_like(old_image)

        print("length of p0: ", len(p0))
        if len(p0) <= 10:
            for point in p0:
                mask = cv2.circle(mask, (int(point[0][0]), int(point[0][1])), 5, 0, -1)
            #cv2.imshow("jimmy", mask)
            new_features = cv2.goodFeaturesToTrack(old_image, mask=mask, **self.feature_params)

            print("new features type: ", type(new_features))
            print("length of p0: ", len(p0))
            if type(new_features) == None:
                print("new features returned nonetype")
                new_features = p0
            if len(p0) == 0:
                p0 = new_features
            else:
                try:
                    p0 = np.concatenate((p0, new_features), axis=0)
                except ValueError as err:
                    print(err)
                    p0 = new_features

        p1, st, err = cv2.calcOpticalFlowPyrLK(old_image, new_image, p0, None, **self.lk_params)

        if p1 is not None:
            good_new = p1[st==1]
            good_old = p0[st==1]

        mask = np.zeros_like(old_image)
        color = np.random.randint(254, 255, (100, 3))

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            # end coordinates x, y, z
            a, b = new.ravel()
            print(" ~ int a from ravel: ", a)
            if a < 640 and b < 480:
                e = depth[int(b - 1), int(a - 1)]
                e_disp = 2*round(0.5*e)
            else:
                e = 0
                print("wtf")
            # start coordinates x, y
            c, d = old.ravel()
            if c < 640 and d < 480:
                f = depth[int(d - 1), int(c - 1)]
                f_disp = 2*round(0.5*f)
            else:
                f = 0
                print("wtf")

            self.p0_depth = np.append(self.p0_depth, (a, b, e))

            dim1 = (int(a) - int(c))
            dim2 = (int(b) - int(d))
            dim3 = (int(e) - int(f))
            self.pts_diff = np.append(self.pts_diff, (dim1, dim2, dim3))

            mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
            frame = cv2.circle(old_image, (int(c), int(d)), 5, color[i].tolist(), -1)

            # write some depths at each point we're tracking
            font = cv2.FONT_HERSHEY_SIMPLEX
            coordText = (int(c), int(d))
            fontScale = 0.5
            fontColor = (255,255,255)
            thickness = 1
            lineType = 2

            cv2.putText(frame, str(e_disp),
                coordText,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)

        if frame.any():
            img = cv2.add(frame, mask)
            cv2.imshow('frame', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            return

        try:
            # Now update the previous frame and previous points
            self.p0 = good_new.reshape(-1, 1, 2)
            print("x diff array: ", self.pts_diff[0])
            avg_0 = np.average(self.pts_diff[0])
            avg_1 = np.average(self.pts_diff[1])
            avg_2 = np.average(self.pts_diff[2])

            pts_diff_avg = [avg_0, avg_1, avg_2]
            print("avg diff xyz: ", pts_diff_avg)
            dims = [dim1, dim2, dim3]
            #print(dims)
            return self.p0, pts_diff_avg, self.p0_depth
        except UnboundLocalError as err:
            dims = [0, 0, 0]
            pts_diff_avg = dims
            print("no dims found, setting to zero: ", dims)
            return self.p0, pts_diff_avg, self.p0_depth
        except IndexError as err:
            dims = [0, 0, 0]
            pts_diff_avg = dims
            print("pts_diff empty! setting to zero: ", dims)
            return self.p0, pts_diff_avg, self.p0_depth

    def stop(self):
        with self._lock:
            print('RSTracker Stop Running')
            self.pipeline.stop()
            self._running = False

    def process_image(self):
            #do all the stuff
            # TODO: not getting emitter off messages, later in loop it just gets even number frames for some reason?
        try:
            #while True:
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            ir_frame = frames.get_infrared_frame(1)
            emitter = rs.depth_frame.get_frame_metadata(
                depth_frame,
                rs.frame_metadata_value.frame_laser_power_mode,
                )
            print("emitter: ", emitter)

            frames_2 = self.pipeline.wait_for_frames()
            ir_frame_2 = frames_2.get_infrared_frame(1)
            emitter_2 = rs.depth_frame.get_frame_metadata(
                ir_frame_2,
                rs.frame_metadata_value.frame_laser_power_mode,
                )
            print("emitter_2: ", emitter_2)

            frame_number = frames.get_frame_number()
            print("frame: ", frame_number)

            if emitter:
                print("emitter on, using depth image")
                depth = frames.get_depth_frame()
                if not depth:
                    print("no depth image")
                    return

                # depth_image = np.asanyarray(depth.get_data())
                # self.scaled_depth = cv2.convertScaleAbs(depth_image, alpha=0.08)

                self.ir_np = np.asanyarray(ir_frame_2.get_data())
                self.last_image = self.ir_np

                #depth_colormap = cv2.applyColorMap(scaled_depth, cv2.COLORMAP_JET)
                #print("** displaying Realsense **")
                #cv2.imshow('RealSense', depth_colormap)
                # return

            else:
                depth = frames_2.get_depth_frame()
                self.ir_np = np.asanyarray(ir_frame.get_data())
                self.last_image = self.ir_np

            depth_image = np.asanyarray(depth.get_data())
            self.scaled_depth = cv2.convertScaleAbs(depth_image, alpha=0.08)

            if np.any(self.last_image) and np.any(self.scaled_depth):
                print("** images detected, running optical flow **")
                self.last_image = np.asanyarray(self.last_image)
                self.scaled_depth = np.asanyarray(self.scaled_depth)
                self.p0, pts_diff_avg, self.p0_depth = self.optical_flow(
                    self.ir_np,
                    self.last_image,
                    self.scaled_depth,
                    self.p0,
                    )

                print("opt_flow: ", pts_diff_avg)
                # add flow dims to show heading
                self.h_x = (self.h_x + pts_diff_avg[0])
                self.h_y = (self.h_y + pts_diff_avg[1])
                self.h_z = (self.h_z + pts_diff_avg[2])
                headings = [self.h_x, self.h_y, self.h_z]

                print("headings xyz: ", headings)

            self.last_image = self.ir_np

            #depth_colormap = cv2.applyColorMap(scaled_depth, cv2.COLORMAP_JET)
            #cv2.imshow('RealSense', depth_colormap)

            print("of some kind")

        finally:
            if not self._running:
                self.pipeline.stop()


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
