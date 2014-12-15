#!/usr/bin/env python

"""1boards.py: Threaded Script to launch read and save data from one MultiWii board and UDP."""
"""University of Glasgow's Micro Air Systems Technologies Laboratory."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2014 Aldux.net & MAST Lab"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import serial, struct, time, threading
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from modules import cfg, optiUDP
from modules.multiwii import MultiWii


from visual import *
import string, math

def start3d():

    grad2rad = 3.141592/180.0

    # Main scene
    scene=display(title="9DOF Razor IMU test")
    scene.range=(1.2,1.2,1.2)
    #scene.forward = (0,-1,-0.25)
    scene.forward = (1,0,-0.25)
    scene.up=(0,0,1)

    # Second scene (Roll, Pitch, Yaw)
    scene2 = display(title='9DOF Razor IMU test',x=0, y=0, width=500, height=200,center=(0,0,0), background=(0,0,0))
    scene2.range=(1,1,1)
    scene.width=500
    scene.y=200

    scene2.select()
    #Roll, Pitch, Yaw
    cil_roll = cylinder(pos=(-0.4,0,0),axis=(0.2,0,0),radius=0.01,color=color.red)
    cil_roll2 = cylinder(pos=(-0.4,0,0),axis=(-0.2,0,0),radius=0.01,color=color.red)
    cil_pitch = cylinder(pos=(0.1,0,0),axis=(0.2,0,0),radius=0.01,color=color.green)
    cil_pitch2 = cylinder(pos=(0.1,0,0),axis=(-0.2,0,0),radius=0.01,color=color.green)
    #cil_course = cylinder(pos=(0.6,0,0),axis=(0.2,0,0),radius=0.01,color=color.blue)
    #cil_course2 = cylinder(pos=(0.6,0,0),axis=(-0.2,0,0),radius=0.01,color=color.blue)
    arrow_course = arrow(pos=(0.6,0,0),color=color.cyan,axis=(-0.2,0,0), shaftwidth=0.02, fixedwidth=1)

    #Roll,Pitch,Yaw labels
    label(pos=(-0.4,0.3,0),text="Roll",box=0,opacity=0)
    label(pos=(0.1,0.3,0),text="Pitch",box=0,opacity=0)
    label(pos=(0.55,0.3,0),text="Yaw",box=0,opacity=0)
    label(pos=(0.6,0.22,0),text="N",box=0,opacity=0,color=color.yellow)
    label(pos=(0.6,-0.22,0),text="S",box=0,opacity=0,color=color.yellow)
    label(pos=(0.38,0,0),text="W",box=0,opacity=0,color=color.yellow)
    label(pos=(0.82,0,0),text="E",box=0,opacity=0,color=color.yellow)
    label(pos=(0.75,0.15,0),height=7,text="NE",box=0,color=color.yellow)
    label(pos=(0.45,0.15,0),height=7,text="NW",box=0,color=color.yellow)
    label(pos=(0.75,-0.15,0),height=7,text="SE",box=0,color=color.yellow)
    label(pos=(0.45,-0.15,0),height=7,text="SW",box=0,color=color.yellow)

    L1 = label(pos=(-0.4,0.22,0),text="-",box=0,opacity=0)
    L2 = label(pos=(0.1,0.22,0),text="-",box=0,opacity=0)
    L3 = label(pos=(0.7,0.3,0),text="-",box=0,opacity=0)

    # Main scene objects
    scene.select()
    # Reference axis (x,y,z)
    arrow(color=color.green,axis=(1,0,0), shaftwidth=0.02, fixedwidth=1)
    arrow(color=color.green,axis=(0,-1,0), shaftwidth=0.02 , fixedwidth=1)
    arrow(color=color.green,axis=(0,0,-1), shaftwidth=0.02, fixedwidth=1)
    # labels
    label(pos=(0,0,0.8),text="9DOF Razor IMU test",box=0,opacity=0)
    label(pos=(1,0,0),text="X",box=0,opacity=0)
    label(pos=(0,-1,0),text="Y",box=0,opacity=0)
    label(pos=(0,0,-1),text="Z",box=0,opacity=0)
    # IMU object
    platform = box(length=1, height=0.05, width=1, color=color.red)
    p_line = box(length=1,height=0.08,width=0.1,color=color.yellow)
    plat_arrow = arrow(color=color.green,axis=(1,0,0), shaftwidth=0.06, fixedwidth=1)


    roll=0
    pitch=0
    yaw=0

    while 1:
        roll = flightController.attitude['angx']
        pitch = flightController.attitude['angy']
        yaw = flightController.attitude['heading']

        axis=(cos(pitch)*cos(yaw),-cos(pitch)*sin(yaw),sin(pitch)) 
        up=(sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw),sin(roll)*cos(yaw)-cos(roll)*sin(pitch)*sin(yaw),-cos(roll)*cos(pitch))
        platform.axis=axis
        platform.up=up
        platform.length=1.0
        platform.width=0.65
        plat_arrow.axis=axis
        plat_arrow.up=up
        plat_arrow.length=0.8
        p_line.axis=axis
        p_line.up=up
        cil_roll.axis=(0.2*cos(roll),0.2*sin(roll),0)
        cil_roll2.axis=(-0.2*cos(roll),-0.2*sin(roll),0)
        cil_pitch.axis=(0.2*cos(pitch),0.2*sin(pitch),0)
        cil_pitch2.axis=(-0.2*cos(pitch),-0.2*sin(pitch),0)
        arrow_course.axis=(0.2*sin(yaw),0.2*cos(yaw),0)
        L1.text = str(float(words[0]))
        L2.text = str(float(words[1]))
        L3.text = str(float(words[2]))        






if __name__ == "__main__":

    try:

        if cfg.DRONE:
            flightController = MultiWii("/dev/tty.usbserial-A801WZA1")
            #flightController = MultiWii("/dev/ttyUSB0")
            readThread = threading.Thread(target=flightController.getDataInf, args=(MultiWii.ATTITUDE,))
            readThread.start()

        if cfg.PRINT:
            printThread = threading.Thread(target=cfg.manageData, args=(flightController.attitude,))
            printThread.start()

        if cfg.visual3d:
            visualThread = threading.Thread(target=start3d, )
            visualThread.start()

        if cfg.TWIS:
            optiUDP.startTwisted()
        
          
    except Exception,error:
        print "Error: "+str(error)
        flightController.ser.close()
        file.close()