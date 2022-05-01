
import numpy as np

# possible forms for control interface:
# 1- takes motor commands
#    - could be RPM, could be current (amps)
# 2- takes attitude commands
#    - could do first order response, could implement a control loop here

# TODO
# class QuadrotorParams:
#     """ Store, load, save quadrotor parameters for the Quadrotor class
#     """
#     mass = [] # [float] quad

class Quadrotor:
    """ Class to simulate quadrotor dynamics and sensors

    Maintains its own internal, simulated time.  Interface consists of parameterization/
    initial values, control inputs, a propagator and getters for sensors.

    Axis convention is aerospace convention: [x,y,z] = [forward, right, down]

    Contains: 
    - motor models
    - sensor models
    """

    _mass = [] # [float, kg] mass
    _inertia = [] # [float 3x3, kg*m^2] moment of inertia

    def __init__(self):
        # model mass and inertia from collection of point masses
        pointmasses = [
            [0.05, 0.05, 0.0, 0.05],
            [-0.05, 0.05, 0.0, 0.05],
            [-0.05, -0.05, 0.0, 0.05],
            [0.05, -0.05, 0.0, 0.05],
            [0.0, 0.0, 0.02, 0.15],
            [0.0, 0.0, -0.02, 0.15],
        ]
        self._mass, self._inertia = inertia_from_pointmasses(pointmasses)
        self._x = np.array([2.0, 0.0, 0.0]) # position in local NED frame
        self._v = np.array([0.0, 0.0, 0.0]) # velocity in local NED frame
        self._R = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

        # print(np.matmul(self._R,self._x))

    def propagate(dt):
        pass
        # F = m*(acc + wxv)

        # M = I*alpha + wxIw


# TODO
# flight controller model
# motor models
# sensor models

# TODO
# class MotorParams:
#     """ Helper Store, load, save quadrotor parameters for the Quadrotor class
#     """

# class ElectricMotor:
#     """ Model electric motor - component in Quadrotor model class
#     """

def inertia_from_pointmasses(masses):
    mass = 0.0
    Ixx = 0.0
    Ixy = 0.0
    Ixz = 0.0
    Iyy = 0.0
    Iyz = 0.0
    Izz = 0.0

    for point in masses:
        Ixx = Ixx + (point[1]**2 + point[2]**2)*point[3]
        Ixy = Ixy - (point[0]*point[1])*point[3]
        Ixz = Ixz - (point[0]*point[2])*point[3]
        Iyy = Iyy + (point[0]**2 + point[2]**2)*point[3]
        Iyz = Iyz - (point[1]*point[2])*point[3]
        Izz = Izz + (point[0]**2 + point[1]**2)*point[3]
        mass = mass + point[3]

    return mass, np.matrix([[Ixx, -Ixy, -Ixz],[-Ixy, Iyy, -Iyz],[-Ixz, -Iyz, Izz]])