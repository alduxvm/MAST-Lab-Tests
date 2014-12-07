#!/usr/bin/env python

"""optiUDP.py: Handles UDP SocketServer communications for reading a Optitrack Motion Capture System."""

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2014 Aldux.net"

__license__ = "GPL"
__version__ = "1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"


import struct, time, socket
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import cfg

UDPmess = ();
UDPtimestamp = 0


class twistedUDP(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        global UDPmess
        numOfValues = len(data) / 8
        mess=struct.unpack('>' + 'd' * numOfValues, data)
        UDPmess = [ round(element,4) for element in mess ]
        UDPmess.insert(0,time.time())
        #self.sendMSG(cfg.line,(cfg.UDPip, cfg.UDPportOut))
        #self.sendMSG("1",(cfg.UDPip, cfg.UDPportOut))

    def sendMSG(self, data, (host, port)):
         self.transport.write(data, (host, port))

def startTwisted():
    reactor.listenUDP(cfg.UDPport, twistedUDP())
    reactor.run()