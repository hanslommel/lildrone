import argparse
import numpy as np
import cv2
from scipy import optimize
#import pyrealsense2.pyrealsense2 as rs
import scipy.interpolate
import time

# image playback
from PIL import Image
import glob

# plotting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


parser = argparse.ArgumentParser()
parser.add_argument("--playback_images",
                    action='store_true',
                    help="plays back depth and IR images from file")
args = parser.parse_args()

# don't import pyrealsense2 if playing back locally
if not args.playback_images:
    import pyrealsense2.pyrealsense2 as rs

def bilinear_interpolate_scipy(image, x, y):
    y_indices = np.arange(image.shape[0])
    x_indices = np.arange(image.shape[1])
    interp_func = scipy.interpolate.interp2d(x_indices, y_indices, image, kind='linear')
    return interp_func(x,y)

def some_function(x, image1, image2):
    # this is super slow, maybe numpy has a way to do this?
    # try pyrealsense2.align?
    E = 0
    N = 0
    for iy, ix in np.ndindex(image1.shape):
        depth2_est = image1[iy, ix]
        depth2 = bilinear_interpolate_scipy(image2, iy + x[0], ix + x[1])
        E = E + (depth2_est - depth2)**2
        N = N + 1
    return E/N # average squared error

    #return (x[0] - 3)**2 + (x[1] - 5)**2

def optical_flow(new_image, old_image, depth, p0):

    frame = np.array([])
    # params for ShiTomasi corner detection
    feature_params = dict(maxCorners = 30,
                        qualityLevel = 0.2,
                        minDistance = 30,
                        blockSize = 7)
    # Parameters for lucas kanade optical flow
    lk_params = dict(winSize = (20, 20),
                    maxLevel = 3,
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),)

    # old_image = cv2.cvtColor(old_image, cv2.COLOR_BGR2GRAY)
    # new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    # ones_like!
    mask = 255*np.ones_like(old_image)

    if len(p0) <= 10:
        for point in p0:
            mask = cv2.circle(mask, (int(point[0][0]), int(point[0][1])), 5, 0, -1)
        cv2.imshow("jimmy", mask)
        new_features = cv2.goodFeaturesToTrack(old_image, mask=mask, **feature_params)
        if len(p0) == 0:
            p0 = new_features
        else:
            p0 = np.concatenate((p0, new_features), axis=0)

    p1, st, err = cv2.calcOpticalFlowPyrLK(old_image, new_image, p0, None, **lk_params)

    if p1 is not None:
        good_new = p1[st==1]
        good_old = p0[st==1]

    mask = np.zeros_like(old_image)
    color = np.random.randint(254, 255, (100, 3))

    p0_depth = np.array([])

    for i, (new, old) in enumerate(zip(good_new, good_old)):
        # end coordinates x, y, z
        a, b = new.ravel()
        if a < 640 and b < 480:
            e = 10*round(0.1*depth[int(b - 1), int(a - 1)])
        else:
            e = 0
            print("wtf")
        # start coordinates x, y
        c, d = old.ravel()
        if c < 640 and d < 480:
            f = 10*round(0.1*depth[int(d - 1), int(c - 1)])
        else:
            f = 0
            print("wtf")

        p0_depth = np.append(p0_depth, (a, b, e))

        dim1 = (int(a) - int(c))
        dim2 = (int(b) - int(d))
        dim3 = (int(e) - int(f))
        mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
        frame = cv2.circle(old_image, (int(a), int(b)), 5, color[i].tolist(), -1)

        # write some depths at each point we're tracking
        font = cv2.FONT_HERSHEY_SIMPLEX
        coordText = (int(c), int(d))
        fontScale = 0.5
        fontColor = (255,255,255)
        thickness = 1
        lineType = 2

        cv2.putText(frame, str(e),
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
    # Now update the previous frame and previous points
    p0 = good_new.reshape(-1, 1, 2)

    return p0, dim1, dim2, dim3, p0_depth

# start streaming
if not args.playback_images:
    pipeline = rs.pipeline()
    config = rs.config()

    #config.enable_stream(rs.stream.depth, 256, 144, rs.format.z16, 300)

    # working:
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # not working
    #config.enable_stream(rs.stream.depth, 0, 848, 100, rs.format.z16, 300)
    config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)

    pipeline_profile = pipeline.start(config)
    device = pipeline_profile.get_device()

    depth_sensor = device.query_sensors()[0]
    depth_sensor.set_option(rs.option.emitter_on_off, 1)
    #depth_sensor.set_option(rs.option.emitter_enabled, 0)

