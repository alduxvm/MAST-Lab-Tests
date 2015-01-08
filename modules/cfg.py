#!/usr/bin/env python

"""cfg.py: Configuration file and extra functions."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2014 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import serial, time, datetime, socket, struct, fcntl
#import optiUDP


"""General settings"""
DRONE   =   1   # Connect to MultiWii and save data
DRONE2  =   0   # Connect to MultiWii and save data
PRINT   =   1   # Print data to terminal, useful for debugging
FILE    =   0   # Save to a timestamped file, the data selected below
ATT     =   0   # Ask and save the attitude of the multicopter
ALT     =   0   # Ask and save the altitude of the multicopter
RC      =   0   # Ask and save the pilot commands of the multicopter
MOT     =   0   # Ask and save the PWM of the motors that the MW is writing to the multicopter
RAW     =   0   # Ask and save the raw imu data of the multicopter
MOTOR   =   1   # Ask and save the motors pwm of the multicopter
RCRAW   =   0   # Ask and save the rc & raw imu data of the multicopter
CMD     =   0   # Send commands to the MW to control it
UDP     =   0   # Save or use UDP data (to be adjusted)
SUDP    =   0   # Send UDP data
TWIS    =   0   # Use twisted 
visual3d    =   0   # 3D visualization


"""UDP ips and ports"""
#UDPip = "localhost"
#UDPip = "130.209.140.214" #MAST Lab IP eduram
UDPip = "172.30.17.51" #MAST Lab IP flexaccess
UDPport = 51001
UDPportOut = 51002
line = ""
rate = 0.02

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def manage2streams(data1,data2):
    global line
    if SUDP:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = get_ip_address('wlan0')
        ipnum = float(ip.translate(None, '.'))
    if FILE:
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%m_%d_%H-%M-%S')+".csv"
        file = open("data/"+st, "w")
    while True:
        if ATT:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['angx']) + " " + str(data1['angy']) + " " + str(data1['heading']) + " " 
            line += str(data2['angx']) + " " + str(data2['angy']) + " " + str(data2['heading']) + " " 
        if RC:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['roll']) + " " + str(data1['pitch']) + " " + str(data1['yaw']) + " " + str(data1['throttle']) + " " 
            #line += str(data2['roll']) + " " + str(data2['pitch']) + " " + str(data2['yaw']) + " " + str(data2['throttle']) + " " 
        if RAW:
            #line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['ax']) + " " + str(data1['ay']) + " " + str(data1['az']) + " " + str(data1['gx']) + " " + str(data1['gy']) + " " + str(data1['gz']) + " "
            line += str(data2['ax']) + " " + str(data2['ay']) + " " + str(data2['az']) + " " + str(data2['gx']) + " " + str(data2['gy']) + " " + str(data2['gz']) + " "
        if UDP:
            line += " ".join(map(str,optiUDP.UDPmess))
        if FILE:
            file.write(line+"\n")
        if PRINT:
            print line
        if SUDP:
            if ATT:
                values = (ipnum, float(data1['timestamp']), float(data1['elapsed']), data1['angx'], data1['angy'], data1['heading'])
                values += (data2['angx'], data2['angy'], data2['heading'])
            if RC:
                values = (ipnum, float(data1['timestamp']), float(data1['elapsed']), data1['roll'], data1['pitch'], data1['yaw'], data1['throttle'])
                #values += (data2['roll'], data2['pitch'], data2['yaw'], data2['throttle'])
            if RAW:
                #values = (ipnum, float(data1['timestamp']), float(data1['elapsed']), data1['ax'], data1['ay'], data1['az'], data1['gx'], data1['gy'], data1['gz'])
                values += (data2['ax'], data2['ay'], data2['az'], data2['gx'], data2['gy'], data2['gz'])
            values = values + optiUDP.UDPmess
            s = struct.Struct('>'+'d'*len(values))
            packet = s.pack(*values)
            sock.sendto(packet, (UDPip, UDPportOut))
        line = ""
        time.sleep(rate)


def manageData(data1):
    global line
    if SUDP:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = get_ip_address('wlan0')
        ipnum = float(ip.translate(None, '.'))
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
        if MOTOR:
            line += str(data1['timestamp']) + " " + str(data1['elapsed']) + " " + str(data1['m1']) + " " + str(data1['m2']) + " " + str(data1['m3']) + " " + str(data1['m4']) + " "
        if UDP:
            line += " ".join(map(str,optiUDP.UDPmess))
        flag = 0
        if optiUDP.UDPmess == "":
            flag = 0
        else:
            flag = 1
        if FILE and flag:
            file.write(line+"\n")
        if PRINT:
            print data1
            print line
        if SUDP:
            if ATT:
                values = (ipnum, float(data1['timestamp']), float(data1['elapsed']), data1['angx'], data1['angy'], data1['heading'])
            if RC:
                values = (ipnum, float(data1['timestamp']), float(data1['elapsed']), data1['roll'], data1['pitch'], data1['yaw'], data1['throttle'])
            if RAW:
                values = (ipnum, float(data1['timestamp']), float(data1['elapsed']), data1['ax'], data1['ay'], data1['az'], data1['gx'], data1['gy'], data1['gz'])
            if MOTOR:
                values = (ipnum, float(data1['timestamp']), float(data1['elapsed']), data1['m1'], data1['m2'], data1['m3'], data1['m4'])
            s = struct.Struct('>'+'d'*len(values))
            packet = s.pack(*values)
            sock.sendto(packet, (UDPip, UDPportOut))
        line = ""
        time.sleep(rate)


