#!/usr/bin/env python
import Queue
import time
"""

METU CENG336 SPRING 2015

by Fatih Gokce, Alperen Eroglu, Caglar Seylan, Merve Asiler based on Mircea Agapie's pyrobosim2d project: 
http://sourceforge.net/projects/pyrobosim2d/

Simple 2D robot simulator in Python (2.6). You need to have Python, Pygame and PySerial 
installed for it to work. Launch from its own directory
by typing    python cengRoboSim.py   in the console/terminal window. Expects
two image files (background.png, robot.bmp) in the same directory.
Press ESC to exit, 'g' for sending $GO: start message to the PIC and switching to active mode, 
and 't' to toggle the trace visibility.

See the homework file for details.
'''



'''
    Copyright (C) 2011 Mircea Agapie 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.    
"""

DEFAULT_PORT = 0
DEFAULT_BAUD = 115200


back_image          = 'backgroundb.png'   #must have this file in same dir.
display_cols        = 800
display_rows        = 270
wall_color          = 'black'
undef_region_color  = 'gray'
gap_color	    = 'blue'

trace_color         = 'black'
trace_arc           = 10        #in degrees, shows on both sides of r.azi
trace_decrease      = -1       #negative, subtracts from robot size to make a smaller trace
trace_width         = 1
leave_trace         = 1         #default mode is not to leave traces

color_of_nothing    = 'white'
sim_version         = 'CENG336 Robosim v1.0'

r_image = 'robot.bmp'  #must have this file in same dir.
bomb_im	= 'bomb.jpg'
dollar_im = 'dollar.jpg'
exit_im = 'exit.jpg'
fail = 'fail.jpg'
success = 'success.jpg'
r_edge           = 20
r_init_azi       = 180        #azimuth, in degrees (up is 0)
r_init_x_topleft = 15
r_init_y_topleft = 15
r_init_fwd_speed = 5        #pixels per command
r_init_spin_speed= 9        #degrees per command
r_transparency   = 75       #0 is totally transp., 255 totally opaque
r_count_per_pixel = 1
r_count_per_degree = 1

r_opmode = 0

amount_of_energy = 240		# 16 levels of energy, each level consists of 15 units, each command takes 1 unit
num_of_dollars = 0
num_of_bombs = 0
tot_points = 0

last_x_position = 0		# Robot's last x position when the user sends END command
last_y_position = 0		# Robot's last y position when the user sends END command
exit_x = 15			# x position of exit cell
exit_y = 2			# y position of exit_cell

start_time = int(round(time.time() * 1000))

map_num_pixels = 30
grid_size_x = 16
grid_size_y = 4

blue = "#%02x%02x%02x" % (0, 0, 250)
red = "#%02x%02x%02x" % (250, 0, 0)
black = "#%02x%02x%02x" % (0, 0, 0)

WAITING = 0
GETTING = 1
PARSING = 2

NO_COMMAND = 0
FORWARD = 1
LEFT = 2
RIGHT = 3
STOP = 4
MAP = 5
END = 6

timeout = 135 		#in seconds

#import everything
import os, pygame, sys, threading, serial, time, array
from pygame.locals import *
import math
import random
from collections import deque

main_dir = os.path.split(os.path.abspath(__file__))[0]
screen = pygame.display.set_mode((display_cols, display_rows))
list_traces = list()


