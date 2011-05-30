#! /usr/bin/env python

import serial
import os.path

def scan():
	available = []
   
 	if os.path.exists('/dev') == 1: 
   		for i in range(256):
       			try:
           			s = serial.Serial('/dev/ttyUSB%d' % i)
           			available.append(s.portstr)
           			s.close()

       			except serial.SerialException:
           			pass

   	for i in range(256):
       		try:
           		s = serial.Serial(i)
           		available.append(s.portstr)
           		s.close()

       		except serial.SerialException:
           		pass
   	return available

if __name__ == '__main__':
	print "Found ports:"
	for s in scan(): 
		print s
