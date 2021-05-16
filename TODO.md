#TODO List for lildrone project

##Software
- Justin and Pete- Install OS on Pi - RASPBIAN
  - Justin DONE
- Get data on Pi
  - cameras
    - arducam shield
      - DONE
    - Justin - connect custom stereo rig
      - DONE
  - lidars
    - DONE
    - Justin - try to plumb through F/C
      - down lidar connected to FC UART, not tested
  - FC
    - is USB from FC to pi just UART connection? use gpio pins?
  - IMU
    - Pete- after betaflight
    - alternatively, just do all SE on F/C?
- SW architecture on Pi
  - Pete- get a starting point, build something with CMake
  - Pete- how should we record all of the separate data streams
    - rosbag? LCM? custom?
  - Pete- how do want to diagram?  draw.io?
- install ardupilot on Mamba - Pete and Justin
  - https://ardupilot.org/copter/docs/common-loading-firmware-onto-chibios-only-boards.html
  - NOPE use betaflight! it supports MultiWii
- Get data on Mamba from Pi
  - Pete- make a plan
  - MultiWii
- Pete- Fork betaflight
- Simulation
  - ROS?
  - simple one-off?

##Questions
- should we switch to Mamba F7, or H3/4, which are more powerfull F/C boards?
  - to run more SE and local planning on board?

##Hardware
- Justin- Power the Pi
  - pads from ESC board
- Pete- put together frame, pi, f/c, escs, motors, battery
  - power on

##Other
- Pete- Order another Pi - 4B 4GB
