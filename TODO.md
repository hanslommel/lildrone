#TODOList for lildrone project
08/01/2021
- what can we do?
  - calibrated and streamed data from the arducam on Pi (Justin)
  - we've seen orientation and calibrated IMU in betaflight

- Next:
  - (Justin) check out range data on betaflight (UART)
  - (Justin) flight time RX input switching (RC Override)
  - (Pete) get all the data on Pi
    - MultiWii (MSP)
  - (Pete) log all the data on Pi
  - (Pete) solder usb-c to flight controller - see links for the diagram (draw.io diagram)
  - (Pete) mount and solder the optical flow sensor
    5V and GND, TX2 and RX2
  - (Pete) Solder TX5 and RX5 to GPIO pin connectors for Pi (may have to order the pin connectors)
  - (Pete) Try to image the mamba with iNav - get inav configurator (see links doc) dev version
    - Justin's instructions are at the bottom of links

- Done: 
  - (Justin) check out optical flow data on betaflight (UART)
  - (Justin) RC flight

##Software
- Justin and Pete- Install OS on Pi - RASPBIAN  -DONE-
  - Justin: need to image pi with GUI-less raspbian
- Get data on Pi
  - cameras
    - arducam shield
      - Justin DONE, Pete TODO
    - Justin - connect custom stereo rig
      - DONE, Pete TODO
  - fork repo for cameras https://github.com/ArduCAM/MIPI_Camera.gi
    - actually, let's just submodule it as-is until we have motivation to make changes and fork
  - lidars
    - DONE
    - Justin - try to plumb through F/C
      - down lidar connected to FC UART, not tested
      - get forward lidar connected
        - try to see data on betaflight?
  - FC
    - is USB from FC to pi just UART connection? use gpio pins?
     - just UART
    - what signal do we want to send? pwm like receiver? setpoint?
    - MultiWii:
      - how do you do the MSP
      - how to send msp signal from pi
        - MultiWii python module! install with: pip3 install MultiWii
      - connect mamba to pi over uart
      - make python script on pi that uses multiwii MSP, open serial port with it
      - configure betaflight to listen to serial UART
       - then MultiWii just works? maybe something is sent over MSP that enables it

  - IMU
    - Pete- after betaflight
    - alternatively, just do all SE on F/C?
     - what options for autopilot on FC?
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
- Justin- Power the Pi -- DONE
  - pads from ESC board
  - print pete a real camera holder!
   - make edits to finalize
   - make top piece out of pi holder to attach to camera holder
- Pete- put together frame, pi, f/c, escs, motors, battery
  - power on DONE
  - order Matek optical flow DONE
  - order luna lidar DONE

##Other
- Pete- Order another Pi - 4B 4GB
