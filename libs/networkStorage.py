"""
Network module for the file sharing program
Stores known IP addresses
Author: Ross Guarino
"""

class nodeDatabase():
	"""
	The data structre for storing connected nodes/peers/connections
	"""
	__slots__=('numOfConnections' , 'table' , 'nick')
	
	def __init__(self):
		self.numOfConnections = 0
		self.table={}
		
	def __str__(self):
		result = "IPTABLE\n ------------------------------------ \n"
		result = result + "Number of connections: " +str(self.numOfConnections)+"\n"
		for ip in table.keys():
			result = result + "|" + str(ip) +"Nickname: " + str(table[ip].nick) + " ~ Number of files: "+ table[ip].num+ "|\n"
		result = result + "------------------------------------"
		return result
		
	def checkIP(self, ip):
		"""
		checkIP: int(ip) -> bool
		Checks to see if the IP is in the table"""
		
		return ip in self.table
	
	def getIP(self, ip):
		"""
		getIP: int(ip) -> class(connection)/None
		return the conenction object for the IP address if there is one
		return None if the IP is not in table"""
		if self.checkIP(ip):
			return self.table[ip]
		else:
			return None
	def getNick(self, ip):
		if self.checkIP(ip):
			return self.table[ip].nick
		else:
			return 'None'
	def addIP(self, ip, key = None, nickName = 'Anonymous'):
		"""
		addConnection: int(ip), str(key)/None , str(nickName) -> int
		adds a new connection to the table in the form of a conenction object
		if the ip is alread in the table then do nothing and return 1"""
		if not self.checkIP(ip):
			self.table[ip] = self.connection(ip, key, nickName)
			self.numOfConnections+=1
			return 0
		else:
			return 1

	def rmIP(self, ip):
		"""
		rmConenction: int -> int
		removes the connection object in the table
		if there no object in the table already do nothing"""
		if self.checkIP(ip):
			del self.table[ip]
			return 0
		else:
			return 1

	def currentConnections(self):
		"""
		Returns a string representation of the current connections along with a dictioonary that represents the connects too
		"""
		connections={}
		i=1
		master ="Current Connections:\n    ID: CLIENT:        Nickname: \n"
		
		for ip in self.table:
			connections[i] = ip
			master=master+"    ["+str(i)+'] '+str(ip)+'  '+self.table[ip].nick+'\n'
			i+=1
		
		return master,connections
	
		
			
	class connection(object):
		__slots__=('ip', 'nick' , 'key')
		
		def __init__(self, ip = None, key = None, nick = None):
			self.ip = ip
			self.nick = nick
			self.key = key
		
		def __str__(self):
			return 'IP: \''+ str(self.ip) + "\'  key: \'"+str(self.key)+"\'  nick:  "+str(self.nick)
		
		def setIP(self, ip):
			self.ip = ip
			
		def setNick(self, nick):
			self.nick = nick
			
		def setKey(self, key):
			self.key = key
		
