#!/usr/bin/python

################################################################################
# Author: Anubhav Jaiswal                                                      #
# Email: anubhav2503@gmail.com                                                 #
# This is a prototype for the 3D Turtle Art Activity which is part of Sugar.   #
################################################################################


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import time

#mul_factor=1

class Turtle():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        self.penDown = True
        
        self.xRotate = 0.0
        self.yRotate = 0.0
        self.zRotate = 0.0

        self.direction = [1.0 , 0.0 , 0.0]

        self.moves_list = [[0.0,0.0,0.0,True]]
        
    def forward(self, value):
        #global mul_factor
        #value = value * mul_factor
        #mul_factor+=0.01
        self.x = self.x + (value * self.direction[0])
        self.y = self.y + (value * self.direction[1])
        self.z = self.z + (value * self.direction[2])
  
    def roll(self, theta):
        temp = []
        self.xRotate = self.xRotate + theta 
        theta = math.radians(theta)
        temp.append(self.direction[0] * 1.0)
        temp.append((self.direction[1] * math.cos(theta)) + (self.direction[2] * math.sin(theta)))
        temp.append((self.direction[1] * -1.0 * math.sin(theta)) + (self.direction[2] * math.cos(theta)))
        self.direction = temp
 
    def pitch(self, theta):
        temp = []
        self.yRotate = self.yRotate + theta 
        theta = math.radians(theta)
        temp.append((self.direction[0] * math.cos(theta)) + (self.direction[2] * -1.0 * math.sin(theta)))
        temp.append(self.direction[1] * 1.0)
        temp.append((self.direction[0] * math.sin(theta)) + (self.direction[2] * math.cos(theta)))
        self.direction = temp
 
    def yaw(self, theta):
        temp = []
        self.zRotate = self.zRotate + theta 
        theta = math.radians(theta)
        temp.append((self.direction[0] * math.cos(theta)) + (self.direction[1] * math.sin(theta)))
        temp.append((self.direction[0] * -1.0 * math.sin(theta)) + (self.direction[1] * math.cos(theta)))
        temp.append(self.direction[2] * 1.0)
        self.direction = temp
        #print self.direction
 
    def penup(self):
        self.penDown = False
 
    def pendown(self):
        self.penDown = True
        
    def setxyz(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.moves_list.append([x, y, z, False]) # Add 1 extra element for next starting point after many setxyz
        if self.moves_list[-1][3] == False:
            self.moves_list[-1] = [x, y, z, False]

def initRendering():

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glClearColor(0.0,0.0,0.0,1.0)
    #gluOrtho2D(0.0,640.0,0.0,480.0)

def handleResize(w, h):
    
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, w / h, 0.5, 30.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def display():
   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    #glTranslatef(-10.0, -10.0, -10.0)
    glTranslatef(0, 0, -10.0)
    glRotatef(45,1,0,0)
    glRotatef(-45,0,1,0)
    #glRotatef(-45,1,0,1)
    #glRotatef(-60,0,0,1)
    glScalef(0.2, 0.2, 0.2)

    glPushMatrix()
    drawAxes()
    glPopMatrix()

    #draw Pen
    glPushMatrix()
    glTranslatef(pen.x, pen.y, pen.z)
    glRotatef(pen.xRotate,1.0,0.0,0.0)
    glRotatef(pen.yRotate,0.0,1.0,0.0)
    glRotatef(pen.zRotate,0.0,0.0,1.0)
    #drawCube()
    glColor3f(1.0,1.0,1.0)
    glutSolidSphere(0.2,20,20)
    glPopMatrix()

    #draw Lines
    glPushMatrix()
    drawLines()
    glPopMatrix()

    ambientColor = [0.8, 0.8, 0.8, 0.0]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambientColor)

    lightPos = [0.5,1.0,1.0, 0.0]
    lightColor = [0.5, 0.5, 0.5, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)

    glPopMatrix()
    glFlush()
    glutSwapBuffers()
    command()

