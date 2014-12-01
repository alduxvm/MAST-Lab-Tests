#!/usr/bin/env python

"""cfg.py: Configuration file and extra functions."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2014 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import serial, time, datetime
import optiUDP


"""General settings"""
DRONE   =   1   # Connect to MultiWii and save data
DRONE2  =   2   # Connect to MultiWii and save data
PRINT   =   1   # Print data to terminal, useful for debugging
FILE    =   0   # Save to a timestamped file, the data selected below
ATT     =   1   # Ask and save the attitude of the multicopter
ALT     =   0   # Ask and save the altitude of the multicopter
RC      =   0   # Ask and save the pilot commands of the multicopter
MOT     =   0   # Ask and save the PWM of the motors that the MW is writing to the multicopter
RAW     =   0   # Ask and save the raw imu data of the multicopter
RCRAW   =   0   # Ask and save the rc & raw imu data of the multicopter
CMD     =   0   # Send commands to the MW to control it
UDP     =   0   # Save or use UDP data (to be adjusted)
TWIS    =   0   # Use twisted 


"""UDP ips and ports"""
UDPip = "localhost"
UDPport = 51001


def manage2streams(data1,data2):
    line=""
    if FILE:
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m_%d_%H-%M-%S')+".csv"
        file = open("data/"+st, "w")
    while True:
        if ATT:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['angx']) + " " + str(data1['angy']) + " " + str(data1['heading']) + " " 
            line += str(data2['angx']) + " " + str(data2['angy']) + " " + str(data2['heading']) + " " 
        if RC:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['roll']) + " " + str(data1['pitch']) + " " + str(data1['yaw']) + " " + str(data1['throttle']) + " " 
            line += str(data2['roll']) + " " + str(data2['pitch']) + " " + str(data2['yaw']) + " " + str(data2['throttle']) + " " 
        if RAW:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['ax']) + " " + str(data1['ay']) + " " + str(data1['az']) + " " + str(data1['gx']) + " " + str(data1['gy']) + " " + str(data1['gz']) + " "
            line += str(data2['ax']) + " " + str(data2['ay']) + " " + str(data2['az']) + " " + str(data2['gx']) + " " + str(data2['gy']) + " " + str(data2['gz']) + " "
        if UDP:
            line += " ".join(map(str,optiUDP.UDPmess))
        if FILE:
            file.write(line+"\n")
        if PRINT:
            print line
        line = ""
        time.sleep(0.02)


def manageData(data1):
    line=""
    if FILE:
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m_%d_%H-%M-%S')+".csv"
        file = open("data/"+st, "w")
    while True:
        if ATT:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['angx']) + " " + str(data1['angy']) + " " + str(data1['heading']) + " " 
        if RC:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['roll']) + " " + str(data1['pitch']) + " " + str(data1['yaw']) + " " + str(data1['throttle']) + " "  
        if RAW:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['ax']) + " " + str(data1['ay']) + " " + str(data1['az']) + " " + str(data1['gx']) + " " + str(data1['gy']) + " " + str(data1['gz']) + " "
        if UDP:
            line += " ".join(map(str,optiUDP.UDPmess))
        if FILE:
            file.write(line+"\n")
        if PRINT:
            print line
        line = ""


