#!/usr/bin/env python

"""multiwii.py: Handles Multiwii Serial Protocol."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2014 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import serial, time, struct

import cfg


class MultiWii:

    """Multiwii Serial Protocol message ID"""
    IDENT = 100
    STATUS = 101
    RAW_IMU = 102
    SERVO = 103
    MOTOR = 104
    RC = 105
    RAW_GPS = 106
    COMP_GPS = 107
    ATTITUDE = 108
    ALTITUDE = 109
    ANALOG = 110
    RC_TUNING = 111
    PID = 112
    BOX = 113
    MISC = 114
    MOTOR_PINS = 115
    BOXNAMES = 116
    PIDNAMES = 117
    WP = 118
    BOXIDS = 119
    RC_RAW_IMU = 121
    SET_RAW_RC = 200
    SET_RAW_GPS = 201
    SET_PID = 202
    SET_BOX = 203
    SET_RC_TUNING = 204
    ACC_CALIBRATION = 205
    MAG_CALIBRATION = 206
    SET_MISC = 207
    RESET_CONF = 208
    SET_WP = 209
    SWITCH_RC_SERIAL = 210
    IS_SERIAL = 211
    DEBUG = 254

    """Global variables of data"""
    rcChannels = {'roll':0,'pitch':0,'yaw':0,'throttle':0,'elapsed':0,'timestamp':0}
    rawIMU = {'ax':0,'ay':0,'az':0,'gx':0,'gy':0,'gz':0,'elapsed':0,'timestamp':0}
    attitude = {'angx':0,'angy':0,'heading':0,'elapsed':0,'timestamp':0}
    temp = ();
    elapsed = 0

    """Use a pythonic way to evaluate and process command received"""
    """Assign the temp tuple to the tuple for raw imu data, no magnetometers saved"""
    def readRaw():
        try:
            rawIMU['ax']=float(temp[0])
            rawIMU['ay']=float(temp[1])
            rawIMU['az']=float(temp[2])
            rawIMU['gx']=float(temp[3])
            rawIMU['gy']=float(temp[4])
            rawIMU['gz']=float(temp[5])
            rawIMU['elapsed']=round(elapsed,3)
            rawIMU['timestamp']=time.time()
        except IndexError:
            pass

    """Assign the temp tuple to the tuple for rc data"""
    def readRC():
        try:
            for value in rcChannels:
                rcChannels[value]=temp[i]
                i+=1
            rcChannels['elapsed']=round(elapsed,3)
            rcChannels['timestamp']=time.time()
        except IndexError:
            pass

    """Assign the temp tuple to the tuple for attitude data, beware of the 10.0 for not losing the decimal part"""
    def readAttitude():
        try:
            attitude['angx']=float(temp[0]/10.0)
            attitude['angy']=float(temp[1]/10.0)
            attitude['heading']=float(temp[2])
            attitude['elapsed']=round(elapsed,3)
            attitude['timestamp']=time.time()
            print attitude
        except IndexError:
            pass

    """Assign the temp tuple to the tuple for rc and raw data, this depends on a modification on the MultiWii code, and is not fully tested yet"""
    def readRCRaw():
        try:
            rawIMU['ax']=float(temp[0])
            rawIMU['ay']=float(temp[1])
            rawIMU['az']=float(temp[2])
            rawIMU['gx']=float(temp[3])
            rawIMU['gy']=float(temp[4])
            rawIMU['gz']=float(temp[5])
        except IndexError:
            pass

    """Evaluate each command recieved, this works like a case-switch in python"""
    evaluateCommand = {
        102 : readRaw,
        105 : readRC,
        108 : readAttitude,
        121 : readRCRaw 
    }

    def __init__(self, serPort):
        self.ser = serial.Serial()
        self.ser.port = serPort
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2
        wakeup = 12

        try:
            self.ser.open()
            if cfg.PRINT:
                print "Waking up multicopter on "+self.ser.port+"..."
            for i in range(1,wakeup):
                if cfg.PRINT:
                    print wakeup-i
                    time.sleep(1)
                else:
                    time.sleep(1)
        except Exception, error:
            print "\n\nError opening "+self.ser.port+" port.\n\n"
            quit()

    def sendCMD(self, data_length, code, data):
        checksum = 0
        total_data = ['$', 'M', '<', data_length, code] + data
        for i in struct.pack('<2B%dh' % len(data), *total_data[3:len(total_data)]):
            checksum = checksum ^ ord(i)
        total_data.append(checksum)
        try:
            b = None
            b = self.ser.write(struct.pack('<3c2B%dhB' % len(data), *total_data))
        except Exception, error:
            print "\n\nError is sendCMD."
            print "("+str(error)+")\n\n"
            self.ser.close()
            quit()
        return b

    def getData(self, cmd):
        try:
            start = time.time()
            self.sendCMD(0,cmd,[])
            while True:
                header = self.ser.read()
                if header == '$':
                    header = header+self.ser.read(2)
                    break
            datalength = struct.unpack('<b', self.ser.read())[0]
            code = struct.unpack('<b', self.ser.read())
            data = self.ser.read(datalength)
            temp = struct.unpack('<'+'h'*(datalength/2),data)
            elapsed = time.time() - start
            print temp
            #evaluateCommand[code[0]]()
            self.ser.flushInput()
            self.ser.flushOutput()
            return temp
        except Exception, error:
            pass



