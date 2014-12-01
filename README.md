# MAST Lab Tests

Scripts used on the Micro Aerial Systems Technologies Laboratory for running different tests.

This is a text based / console, no GUI, it works for saving data from the multicopter and/or sending commands from a computer via s serial modem, as well as performing several other tasks.

## Current scripts:

* simple.py -> Script to launch read and save data with one or two boards.
* 2boards.py -> Threaded Script to launch read and save data from two MultiWii boards and UDP. We use this one to read RC channels from the flying FC and ask raw imu data to the piggyback board with a defined 20hz for the MPU6050, in order to eliminate the accelerometer readings and be able to do systems indetification, we requiere two boards just because flying at 20hz update rate for the MPU6050 is highly unstable.

## Why?

Here in the MAST Lab (Micro Aerial Systems Technologies Laboratory) of the University of Glasgow we are a group of researchers doing precise GNC algorithms to control a single or a fleet of small multicopters and other UAV's.

We have a position controller working with the multiwii board being flow by Simulink using data from the motion capture system (Optitrack) and just sending rc channels via a serial wireless radio (roll, pitch, yaw, throttle), you can see a video about that here [TEGO indoor position control](https://vimeo.com/105761692)

More info on the old arquitecture [here.](http://aldux.net/rd/tego-indoor-position-control "More info")

Next step is putting a more powerful computer onboard, we decided to use a Raspberry Pie, this computer ask data to the multwii boards and also to the motion capture system, and saves it.

The diagram is as follows:

![Connection diagram](http://aldux.net/images/diagram.png "Connection diagram")

## Caution

This code is still under heavy development, everyday I add and remove stuff. Proceed with caution.

## Social networks:

You can follow us in this URL's:

* [Aldux.net](http://aldux.net/)
* [Aldux.net Facebook](https://www.facebook.com/AlduxNet)
* [MAST Lab Facebook](https://www.facebook.com/MASTLab)