class Miniterm:
    def __init__(self, port, baudrate, parity, rtscts, xonxoff):
       # self.serial = serial.Serial(port, baudrate, parity=parity,
        #                        rtscts=rtscts, xonxoff=xonxoff, timeout=1)
                                
        '''	  In this case, if your operating system is:
				* Windows: You may need to change 'DEFAULT_PORT' in line 40 depending on the port assignment in your system. 
				For example, in your device manager, if the serial converter is assigned to COM7 
				then you need to change 0 to 6 (1 less than the number seen in the device manager) in line 40.
				* Linux: Comment out line 126 and 127 above, and remove #'s from the beginning of line 136 and 137. 
				The device name and number ('/dev/ttyUSB0' in line 136) may change on your system. You may need to 
				change this definition.'''
        self.serial = serial.Serial('/dev/ttyUSB0', baudrate, parity=parity,
                                rtscts=rtscts, xonxoff=xonxoff, timeout=1)

	self.state = WAITING
	self.data = ''
	self.command_available = False
	self.command = NO_COMMAND
	self.time = 0
	self.avg_time = -1;
	self.max_time = -999999;
	self.min_time = 999999;
	self.prev_time = -1;
	self.startTime = -1
	self.endTime = -1
	self.remTime = timeout
	self.cmdCount = 0;
	self.commands = deque()

    def start(self):
        self.alive = True
        self.receiver_thread = threading.Thread(target=self.reader)
        self.receiver_thread.setDaemon(1)
        self.receiver_thread.start()

    def stop(self):
        self.alive = False

    def join(self):
        self.receiver_thread.join(0.1)

    def updateFPS(self):
	self.time = time.time()
	diff1 = (self.time-self.startTime)*1000.0
	self.cmdCount = self.cmdCount + 1
	self.avg_time = (diff1)/self.cmdCount
	
	if(self.prev_time != -1):
		diff2 = (self.time-self.prev_time)*1000.0
		print('Current time difference from previous command: '+str(diff2)+' ms')
		if(diff2 < self.min_time):
			self.min_time = diff2
		if(diff2 > self.max_time):
			self.max_time = diff2
		self.prev_time = self.time
	else:
		self.prev_time = self.time

    def reader(self):
	global amount_of_energy, num_of_bombs
	while self.alive:
        	if self.state == WAITING:
			self.data = ''
		        if self.serial.inWaiting() == 0:
		            time.sleep(.01)
		            continue
		        
		        byte = self.serial.read()
			
		        # If a start byte is found, switch state
		        if byte == '$':
		            self.data += byte
			    self.state = GETTING
            	elif self.state == GETTING:
			byte = self.serial.read()

			self.data += byte

			if byte == ':':
				if len(self.data) == 3 or len(self.data) == 5 or len(self.data) == 6:
					# Energy Control
					if amount_of_energy == 0 and self.data[1] != 'E' and self.data[1] != 'C':
							print('SORRY! No Energy. Charge yourself and send the command again.')
							self.command_available = True
					else:
						# End of Energy Control
						if (self.data[1] == 'F'):
							if r_opmode == 1:
								amount_of_energy = amount_of_energy - 1
								self.updateFPS()
								self.commands.append('F')
							self.command_available = True
						elif (self.data[1] == 'R'):
							if r_opmode == 1:
								amount_of_energy = amount_of_energy - 1
								self.updateFPS()
								self.commands.append('R')
							self.command_available = True
						elif (self.data[1] == 'L'):
							if r_opmode == 1:
								amount_of_energy = amount_of_energy - 1
								self.updateFPS()
								self.commands.append('L')
							self.command_available = True 
						elif (self.data[1] == 'S'):
							if r_opmode == 1:
								amount_of_energy = amount_of_energy - 1
								self.updateFPS()
								self.commands.append('S')
							self.command_available = True
						elif (self.data[1] == 'P'):
							if r_opmode == 1:
								amount_of_energy = amount_of_energy - 1
								self.updateFPS()
								self.commands.append('P')
							self.command_available = True
						elif (self.data[1] == 'B'):
							if num_of_bombs == 0:
								print('SORRY! You do not have any bomb in stock.')
							elif r_opmode == 1:
								amount_of_energy = amount_of_energy - 1
								num_of_bombs = num_of_bombs - 1
								self.updateFPS()
								self.commands.append('B')
							self.command_available = True
						elif (self.data[1] == 'C'):
							if r_opmode == 1:
								amount_of_energy += 15
								if amount_of_energy > 240:
									amount_of_energy = 240
								self.updateFPS()
							self.command_available = True				
						elif (self.data[1] == 'E' and self.data[2] == 'N' and self.data[3] == 'D'):
							#END command
							if r_opmode == 1:
								self.endTime = time.time()
								self.updateFPS()
								self.commands.append('E')		
							self.command_available = True
						else:
							print('WARNING! Invalid Command. Command can be of type F, R, L, S, M or E. However, got ', self.data[1])
				else:
					print('WARNING! Invalid message length! Message was:' + self.data)
				self.state = WAITING

