import time
from collections import deque
from itertools import cycle

from yamspy import MSPy


# Max periods for:
CTRL_LOOP_TIME = 1/100
SLOW_MSGS_LOOP_TIME = 1/5 # these messages take a lot of time slowing down the loop...

NO_OF_CYCLES_AVERAGE_GUI_TIME = 10

# serial port for flight controller
SERIAL_PORT = "/dev/serial0"

CMDS = {
        'roll':     1500,
        'pitch':    1500,
        'throttle': 900,
        'yaw':      1500,
        'aux1':     1000,
        'aux2':     1000
        }

# this order depends on how the flight controller is configured, this order is for AETR
CMDS_ORDER = ['roll', 'pitch', 'throttle', 'yaw', 'aux1', 'aux2']

# It's necessary to send some messages or the RX failsafe will be activated
# and it will not be possible to arm.
command_list = ['MSP_API_VERSION', 'MSP_FC_VARIANT', 'MSP_FC_VERSION', 'MSP_BUILD_INFO', 
                'MSP_BOARD_INFO', 'MSP_UID', 'MSP_ACC_TRIM', 'MSP_NAME', 'MSP_STATUS', 'MSP_STATUS_EX',
                'MSP_BATTERY_CONFIG', 'MSP_BATTERY_STATE', 'MSP_BOXNAMES']

def takeoff_sequence():
    takeoff = True
    try:
        print("Connecting to the FC...")

        with MSPy(device=SERIAL_PORT, loglevel='WARNING', baudrate=115200) as board:
            if board == 1: # an error occurred...
                print("Returned 1, unable to connect to FC.")
                return
            
            else:
                for msg in command_list: 
                    if board.send_RAW_msg(MSPy.MSPCodes[msg], data=[]):
                        dataHandler = board.receive_msg()
                        board.process_recv_data(dataHandler)

            print('Sending Disarm command...')
            CMDS['aux1'] = 1000
            board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])
            time.sleep(1)

            # set throttle before arming:
            CMDS['throttle'] = 988
        
            # use aux 2 to set autolevel on flight controller
            CMDS['aux2'] = 1300
            # arming
            print('Sending Arm command, waiting 4 seconds')
            CMDS['aux1'] = 1800
            board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])
            time.sleep(4)

            # TODO find good values for throttle on takeoff
            # ramp up throttle for takeoff
            ascent_throttle = 1600
            for i in range(988, ascent_throttle, 5):
                CMDS['throttle'] = i
                print('throttle up:{}'.format(CMDS['throttle']))
                board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])
                time.sleep(0.01)

            # follow altimeter reading to hover height
            hover_throttle = 1500

            while takeoff == True:
                if altimeter <= 1.5:
                    CMDS['throttle'] = ascent_throttle
                else:
                    for i in range(ascent_throttle, hover_throttle, -1):
                        CMDS['throttle'] = i
                        print('throttle up:{}'.format(CMDS['throttle']))
                        board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER])
                        time.sleep(0.001)
                        takeoff = False

            # # Send the RC channel values to the FC
            # if board.send_RAW_RC([CMDS[ki] for ki in CMDS_ORDER]):
            #     dataHandler = board.receive_msg()
            #     board.process_recv_data(dataHandler)

if __name__ == "__main__":
    takeoff_sequence()