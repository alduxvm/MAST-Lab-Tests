#!/usr/bin/env python

"""cfg.py: Configuration file."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2014 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import serial, time, datetime

import MSP, MSP2, optiUDP

#import numpy as np
#from matplotlib import pyplot as plt

"""General settings"""
DRONE   =   1   # Connect to MultiWii and save data
DRONE2  =   1   # Connect to MultiWii and save data
PRINT   =   1   # Print data to terminal, useful for debugging
FILE    =   0   # Save to a timestamped file, the data selected below
PLOT    =   0   # Plot one axis
TIME    =   0   # Save the difference of time between all the main functions for perfomance logging
FLYT    =   0   # Save the flight time in seconds
ATT     =   1   # Ask and save the attitude of the multicopter
ALT     =   0   # Ask and save the altitude of the multicopter
RC      =   0   # Ask and save the pilot commands of the multicopter
MOT     =   0   # Ask and save the PWM of the motors that the MW is writing to the multicopter
RAW     =   0   # Ask and save the raw imu data of the multicopter
RCRAW   =   0   # Ask and save the rc & raw imu data of the multicopter
CMD     =   0   # Send commands to the MW to control it
UDP     =   0   # Save or use UDP data (to be adjusted)
ASY     =   0   # Use async communicacion
SCKSRV  =   0   # Use socketserver communication
TWIS    =   0   # Use twisted 


"""Serial Port Configuration for easy access"""
#port = "/dev/tty.usbserial-AM016WP4" # This is the port that the MultiWii is attached to (for mac & MW home)
#port = "/dev/tty.usbserial-A101CCVF"  # This is the port that the MultiWii is attached to (for mac & MW office)
#port = "/dev/ttyUSB0"    # This is the port that the MultiWii is attached to (for raspberry pie)

"""UDP ips and ports"""
#Raspberry pie IP address
#UDPip = "172.30.150.170"
#Mac IP address
#UDPip = "130.209.27.59"
UDPip = "localhost"
UDPport = 51001

def manageData():
    line=""
    if FILE:
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m_%d_%H-%M-%S')+".csv"
        file = open("data/"+st, "w")
    while True:
        if ATT:
            line += str(MSP.attitude['timestamp']) + " " + str(MSP.attitude['elapsed']) + " " + str(MSP.attitude['angx']) + " " + str(MSP.attitude['angy']) + " " + str(MSP.attitude['heading']) + " " 
        if RC:
            line += str(MSP.attitude['timestamp']) + " " + str(MSP.attitude['elapsed']) + " " + str(MSP.rcChannels['roll']) + " " + str(MSP.rcChannels['pitch']) + " " + str(MSP.rcChannels['yaw']) + " " + str(MSP.rcChannels['throttle']) + " " 
        if RAW:
            line += str(MSP.attitude['timestamp']) + " " + str(MSP.attitude['elapsed']) + " " + str(MSP.rawIMU['ax']) + " " + str(MSP.rawIMU['ay']) + " " + str(MSP.rawIMU['az']) + " " + str(MSP.rawIMU['gx']) + " " + str(MSP.rawIMU['gy']) + " " + str(MSP.rawIMU['gz']) + " "
        if UDP:
            line += " ".join(map(str,optiUDP.UDPmess))
        if FILE:
            file.write(line+"\n")
        if PRINT:
            print line
        line = ""


def manageData2():
    line=""
    if FILE:
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m_%d_%H-%M-%S')+".csv"
        file = open("data/"+st, "w")
    while True:
        if ATT:
            line += str(MSP.attitude['timestamp']) + " " + str(MSP.attitude['elapsed']) + " " + str(MSP.attitude['angx']) + " " + str(MSP.attitude['angy']) + " " + str(MSP.attitude['heading']) + " " 
            line += str(MSP2.attitude['angx']) + " " + str(MSP2.attitude['angy']) + " " + str(MSP2.attitude['heading']) + " " 
        if RC:
            line += str(MSP.attitude['timestamp']) + " " + str(MSP.attitude['elapsed']) + " " + str(MSP.rcChannels['roll']) + " " + str(MSP.rcChannels['pitch']) + " " + str(MSP.rcChannels['yaw']) + " " + str(MSP.rcChannels['throttle']) + " " 
            line += str(MSP2.rcChannels['roll']) + " " + str(MSP2.rcChannels['pitch']) + " " + str(MSP2.rcChannels['yaw']) + " " + str(MSP2.rcChannels['throttle']) + " " 
        if RAW:
            line += str(MSP.attitude['timestamp']) + " " + str(MSP.attitude['elapsed']) + " " + str(MSP.rawIMU['ax']) + " " + str(MSP.rawIMU['ay']) + " " + str(MSP.rawIMU['az']) + " " + str(MSP.rawIMU['gx']) + " " + str(MSP.rawIMU['gy']) + " " + str(MSP.rawIMU['gz']) + " "
            line += str(MSP2.rawIMU['ax']) + " " + str(MSP2.rawIMU['ay']) + " " + str(MSP2.rawIMU['az']) + " " + str(MSP2.rawIMU['gx']) + " " + str(MSP2.rawIMU['gy']) + " " + str(MSP2.rawIMU['gz']) + " "
        if UDP:
            line += " ".join(map(str,optiUDP.UDPmess))
        if FILE:
            file.write(line+"\n")
        if PRINT:
            print line
        line = ""
        time.sleep(0.02)



#plt.ion() # enable interactivity
#ydata = [0]*50
#ax1=plt.axes() 
#line, = plt.plot(ydata)
#plt.ylim([-100,100])

def plotData():
    ymin = float(min(ydata))-10
    ymax = float(max(ydata))+10
    plt.ylim([ymin,ymax])
    ydata.append(MSP.attitude['angx'])
    del ydata[0]
    line.set_xdata(np.arange(len(ydata)))
    line.set_ydata(ydata)  # update the data
    plt.draw() # update the plot

