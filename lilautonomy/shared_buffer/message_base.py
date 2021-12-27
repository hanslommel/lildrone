from yamspy import MSPy

class MessageBase:
    """MessageBase class.

    All message types will be derived from this.
    """
    _tov = None

    def __init__(self, tov):
        print('Init MessageBase')
        self._tov = tov

    def imuMessage():
        print("Getting IMU message...")
        with MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200) as board:
        # 1. Message is sent: MSP_ALTITUDE without any payload (data=[])
            if board.send_RAW_msg(MSPy.MSPCodes['MSP_ALTITUDE'], data=[]):
                # 2. Response msg from the flight controller is received
                dataHandler = board.receive_msg()
                # 3. The msg is parsed
                board.process_recv_data(dataHandler)
                # 4. After the parser, the instance is populated.
                # In this example, SENSOR_DATA has its imu value updated.
                print(board.SENSOR_DATA['altitude'])

# For some msgs there are available specialized methods to read them faster:
# fast_read_altitude
# fast_read_imu
# fast_read_attitude
# fast_read_analog
# fast_msp_rc_cmd
#
# Notice they all start with "fast_" ;)
