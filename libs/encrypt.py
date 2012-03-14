"""
Author: Ross Guarino
A module for using Diffie Hellman key transfer and exor encryption in python3
"""
import random
def bar():
	print('it works')

def genKey( s, role='INIT'):
	"""
	denKey: socket, type(default: KEY_INT) -> key(int/string)
	Takes in a socket instance
	Generates a key and returns the key in the form of the int
	"""
	if role== 'INIT':
		p = str(random.randint(10, pow(90,10)))
		base = str(random.randint(10,1000))
		privateA = str(random.randint(10,1000))
		publicA = str(pow(int(base),int(privateA))%int(p))
		while len(p)<20:
			p='0'+p
		while len(base)<4:
			base='0'+base
		
		master=p+base+publicA
		s.send(master.encode())
		data=s.recv(4096).decode()
		B=data

		key= int(pow(int(B),int(privateA))%int(p))
	
		return key
		
		
	elif role== "RECV":
		
		privateB= str(random.randint(10,1000))
		data= s.recv(4096).decode()
		p=data[0:20]
		base=data[20:24]
		A=data[24:]
		publicB = str(pow(int(base),int(privateB))%int(p))
		while len(publicB)<4:
			publicB='0'+publicB

		s.send(publicB.encode())
			
		key = int(pow(int(A),int(privateB))%int(p))
		
		return key
		

def encrypt(string, key):
	"""Takes a string and a integer(ke) and uses the integer to encrpt the string"""
	try:
		binResult=''
		for char in string:
			temp=bin(ord(char))[2:]
			while len(temp) < 7:
				temp='0'+temp
			binResult=binResult+temp
		return exor(binResult, bin(int(key))[2:])
	except(ValueError, TypeError):
		print('Something went wront with the ecryption, you may have got a bad packet')
		return 1

def exor(message, key):
	"""Takes in a string exors it with the key then return it"""
	try:
		count=0
		master=""
		for letter in message:
			if(count==len(key)):
				count=0
			master=master+str(int(letter) ^ int(key[count]))
			count=count+1
		return master
	except(ValueError):
		print('Something went wront with the decryption, you may have got a bad packet')
		return 1

def refract(binary, key):
	try:
		""" takes in a encrypted bin string and a int(key) and returns a string """
		binary=exor(binary,bin(int(key))[2:])
		#print('binary'+binary)
		master=""
		for x in range(0, int(len(binary)/7)):
			master=master+chr(int(binary[x*7:(x+1)*7],2)+0)
		#print('key: '+key+'refracted: '+master)
		return master
	except(ValueError):
		print('Something went wront with the decryption, you may have got a bad packet')
		#print('Binary:' + str(binary))
		#print("masater" + str(master))
		return 1