last_image = np.array([])
ir_np = np.array([])
scaled_depth = np.array([])

start_time = time.time()
x = 1 # displays the frame rate every 1 second
counter = 0
fps_counter = 0
p0 = []

# plotting
# fig = plt.figure(figsize=(4,4))
# ax = fig.add_subplot(111, projection='3d')

# set up image reading from folder
if args.playback_images:
    print("image playback selected, creating image lists...")
    ir_image_list = []
    depth_image_list = []
    for filename in sorted(glob.glob('dataset/realsense/color/*.jpg')):
        print("appending image to list: ", filename)
        with Image.open(filename) as im:
            im = np.asanyarray(im)
            ir_image_list.append(im)
            print(type(im))
    for filename in sorted(glob.glob('dataset/realsense/depth/*.png')):
        with Image.open(filename) as im:
            im = np.asanyarray(im)
            depth_image_list.append(im)

try:
    while True:
        if not args.playback_images:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            ir_frame = frames.get_infrared_frame(1)

            frame_number = frames.get_frame_number()
            print("frame: ", frame_number)

            emitter = rs.depth_frame.get_frame_metadata(depth_frame, rs.frame_metadata_value.frame_laser_power_mode)

            if emitter:
                depth = frames.get_depth_frame()
                if not depth:
                    continue

                depth_image = np.asanyarray(depth.get_data())
                scaled_depth = cv2.convertScaleAbs(depth_image, alpha=0.08)

                depth_colormap = cv2.applyColorMap(scaled_depth, cv2.COLORMAP_JET)
                cv2.imshow('RealSense', depth_colormap)

            else:
                ir1_frame = frames.get_infrared_frame(1) # Left IR Camera, it allows 1, 2 or no input
                ir_np = np.asanyarray(ir1_frame.get_data())
        else:
            try:
                ir_np = ir_image_list[counter]
                ir_np = np.asanyarray(ir_np)
                print("showing image #: ", counter)
                scaled_depth = depth_image_list[counter]
                scaled_depth = np.asanyarray(scaled_depth)
            except IndexError as err:
                # loop through images when we get to the end
                counter = 0
                continue

        if np.any(last_image) and np.any(scaled_depth):
            #res_lsq = least_squares(fun, [0,0], args=(t_train, y_train))
            #res_lsq = optimize.least_squares(some_function, [0,0], args=(last_image, scaled_depth))
            #print(res_lsq.x)
            last_image = np.asanyarray(last_image)
            scaled_depth = np.asanyarray(scaled_depth)
            p0, dim1, dim2, dim3, p0_depth = optical_flow(ir_np, last_image, scaled_depth, p0)
            print("opt_flow: ", dim1, dim2, dim3)

            # plotting
            #for i in range(len(p0_depth)):
                #print(p0_depth[i]) 
                #print(p0_depth[i+1])
                #print(p0_depth[i+2])
                #ax.scatter(p0_depth[i], p0_depth[i], p0_depth[i])
                #plt.show()

        last_image = ir_np

        #depth_colormap = cv2.applyColorMap(scaled_depth, cv2.COLORMAP_JET)
        #cv2.imshow('RealSense', depth_colormap)

        counter+=1

        fps_counter+=1
        if (time.time() - start_time) > x :
            print("FPS: ", fps_counter / (time.time() - start_time))
            fps_counter = 0
            start_time = time.time()

        key = cv2.waitKey(1)

        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break


finally:
    if not args.playback_images:
        pipeline.stop()
