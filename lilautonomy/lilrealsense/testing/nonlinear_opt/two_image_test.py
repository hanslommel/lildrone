import numpy as np
import cv2
from scipy import optimize
import pyrealsense2.pyrealsense2 as rs
import scipy.interpolate


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

# pseudo
# def fun(x,img1,img2)
#   E = 0;
#   N = 0;
#   for each pixel in img1:
#     depth2_est = im1(pixel)
#     depth2 = img2(pixel+x)
#     E = E+(depth2_est-depth2)^2
#     N = N+1
#   return E/N # average squared error


pipeline = rs.pipeline()

config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#config.enable_stream(rs.stream.depth, 0, 848, 100, rs.format.z16, 300)
#config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)

pipeline_profile = pipeline.start(config)
device = pipeline_profile.get_device()

depth_sensor = device.query_sensors()[0]
depth_sensor.set_option(rs.option.emitter_on_off, 0)

last_image = np.array([])

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        frame_number = frames.get_frame_number()
        print("frame: ", frame_number)

        depth = frames.get_depth_frame()
        if not depth:
            continue

        depth_image = np.asanyarray(depth.get_data())
        scaled_depth = cv2.convertScaleAbs(depth_image, alpha=0.08)

        scaled_depth = cv2.resize(scaled_depth, dsize=(6, 5), interpolation=cv2.INTER_CUBIC)

        if np.any(last_image):
            #res_lsq = least_squares(fun, [0,0], args=(t_train, y_train))
            print("solving!")
            res_lsq = optimize.least_squares(some_function, [0,0], args=(last_image, scaled_depth))
            print(res_lsq.x)
        last_image = scaled_depth

        depth_colormap = cv2.applyColorMap(scaled_depth, cv2.COLORMAP_JET)
        cv2.imshow('RealSense', depth_colormap)


        key = cv2.waitKey(1)

        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break


finally:
    pipeline.stop()