def command():
    """ Command parsing and execution function """
    def exec_single_command(tokens):
        """ Executes a single command
            Requires, command name, tokens
        """
        func = tokens[0].lower()

        if func == 'fd':
            value = float(tokens[1])
            pen.forward(value)
            pen.moves_list.append([pen.x,pen.y,pen.z,pen.penDown])
        elif func == 'rx':
            value = float(tokens[1])
            pen.roll(value)
        elif func == 'ry':
            value = float(tokens[1])
            pen.pitch(value)
        elif func == 'rz':
            value = float(tokens[1])
            pen.yaw(value)
        elif func == 'setxyz':
            valX = float(tokens[1])
            valY = float(tokens[2])
            valZ = float(tokens[3])
            pen.setxyz(valX, valY, valZ)
        elif func == 'pen':
            if tokens[1] == 'd':
                pen.pendown()
            elif tokens[1] == 'u':
                pen.penup()
        elif func == 'reset':
            pen.direction = [1.0, 0.0, 0.0]
    
    try: 
        cmd = raw_input("> ")
    except EOFError:
        print "Caught EOF, terminating"
        time.sleep(5)
        sys.exit(1)

    tokens = cmd.split(' ')
    func = tokens[0].lower()

    if func in ['fd', 'rx', 'ry', 'rz', 'setxyz', 'pen', 'reset']:
        exec_single_command(tokens)

    elif func == 'repeat':
        count = int(tokens[1])
        cmd_r = raw_input(">> ")
        cmd_list = []
        while cmd_r != 'end':
            #print cmd_r
            cmd_list.append(cmd_r)    
            cmd_r = raw_input(">> ")
        # reverse list
        cmd_list.reverse()
        # Exec commands in list
        # TODO: handle malicious and/or multi-statement commands written within repeat
        for i in xrange(count):
            for cmd in cmd_list:
                exec_single_command(cmd.split(' '))
        
    elif func == 'x':
        sys.exit()
    
# ANOTHER OPTION FOR POINTER
def drawCube():
     
    #Back
    glBegin(GL_POLYGON)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()

    #Front
    glBegin(GL_POLYGON)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(  0.5, -0.5, 0.5 )
    glVertex3f(  0.5,  0.5, 0.5 )
    glVertex3f( -0.5,  0.5, 0.5 )
    glVertex3f( -0.5, -0.5, 0.5 )
    glEnd()

    #Right
    glBegin(GL_POLYGON)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glEnd()

    #Left
    glBegin(GL_POLYGON)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()

    #Top
    glBegin(GL_POLYGON)
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glEnd()

    #Bottom
    glBegin(GL_POLYGON)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glEnd()

def drawAxes():

    for i in range(-10,10):
        glColor3f(1.0,0.0,0.0)
        if i == 0:
            glColor3f(0.0,1.0,1.0)
        glBegin(GL_LINES)
        glVertex3f(-10.0,0.0,i)
        glVertex3f(10.0,0.0,i)
        glEnd()

    for i in range(-10,10):
        glColor3f(1.0,0.0,0.0)
        if i == 0:
            glColor3f(0.0,1.0,1.0)
        glBegin(GL_LINES)
        glVertex3f(i,0.0,-10.0)
        glVertex3f(i,0.0,10.0)
        glEnd()

    glColor3f(0.0,1.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,-10.0,0.0)
    glVertex3f(0.0,10.0,0.0)
    glEnd()

    
def drawLines():

    for i,j in zip(pen.moves_list, pen.moves_list[1:]):
        source = i
        dest = j
        if j[3] is False:
            continue
        glBegin(GL_LINES)
        glColor3f(1.0,1.0,1.0)
        glVertex3f(j[0],j[1],j[2])
        glVertex3f(i[0],i[1],i[2])
        glEnd()
 
#def camera():

def handleKeypress1(key, x, y):
    if key == '\x1b':
        sys.exit()

def handleKeypress2(key, x, y):

    if key == GLUT_KEY_LEFT:
        pen.yRotate = pen.yRotate - 10
    if key == GLUT_KEY_RIGHT:
        pen.yRotate = pen.yRotate + 10
    if key == GLUT_KEY_UP:
        pen.xRotate = pen.xRotate - 10
    if key == GLUT_KEY_DOWN:
        pen.xRotate = pen.xRotate + 10


if __name__ == '__main__':
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    w = glutGet(GLUT_SCREEN_WIDTH)
    h = glutGet(GLUT_SCREEN_HEIGHT)

    windowWidth = w * 2 / 3
    windowHeight = h * 2 / 3

    glutInitWindowSize(windowWidth, windowHeight)
    glutInitWindowPosition( (w - windowWidth)/2, (h - windowHeight)/2 )
    glutCreateWindow("Turtle Art 3D")

    pen = Turtle()
    initRendering()
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutKeyboardFunc(handleKeypress1)
    glutSpecialFunc(handleKeypress2)
    glutReshapeFunc(handleResize)
    glutMainLoop()
