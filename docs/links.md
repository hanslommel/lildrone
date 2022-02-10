MultiWii Python package: https://pypi.org/project/MultiWii/
nope use YAMSPy!

Wifi MSP control (long raaaange): https://www.instructables.com/Long-Range-Wifi-PPM-MSP/

optical flow / lidar
https://github.com/iNavFlight/inav/wiki/MSP-V2

lildrone system flowchart:
https://drive.google.com/file/d/1l15bH1IFUwRLjBwumo6ilKirpo2iZqis/view?usp=sharing

lildrone autonomy class diagram:
https://drive.google.com/file/d/1NzRtgO5ifQYxKSk8Fef-b3WayeufrIQC/view?usp=sharing

lildrone autonomy structure diagram:
https://drive.google.com/file/d/10NsvcqlPxexcTTl86E4TRIu232x3eRFq/view?usp=sharing

MultiWii getting IMU data:
https://docs.quanser.com/quarc/documentation/multiwii_imu_block.html

Enabling lidar maybe?
https://github.com/betaflight/betaflight/issues/5245

using Matek optical flow with this library maybe?
https://github.com/pimoroni/pmw3901-python

build custom firmware to enable MSP override with RC: https://github.com/iNavFlight/inav/issues/4084
also have to change  _Static_assert(ARRAYLEN(menuOsdElemsEntries) - 2 + 1 == OSD_ITEM_COUNT, "missing OSD elements in CMS");
to something like  _Static_assert(ARRAYLEN(menuOsdElemsEntries) - 2 + 1 < OSD_ITEM_COUNT, "missing OSD elements in CMS");
to build firmware from the inav folder:
./build.sh MAMBAF405US_I2C

Custom firmware will be tagged as 5.0.0 so we'll need the dev configurator:
http://seyrsnys.myzen.co.uk/inav-configurator-next/