class Trace():
    def __init__(self, from_rect, start_angle, stop_angle):
        self.rect       = from_rect
        self.start_angle= start_angle
        self.stop_angle = stop_angle

class Obstacle(pygame.Rect):
    def __init__(self, x_topleft, y_topleft, width, height, color):
        self.x_topleft  = x_topleft
        self.y_topleft  = y_topleft
        self.width      = width
        self.height     = height
        self.color      = pygame.Color(color)

''' Changes alpha for surfaces with per-pixel alpha; only for small surfaces!
    Sets alpha for WHITE pixels to new_alpha.
    The alpha value is an integer from 0 to 255, 0 is fully transparent and
    255 is fully opaque. '''
def change_alpha_for_white(surface,new_alpha):
    size = surface.get_size()
    if size[0]>300 or size[1]>300:
        return surface
    for y in xrange(size[1]):
	for x in xrange(size[0]):
	    r,g,b,a = surface.get_at((x,y))
	    if r==255 and g==255 and b==255:
                surface.set_at((x,y),(r,g,b,new_alpha))
    return surface

''' Changes alpha for surfaces with per-pixel alpha; only for small surfaces!
    Sets alpha for pixels with alpha == 0 to new_alpha. It is needed b/c
    transform.smoothscale pads image with alpha=0. '''
def change_alpha_for_alpha(surface,new_alpha):
    size = surface.get_size()
    for y in xrange(size[1]):
	for x in xrange(size[0]):
	    r,g,b,a = surface.get_at((x,y))
	    if a<200:
                surface.set_at((x,y),(r,g,b,new_alpha))
    return surface

def draw_traces(target_surf):
    for t in list_traces:
        pygame.draw.arc(target_surf, pygame.Color(trace_color), t.rect,\
                        t.start_angle*math.pi/180, t.stop_angle*math.pi/180, trace_width)


