"""
Author: Ross Guarino
The host module for PyShare, a peer to peer file sharing program
"""
from libs import encrypt, utils, FTS
import sys, threading, socket, math

def main(IPDatabase, localData):
	"""
	The main loop of the host thread
	"""
	print("STARTING HOST SERVICES")
	HOST= ''
	PORT= 44450
	#socket.setdefaulttimeout(1)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	while True:
		#print('SERVER>> listening')
		s.listen(1)
		conn, addr = s.accept()
		#print('SERVER>> accepted')
		data=utils.catch(conn)
		
		if localData.kill == True:
			s.close()
			return
		#print('SERVER>> received : '+ str(data))
		if(data=='-0'): #new connection
			handleConnection(IPDatabase, localData, conn, addr)
		elif(data=='-1'): #disconnect
			handleDisconnect(IPDatabase, addr)
		elif(data=='-2'): #search
			#routing.route(IPDatabse, localData, conn, addr)
			handleSearch(IPDatabase, localData, conn, addr)
		elif(data == '-3'): #download
			threading.Thread(target=handleDownload, name='Host Thread', args=(IPDatabase, conn, addr)).start()
			
def handleConnection(IPDatabase, localData, ms, addr):
	try:
		c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		c.bind(('', 0))
		
		port = str(c.getsockname()[1])
		utils.throw(ms, port)
		c.listen(1)
		s, addr = c.accept()
		
		key = encrypt.genKey(s, 'RECV')
		
		#print('receiving nickname')
		data=utils.catch(s)
		nick=encrypt.refract(data, key)
		
		myNick = encrypt.encrypt(localData.nickName,key)
		utils.throw(s, myNick)
		#print('sending connected nodes')
		master, connections = IPDatabase.currentConnections()
		s.send(utils.formatNumber(len(connections)).encode())
		for ip in connections:
			element = encrypt.encrypt( connections[ip], key)
			utils.throw(s , element)
		
		IPDatabase.addIP(addr[0], key, nick)
		
	except(socket.error):
		pass

def handleDisconnect(IPDatabase, addr):
	IPDatabase.rmIP(addr[0])
	
def handleDownload(IPDatabase, ms, addr):
	try:
		user = IPDatabase.table[addr[0]]
		c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		c.bind(('', 0))
		port = str(c.getsockname()[1])
		utils.throw(ms, str(port))
		c.listen(1)
		c, addr = c.accept()
		
		fileLocation = encrypt.refract(utils.catch(c), user.key)
		
		FTS.sendFile(c, fileLocation, user.key)
	
	except(socket.error):
		return
	
def handleSearch(IPDatabase, localData, ms, addr):
	user = IPDatabase.table[addr[0]]
	c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	c.bind(('', 0))
	port = str(c.getsockname()[1])
	utils.throw(ms, port)
	c.listen(1)
	s, addr = c.accept()
	
	term = encrypt.refract( utils.catch(s) , user.key)
	master=''
	for key in localData.files.keys():
		try:
			if term.lower() in localData.files[key].lower() or term.lower() in key.lower():
				master= master+localData.files[key]+','+key+"|"
		except UnicodeEncodeError:
			pass
	if len(master) >0:
		master=master[:-1]
	
	master=encrypt.encrypt(master, user.key)
	packetSize=1024
	segments = math.ceil(len(master)/packetSize)
	s.send(utils.formatNumber(segments).encode())
	position=0
	index=0
	while index<segments:
		segment=master[position:position+packetSize]
		s.send(segment.encode())
		position+=packetSize
		index+=1
	
	