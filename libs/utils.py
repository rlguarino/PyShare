"""
Author: Ross Guarino
The module for commonly used funcitons that the PyShare program uses
"""
import time

def formatTime():
	_time = str(time.asctime())
	while (len(_time) < 15):
		_time = ' '+_time
	return _time
	
def isIP(string):
	"""
	Checks to see if the string is a valid IP address. 
	return True if it is, False if it is not.
	"""
	pass
	
def formatSize(number):
	"""
	Formats a number to be the right length as a precurser packet
	"""
	temp=str(number)
	while(len(temp)<4):
		temp='0'+temp
	return temp
	
def catch(conn):
	"""catch: socket -> str
	#Catches data that comes in two packets. 1: the size of the scond packet and 2: the actual data.
	"""
	data = conn.recv(4)
	data = str(conn.recv(int(data.decode())).decode())
	return data

def throw(s, data):
	"""
	Sends strings across the network. first sends the formatted number and then the actual data
	"""
	#print('sending...  '+str(data))
	s.send(formatNumber(len(data)).encode())
	s.send(data.encode())
	#print('sent')

def formatNumber(number): 
	temp=str(number)
	while(len(temp)<4):
		temp='0'+temp
	return temp	