from shared_buffer import PublisherBase, MessageBase

class IMUMessage(MessageBase):
    """IMU Message class.

    """

    def __init__(self, acceleration, rate):
        print('IMU Message')
        self._acceleration = acceleration
        self._rate = rate

class IMUPublisher(PublisherBase):
    """IMU Publisher class.

    """
    _imu_buffer_length = 100

    def __init__(self):
        print('IMU Publisher')
        super(IMUPublisher, self).__init__(self._imu_buffer_length)