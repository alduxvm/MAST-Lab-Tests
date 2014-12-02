#!/usr/bin/env python

"""main.py: Main simple test script to launch read and save data"""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2014 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import serial, struct, time
from modules.multiwii import MultiWii


if __name__ == "__main__":

	#MSP.startMulticopter()

	#board1 = MultiWii("/dev/tty.usbserial-A101CCVF")
	#board2 = MultiWii("/dev/tty.usbserial-A801WZA1")
	piggybackBoard = MultiWii("/dev/ttyUSB0")
	flightController = MultiWii("/dev/ttyUSB1")


	try:
		while True:
			flightController.getData(MultiWii.ATTITUDE)
			piggybackBoard.getData(MultiWii.ATTITUDE)
			line = "1:"+str(flightController.attitude)
			line += " 2:"+str(piggybackBoard.attitude)
			print line
			#MSP.getData(MSP.ATTITUDE)
	except Exception,error:
		print "Error: "+str(error)