maparr =  [[0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0],
           [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
           [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
           [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]


blocks =  [[0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1],
           [0,0,0,0,1,0,0,1,1,0,0,1,0,1,1,0,1],
           [0,1,0,0,1,0,0,1,1,0,0,1,0,1,1,0,1],
           [1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1],
	   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
'''
#no blocks
blocks =  [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
	   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
'''

for j in range(17):
	blocks[-1][j] = 1
for i in range(5):
	blocks[i][-1] = 1

blocks[-1][-1] = 1

list_rect_obstacles = []
list_obstacles = []

def createObstacles():
	global list_rect_obstacles, list_obstacles, blocks, wall_color, display_cols
	list_rect_obstacles = []
	list_obstacles = []
	for i in range(4):
		for j in range(16):
			if blocks[i][j] == 1:
				block = Obstacle(50*j,50*i,50,50, wall_color)
				list_obstacles.append(block)
	w = Obstacle(0,200,display_cols,1,wall_color)
	list_obstacles.append(w)

	for ob in list_obstacles:
		list_rect_obstacles.append(pygame.Rect(ob.x_topleft,ob.y_topleft,ob.width,ob.height))

createObstacles()
list_map_rect = []
list_map = []

for i in range(4):
	for j in range(16):
		if maparr[i][j] == -1:
			block = Obstacle((50*j),(50*i+270),50,50, undef_region_color)
			list_map.append(block)
		elif maparr[i][j] == 0:
			block = Obstacle(50*j,50*i+270,50,50, gap_color)
			list_map.append(block)
		elif maparr[i][j] == 1:
			block = Obstacle(50*j,50*i+270,50,50, wall_color)
			list_map.append(block)
w = Obstacle(0,269,display_cols,1,wall_color)
list_map.append(w)
w = Obstacle(0,470,display_cols,1,wall_color)
list_map.append(w)

for ob in list_map:
    list_map_rect.append(pygame.Rect(ob.x_topleft,ob.y_topleft,ob.width,ob.height))

class Robot(pygame.sprite.Sprite):
    def __init__(self, image, x_topleft, y_topleft, azimuth, fwd_speed, spin_speed):

	try:
		self.miniterm = Miniterm(DEFAULT_PORT, DEFAULT_BAUD, 'N',
	    		rtscts=False, xonxoff=False,
	)
	except serial.SerialException, e:
		sys.stderr.write("could not open port %r: %s\n" % (DEFAULT_PORT, e))
		sys.exit(1)

	self.miniterm.start()

        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        #Sprites must have an image and a rectangle
        self.image          = image
        self.rect           = image.get_rect()
        self.rect.topleft   = x_topleft, y_topleft
        self.fwd_speed      = fwd_speed
        self.spin_speed     = spin_speed
        self.azi            = azimuth       #in degrees
        self.original       = self.image    #unchanging copy, for rotations
        self.opmode         = 0             #0=idle, 1=active
        
	self.spin(0)
	self.xfloat = self.rect.center[0] * 1.0
	self.yfloat = self.rect.center[1] * 1.0

	self.xpixel = self.rect.center[0]
	self.ypixel = self.rect.center[1]

	self.moveSuccesfull = False
       
    def update(self):

        if   (self.opmode == 0): 				#IDLE
			if self.miniterm.command_available == True:
				print('WARNING! Command received in IDLE mode!')
				self.miniterm.command_available = False
			return          				
        elif (self.opmode == 1): self.mode_active()     	#ACTIVE
        elif (self.opmode == 2): 			     			#END
			if self.miniterm.command_available == True:
				print('WARNING! Command received in END mode!')
				self.miniterm.command_available = False
			return          				
        else:
            print 'ERROR! Undefined operation mode!'

    def mode_active(self):	
	global tot_points, num_of_bombs, num_of_dollars, blocks, last_x_position, last_y_position
	if len(self.miniterm.commands) > 0:
		cmd = self.miniterm.commands.popleft()
		if (cmd == 'F'):
			temp_unghi = self.azi*math.pi/180
			walk_dx = -self.fwd_speed*math.sin(temp_unghi)
			walk_dy = -self.fwd_speed*math.cos(temp_unghi)
			self.move(walk_dx, walk_dy)
			self.miniterm.serial.write('$')
			self.miniterm.serial.write('E')
			if self.moveSuccesfull == True:
				self.miniterm.serial.write(self.a2s([self.fwd_speed*r_count_per_pixel]))
			else:
				self.miniterm.serial.write(self.a2s([0x00]))
			self.miniterm.serial.write(':')
		if (cmd == 'R'):
			self.spin(-1.0*self.spin_speed)
			self.miniterm.serial.write('$')
			self.miniterm.serial.write('E')
			self.miniterm.serial.write(self.a2s([self.spin_speed*r_count_per_degree]))
			self.miniterm.serial.write(':')
		if (cmd == 'L'):
			self.spin(self.spin_speed)
			self.miniterm.serial.write('$')
			self.miniterm.serial.write('E')
			self.miniterm.serial.write(self.a2s([self.spin_speed*r_count_per_degree]))
			self.miniterm.serial.write(':')
		if (cmd == 'S'):
			if (self.azi % 90) != 0:
				print('WARNING! You should send STOP command at multiple of 90 degrees.') 
			if ((self.rect.center[0]-25)%50) != 0 or ((self.rect.center[1]-25)%50) != 0:
				print('WARNING! You should send STOP command at center points.')
			self.sendSensorData()
		#MAP command is handled serial read, not here.
		#if self.miniterm.command == MAP:
			#updateMap()
			#self.miniterm.command_available = False
		if (cmd == 'P'):
			xpixel = int(math.ceil(self.xfloat / 50.0)) - 1 
			ypixel = int(math.ceil(self.yfloat / 50.0)) - 1
			for i in range (24):
				if q[i].status == 1 and q[i].x == xpixel and q[i].y == ypixel:
					if q[i].type == 0:
						tot_points += 10
						num_of_dollars += 1
					elif q[i].type == 1:
						#tot_points += 2
						num_of_bombs += 1
					q[i].status = 2
		if (cmd == 'B'):
			xpixel = int(math.ceil(self.xfloat / 50.0)) - 1 
			ypixel = int(math.ceil(self.yfloat / 50.0)) - 1
			if (xpixel - 1) >= 0 and blocks[ypixel][xpixel-1] == 1:
				blocks[ypixel][xpixel-1] = 0
			if (xpixel + 1) < 16 and blocks[ypixel][xpixel+1] == 1:
				blocks[ypixel][xpixel+1] = 0
			if (ypixel - 1) >= 0 and blocks[ypixel-1][xpixel] == 1:
				blocks[ypixel-1][xpixel] = 0
			if (ypixel + 1) < 4 and blocks[ypixel+1][xpixel] == 1:
				blocks[ypixel+1][xpixel] = 0
			createObstacles()
		if (cmd == 'E'):
			last_x_position = int(math.ceil(self.xfloat / 50.0)) - 1 
			last_y_position = int(math.ceil(self.yfloat / 50.0)) - 1
			self.opmode = 2
			r_opmode = 2
			self.endWithCommand()
			

		#print ('x: ' + str(self.rect.center[0]) + ' y: ' + str(self.rect.center[1]) + ' theta: ' + str(self.azi))

    def move(self,dx,dy):

	self.xfloat = self.xfloat + dx 
	self.yfloat = self.yfloat + dy	
	
        previous_rect = self.rect           #remember in case undo is necessary

        self.rect = self.rect.move(self.xfloat-self.xpixel,self.yfloat-self.ypixel)
        if self.rect.collidelist(list_rect_obstacles) != -1 or self.rect.topleft[0] < 0 or self.rect.topleft[1] < 0 or self.rect.topleft[0] > display_cols - r_edge or self.rect.topleft[1] > display_rows - r_edge:
            print 'WARNING! I am not able move because of a block in front of me.'
            self.rect = previous_rect                   #undo the move
	    self.xfloat = self.xfloat - dx
	    self.yfloat = self.yfloat - dy
            self.moveSuccesfull = False
        else:                   #if there was no collision
	    self.moveSuccesfull = True
            if leave_trace:     #update trace list
                tr = self.rect.inflate(trace_decrease, trace_decrease)
                list_traces.append(Trace(tr, 90+self.azi-trace_arc, 90+self.azi+trace_arc))

	self.xpixel = self.rect.center[0]
	self.ypixel = self.rect.center[1]
       
    def spin(self,dtheta):
        center = self.rect.center
        self.azi += dtheta
        if self.azi >= 360:        
            self.azi = self.azi-360
        if self.azi < 0:
            self.azi = self.azi+360
        temp_rota_imag = pygame.transform.rotate(self.original, self.azi)
        self.image = pygame.transform.smoothscale(temp_rota_imag,(r_edge,r_edge))
        #smoothscale pads w/pixels having alpha=0. Increasing alpha to see a faint rect.
        self.image = change_alpha_for_alpha(self.image, r_transparency)
        self.rect = self.image.get_rect()
        self.rect.center = center
        '''when using transform.smoothscale, rotations never generate collisions, b/c
        the image always stays a square of edge r_edge'''
        if leave_trace:     #update trace list
            tr = self.rect.inflate(trace_decrease, trace_decrease)
            list_traces.append(Trace(tr, 90+self.azi-trace_arc, 90+self.azi+trace_arc))

    def a2s(self,array):
    	return ''.join(chr(b) for b in array)
		
    def sendSensorData(self):
		self.miniterm.serial.write('$')
		self.miniterm.serial.write('D')
		self.miniterm.serial.write(self.a2s([int(math.ceil(self.xfloat / 50.0)) - 1, int(math.ceil(self.yfloat / 50.0)) - 1, int(math.floor(self.azi / 9.0))]))
		self.miniterm.serial.write(':')

    def sendAlertCommand(self, x, y, type):
		self.miniterm.serial.write('$')
		self.miniterm.serial.write('A')
		self.miniterm.serial.write(self.a2s([x, y, type]))
		self.miniterm.serial.write(':')

    def endWithCommand(self):
	print('')
	print('You sent END command after '+str(self.miniterm.endTime-self.miniterm.startTime)+' seconds.')
	print('')

	print('')
	print('Timing between commands [All three values should be as close as to 50 ms]:')
	print('')
	print('\tAvg: '+str(round(self.miniterm.avg_time,2))+' ms')
	print('\tMax: '+str(round(self.miniterm.max_time,2))+' ms')
	print('\tMin: '+str(round(self.miniterm.min_time,2))+' ms')
	
	print('')
	print('\tTotal points, # of Bombs, # of Dollars:')
	print('')
	print('\tTotal Points: '+str(tot_points))
	print('\t# of Bombs: '+str(num_of_bombs))
	print('\t# of Dollars: '+str(num_of_dollars))

	print('')
	print('You can reset the simulator by pressing r.')
	print('')

    def resetEverything(self):
	global blocks, num_of_bombs, num_of_dollars, tot_points, last_x_position, last_y_position, amount_of_energy
	self.rect.topleft = r_init_x_topleft, r_init_y_topleft
        self.azi            = r_init_azi        
	self.spin(0)
	self.xfloat = self.rect.center[0] * 1.0
	self.yfloat = self.rect.center[1] * 1.0

	self.xpixel = self.rect.center[0]
	self.ypixel = self.rect.center[1]

	self.moveSuccesfull = False
		
	#reset map

	color = pygame.Color(undef_region_color)
	for i in range(4):
		for j in range(16):
			maparr[i][j] = -1
			list_map[i*16+j].color = color

	color = pygame.Color(gap_color)
	maparr[0][0] = 0
	maparr[0][15] = 0
	list_map[0].color = color
	list_map[15].color = color

	self.miniterm.prev_time = 0
	self.miniterm.time = 0
	self.miniterm.prev_time = -1;
	self.miniterm.avg_time = -1;
	self.miniterm.max_time = -999999;
	self.miniterm.min_time = 999999;
	self.miniterm.startTime = -1
	self.miniterm.endTime = -1
	self.miniterm.remTime = timeout
	self.miniterm.cmdCount = 0
	self.miniterm.commands = deque()
	self.miniterm.command_available = False
	construct_queue()
	tot_points = 0
	num_of_bombs = 0
	num_of_dollars = 0
	amount_of_energy = 240
	last_x_position = 0
	last_y_position = 0

	blocks = [[0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1],
           [0,0,0,0,1,0,0,1,1,0,0,1,0,1,1,0,1],
           [0,1,0,0,1,0,0,1,1,0,0,1,0,1,1,0,1],
           [1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1],
	   [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

	createObstacles()

	return


########end of Robot class########

def load_image(name):
    path = os.path.join(main_dir, name)
    temp_image = pygame.image.load(path).convert_alpha()  #need this if using ppalpha
    return change_alpha_for_white(temp_image, r_transparency)  

###########################################
###########################################

class Item():
	def __init__(self, type, x, y, pop_time, act):
		self.type = type
		self.x = x
		self.y = y
		self.pop_time = pop_time		
		self.status = act

q = [Item(0, 0, 0, 0, 0) for i in range(0, 24)]
		
def construct_queue():
	random.seed()

	type_array = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
	type_array2 = [0, 1, 0, 1]

	flag = False
	while not flag:
		flag = True
		#dc = 0
		random.shuffle(type_array)
		for i in range(0, 18):
			if (type_array[i] == type_array[i + 1]) and (type_array[i + 1] == type_array[i + 2]) and (type_array[i] == type_array[i + 2]):
		#		dc += 1
				flag = False
		#print(dc)

	flag = False
	while not flag:
		flag = True
		#dc = 0
		random.shuffle(type_array2)
		for i in range(0, 2):
			if (type_array2[i] == type_array2[i + 1]) and (type_array2[i + 1] == type_array2[i + 2]) and (type_array2[i] == type_array2[i + 2]):
		#		dc += 1
				flag = False
		#print(dc)
			
	pop_time = 0
	# for the part1
	for i in range(0, 4):
		type = type_array2[i]
		while True:
			a = random.randrange(0, 5)
			b = random.randrange(0, 4)
			if not ((a == 0 and b == 3) or (a == 1 and b == 2) or (a == 4 and b == 1) or (a == 4 and b == 2)):
				break
		pop_time += (random.randrange(0, 60) + 1) * 100
		q[i] = Item(type, a, b, pop_time, 0)

	# for the part2
	for i in range(0, 12):
		type = type_array[i]
		while True:
			a = random.randrange(0, 11)
			b = random.randrange(0, 4)
			if not ((a == 0 and b == 3) or (a == 1 and b == 2) or (a == 4 and b == 1) or (a == 4 and b == 2) or (a == 5 and b == 0) or (a == 5 and b == 3) or (a == 7 and b == 1) or (a == 7 and b == 2) or (a == 8 and b == 1) or (a == 8 and b == 2) or (a == 10 and b == 0) or (a == 10 and b == 3)):
				break
		pop_time += (random.randrange(0, 60) + 1) * 100
		q[i+4] = Item(type, a, b, pop_time, 0)

	# for the part3
	for i in range(12, 20):
		type = type_array[i]
		while True:
			a = random.randrange(0, 13)
			b = random.randrange(0, 4)
			if not ((a == 0 and b == 3) or (a == 1 and b == 2) or (a == 4 and b == 1) or (a == 4 and b == 2) or (a == 5 and b == 0) or (a == 5 and b == 3) or (a == 7 and b == 1) or (a == 7 and b == 2) or (a == 8 and b == 1) or (a == 8 and b == 2) or (a == 10 and b == 0) or (a == 10 and b == 3) or (a == 11 and b == 1) or (a == 11 and b == 2)):
				break
		pop_time += (random.randrange(0, 60) + 1) * 100
		q[i+4] = Item(type, a, b, pop_time, 0)

def main():
    global leave_trace, list_traces, r_opmode, maparr, list_map, list_map_rect
    global tot_points, num_of_bombs, num_of_dollars, amount_of_energy, last_x_position, last_y_position, exit_x, exit_y

    pygame.init()           #also calls display.init()    

    r_sprite = load_image(r_image)
    bomb_sprite = load_image(bomb_im)
    dollar_sprite = load_image(dollar_im)
    exit_sprite = load_image(exit_im)
    background  = load_image(back_image)
    fail_sprite = load_image(fail)
    success_sprite = load_image(success)

    #prepare simulation objects
    #clock = pygame.time.Clock()
    r = Robot(r_sprite, r_init_x_topleft, r_init_y_topleft,r_init_azi, r_init_fwd_speed,\
              r_init_spin_speed)
    allsprites = pygame.sprite.RenderPlain((r))

    #display the environment once, right before event loop
    screen.blit(background, (0, 0))
    count = -1
    for ob in list_obstacles:
        count = count + 1
        s = pygame.display.get_surface()
        s.fill(ob.color, list_rect_obstacles[count])
    count = -1
    for ob in list_map:
        count = count + 1
        s = pygame.display.get_surface()
        s.fill(ob.color, list_map_rect[count])

    pygame.display.flip()   
    pygame.display.set_caption(sim_version + ' \tmode: IDLE')

    font = pygame.font.SysFont("calibri",30)
    font2 = pygame.font.SysFont("calibri",18)
    text1 = font.render('AREA', True,(0,0,0))
    text2 = font.render('CURRENT MAP', True,(0,0,0))

    construct_queue()
    going = True
    while going:

        #Event loop################################
        for event in pygame.event.get():
            if event == QUIT:
                going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
			going = False
                if event.key == K_g:
		    if r.opmode != 2 and r.opmode != 1:
			    r.miniterm.serial.write('$')
			    r.miniterm.serial.write('G')
			    r.miniterm.serial.write('O')
			    r.miniterm.serial.write(':')
		            r.opmode = 1            #ACTIVE mode
			    r_opmode = 1
			    start_time = int(round(time.time() * 1000))
			    r.miniterm.max_rate = -100
			    r.miniterm.min_rate = 9999
			    r.miniterm.avg_rate = 20
			    r.miniterm.prev_time_valid = 0
			    r.miniterm.cmdCount = 0
			    r.miniterm.command_available = False
			    r.miniterm.state = WAITING
		            pygame.display.set_caption(sim_version + ' \tmode: ACTIVE')
			    r.miniterm.startTime = time.time()
                if event.key == K_r:
		    if r.opmode == 2:
			list_traces = list()
			r.resetEverything()
			pygame.display.set_caption(sim_version + ' \tmode: IDLE')
			r.opmode = 0 # enter IDLE mode
			r_opmode = 0
                if event.key == K_t:        #toggles the tracing mode
                    if leave_trace:
                        leave_trace = 0
                        list_traces = list()
                        print 'Trace is OFF.'
                    else:
                        leave_trace = 1
			print 'Trace is ON.'

        #End of event loop#######################
                        
        #Redrawing    
        allsprites.update()
        screen.blit(background, (0, 0))  #redraws the entire bkgrnd.
        count = -1
        for ob in list_obstacles:
            count = count + 1
            s = pygame.display.get_surface()
	    s.fill(ob.color, list_rect_obstacles[count])
    	count = -1
    	for ob in list_map:
            count = count + 1
            s = pygame.display.get_surface()
            s.fill(ob.color, list_map_rect[count])

	screen.blit(text1,(360.,202.))
	screen.blit(text2,(325.,475.))
	screen.blit(exit_sprite, (755, 102))	# Show the symbolic exit icon

	text3 = font2.render('x: '+str(r.rect.center[0])+\
			    ' y: '+str(r.rect.center[1])+\
			    ' Theta: '+str(round(r.azi,0)), True,(0,100,0))

	screen.blit(text3,(20.,230.))
	if(r.opmode == 1):
		cur_time = int(round(time.time() * 1000))
		for i in range(0, 24):
			if(cur_time - start_time) > q[i].pop_time and q[i].status == 0:
				r.sendAlertCommand(q[i].x, q[i].y, q[i].type)
				q[i].status = 1
		for i in range(0, 24):
			if q[i].status == 1:
				screen.blit(bomb_sprite, (q[i].x * 50 + 15, q[i].y * 50 + 15))
				if q[i].type == 1:
					exp_time = 5000
					screen.blit(bomb_sprite, (q[i].x * 50 + 15, q[i].y * 50 + 15))
				elif q[i].type == 0:
					exp_time = 5500
					screen.blit(dollar_sprite, (q[i].x * 50 + 15, q[i].y * 50 + 15))
				if (cur_time - start_time) - q[i].pop_time > exp_time:
					q[i].status = 2
		r.miniterm.remTime = timeout-(time.time()-r.miniterm.startTime)
		if r.miniterm.remTime <= 0:
			r.opmode = 2
			r_opmode = 2
			pygame.display.set_caption(sim_version + ' \tmode: END')
			r.miniterm.state = WAITING
		text5 = font2.render('Timing[ms] Avg: '+str(round(r.miniterm.avg_time,2))+\
						     '           Max: '+str(round(r.miniterm.max_time,2))+\
							 '                      Min: '+str(round(r.miniterm.min_time,2)), True,(0,100,0))
		text6 = font2.render('Total Points: '+str(tot_points)+\
						     '                    # of Bomb(s): '+str(num_of_bombs)+\
							 '                    # of Dollar(s): '+str(num_of_dollars)+\
					'                 Amount of Energy[unit]: '+str(amount_of_energy), True,(0,100,0))
		screen.blit(text5,(220.,230.))
		screen.blit(text6,(20.,250.))
	elif(r.opmode == 2):
		text5 = font2.render('Timing[ms] Avg: '+str(round(r.miniterm.avg_time,2))+\
						     '           Max: '+str(round(r.miniterm.max_time,2))+\
							 '                      Min: '+str(round(r.miniterm.min_time,2)), True,(0,100,0))
		text6 = font2.render('Total Points: '+str(tot_points)+\
						     '                    # of Bomb(s): '+str(num_of_bombs)+\
							 '                    # of Dollar(s): '+str(num_of_dollars)+\
					'                 Amount of Energy[unit]: '+str(amount_of_energy), True,(0,100,0))
		screen.blit(text5,(220.,230.))
		screen.blit(text6,(20.,250.))
		if num_of_dollars > 2 and exit_x == last_x_position and exit_y == last_y_position:
			screen.blit(success_sprite, (340, 50))
		else:
			screen.blit(fail_sprite, (350, 50))
        draw_traces(screen)
        allsprites.draw(screen)
	
        #pygame.display.update()
        pygame.display.flip()   #all changes are drawn at once (double buffer)
        #pygame.time.delay(100)
    pygame.quit()               #also calls display.quit()


if __name__ == '__main__':
    main()

        

