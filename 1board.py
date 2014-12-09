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


if __name__ == "__main__":

    try:

        if cfg.DRONE:
            flightController = MultiWii("/dev/tty.usbserial-A101CCVF")
            #flightController = MultiWii("/dev/ttyUSB1")
            readThread = threading.Thread(target=flightController.getDataInf, args=(MultiWii.RAW_IMU,))
            readThread.start()

        if cfg.PRINT:
            printThread = threading.Thread(target=cfg.manageData, args=(flightController.rawIMU,))
            printThread.start()

        if cfg.TWIS:
            optiUDP.startTwisted()
        
          
    except Exception,error:
        print "Error: "+str(error)
        flightController.ser.close()
        file.close()