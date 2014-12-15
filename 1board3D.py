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
from modules import cfg
from modules.multiwii import MultiWii


from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *


ax = ay = az = 0.0
yaw_mode = False

def resize((width, height)):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def drawText(position, textString):     
    font = pygame.font.SysFont ("Courier", 18, True)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def draw():
    global rquad
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); 
    
    glLoadIdentity()
    glTranslatef(0,0.0,-7.0)

    osd_text = "pitch: " + str("{0:.2f}".format(ay)) + ", roll: " + str("{0:.2f}".format(ax))

    if yaw_mode:
        osd_line = osd_text + ", yaw: " + str("{0:.2f}".format(az))
    else:
        osd_line = osd_text

    drawText((-2,-2, 2), osd_line)

    # the way I'm holding the IMU board, X and Y axis are switched 
    # with respect to the OpenGL coordinate system
    if yaw_mode:                             # experimental
        glRotatef(az, 0.0, 1.0, 0.0)  # Yaw,   rotate around y-axis
    else:
        glRotatef(0.0, 0.0, 1.0, 0.0)
    glRotatef(ay ,1.0,0.0,0.0)        # Pitch, rotate around x-axis
    glRotatef(-1*ax ,0.0,0.0,1.0)     # Roll,  rotate around z-axis

    glBegin(GL_QUADS)   
    glColor3f(0.0,1.0,0.0)
    glVertex3f( 1.0, 0.2,-1.0)
    glVertex3f(-1.0, 0.2,-1.0)      
    glVertex3f(-1.0, 0.2, 1.0)      
    glVertex3f( 1.0, 0.2, 1.0)      

    glColor3f(1.0,0.5,0.0)  
    glVertex3f( 1.0,-0.2, 1.0)
    glVertex3f(-1.0,-0.2, 1.0)      
    glVertex3f(-1.0,-0.2,-1.0)      
    glVertex3f( 1.0,-0.2,-1.0)      

    glColor3f(1.0,0.0,0.0)      
    glVertex3f( 1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)      
    glVertex3f(-1.0,-0.2, 1.0)      
    glVertex3f( 1.0,-0.2, 1.0)      

    glColor3f(1.0,1.0,0.0)  
    glVertex3f( 1.0,-0.2,-1.0)
    glVertex3f(-1.0,-0.2,-1.0)
    glVertex3f(-1.0, 0.2,-1.0)      
    glVertex3f( 1.0, 0.2,-1.0)      

    glColor3f(0.0,0.0,1.0)  
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2,-1.0)      
    glVertex3f(-1.0,-0.2,-1.0)      
    glVertex3f(-1.0,-0.2, 1.0)      

    glColor3f(1.0,0.0,1.0)  
    glVertex3f( 1.0, 0.2,-1.0)
    glVertex3f( 1.0, 0.2, 1.0)
    glVertex3f( 1.0,-0.2, 1.0)      
    glVertex3f( 1.0,-0.2,-1.0)      
    glEnd() 
         
def read_data():
    global ax, ay, az
    ax = ay = az = 0.0
    line_done = 0

    ax = flightController.attitude['angx']
    ay = flightController.attitude['angy']
    az = flightController.attitude['heading']


def start3d():
    global yaw_mode

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    screen = pygame.display.set_mode((640,480), video_flags)
    pygame.display.set_caption("Press Esc to quit, z toggles yaw mode")
    resize((640,480))
    init()
    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break       
        if event.type == KEYDOWN and event.key == K_z:
            yaw_mode = not yaw_mode
        read_data()
        draw()
      
        pygame.display.flip()
        frames = frames+1

    print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))



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