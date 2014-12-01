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

	board1 = MultiWii("/dev/tty.usbserial-A101CCVF")
	board2 = MultiWii("/dev/tty.usbserial-A801WZA1")

	try:
		while True:
			board1.getData(MultiWii.ATTITUDE)
			board2.getData(MultiWii.ATTITUDE)
			print "1:"+str(board1.attitude)+" 2:"+str(board2.attitude)
			#MSP.getData(MSP.ATTITUDE)
	except Exception,error:
		print "Error: "+str(error)