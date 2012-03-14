"""
Author: Ross Guarino
The userIO module for the file sharing program
"""
from libs import encrypt, utils, FTS, parser
import sys, os, socket, threading

def main(IPDatabase, localData):
	print("STARTING USER INTERFACE")
	while True:
		command = str(input('-----------------------------------------------------[' +utils.formatTime()+ ']\n>>>'+localData.nickName+":\\")).lower()
		command, arg1, arg2 = parser.parseCommand(command)
		runCommand(IPDatabase, localData, command, arg1, arg2)
		
def runCommand(IPDatabase, localData, command, arg1, arg2):
		if command == None and arg1 ==None and arg2 == None:
			print('invalid Command or arguments')
		if command == 'connect': #Connect
			if arg1 == None:
				arg1 = input('Enter the IP of the peer you would like to connect to: ')
			setUpConnection(IPDatabase, localData, arg1)
		elif command == 'settings':
			if arg1 == 'changedownload' or arg1 == 'download':
				if arg2 == None:
					arg2 = input("What directory would you like to set the download to? ")
					if arg2 == '' or arg2 =='0':
						return
				if os.path.exsts(os.path.dirname(arg2)):
					localData.downloadLocation = arg2
			if arg1 == None:
				print("-Current Configuration:")
				print("---NickName: "+str(localData.nickName))
				print("---Directories: "+str(localData.directoriesShared()))
				print("---Download: "+localData.downloadLocation)
		elif command == 'disconnect': #Disconnect
			"""
			Disconenct:
			command = 2
			arg1 = 0 -> diconnect from all
			arg1 = str(ip) -> disconnect from just that IP address
			arg1 = -all -> disconnect with everyone
			arg1 = None -> get an index from the user. then use thet index to get an IP and pass that into the function
			"""
			string, connections = IPDatabase.currentConnections()
			if arg1 == None:
				#Ther awas no argument passed
				print(string)
				arg1 = input('Enter the index of the node that you would like to disconenct from: ')
				
				if arg1 == '0':
					return

				elif arg1 == '':
					#disconnect with all
					for id in connections:
						removeConnection( IPDatabase, connections[id])
				
				else:
					try:
						arg1 = int(arg1)
					except(ValueError):
						print('Invalid input please ener an Int')
						return
					
					if arg1 in connections:
						#disconnect with only one
						removeConnection( IPDatabase, connections[arg1])
					else:
						#invalid input
						print("ERROR: IndexError[Index not valid]")
				
			elif arg1 == 'all':
				#the argument was '-all' which means disconnect all
				for id in connections:
					removeConnection(connections[id])
			else:
				if arg1 in connections:
					removeConnections(arg1)
				else:
					print('No such connected IP')
		
		elif command == 'reconnect': #Reconnect
			"""
			reconnect:
			command = 3
			arg1 = str(ip) -> reconnect with just that IP
			arg1 = -all -> reconenct with everone
			arg1 = None -> get an index from the user. reconnect with that IP
			"""
			string, connections = IPDatabase.currentConnections()
			if arg1 == None:
				#passed no arguments
				print(string)
				arg1 = input("ener the index of the peer that you would like to reconnect to: ")
				if arg1  == '':
					#entered empty string -> reconnect all
					for id in connections:
						removeConnection(IPDatabase, connections[id])
						setUpConnection(IPDatabase, localData, connections[id], True)
				
				elif int(arg1) in connections: #need to handle user errors here
					#entered a index
					removeConnection( IPDatabase, connections[int(arg1)])
					setUpConnection(IPDatabase, localData, connections[int(arg1)], True)
				else:
					#did not enter a valid anything
					print("ERROR: IndexError[Index not valid]")
			
	
			elif arg1 == 'all':
				#argument pass was '-all' reconnect all!
				for id in connections:
					removeConnection(IPDatabase, connections[id])
					setUpConnection(IPDatabase, localData, connections[id], True)
			else:
				#they pass an aggument
				removeConnection(IPDatabase, arg1)
				setUpConnection(IPDatabase, localData, arg1, True)

		elif command == 'search': #Search
			"""
			Search:
			Command = 4
			arg1 = str(searchterm) -> search with this search term 
			arg1 = None -> ask the user for a search term 
			"""
			if arg1 == None:
				arg1 = str(input("enter a term to search with: "))
				if len(arg1) < 3:
					print('You much enter a term larger than 3 characters')
					return
				
			
			
			results = search(IPDatabase, arg1)
			totalRes =len(results)
			if totalRes == 0:
				print("There were no results to you search")
				return
			elif totalRes > 50:
				choice=input("There #:]are "+ str(totalRes)+ " total results would you like to display all of them[y/n]")
				if choice == 'y' or choice == 'Y' or choice == "yes":
					printResults(IPDatabase, results, totalRes)
				else: 
					pass 
			
			else:
				printResults(IPDatabase, results, totalRes)
				
		elif command == 'download': #Download
			"""
			Download:
			arg1 = str(search term) -> search with this term
			arg1 = None -> ask the user for a search term
			"""
			
			if arg1 == None:
				arg1 = str(input("Enter a term to search for: "))
				if len(arg1) < 3:
					print('You much enter a term larger than 3 characters')
					return
			
			results = search(IPDatabase, arg1)
			totalRes = len(results)
			if totalRes == 0:
				print("There were no results to you search")
				return
			elif totalRes > 50:
				choice=input("There There "+ str(totalRes)+ " total results would you like to display all of them[y/n]")
				if choice == 'y' or choice == 'Y' or choice == "yes":
					printResults(IPDatabase, results, totalRes)
				else:
					return
					pass 
			
			else:
				printResults(IPDatabase, results, totalRes)
				
			
			index= input("enter the index of the file that you would like to download: ")
			
			if index.lower == 'exit':
				return
			
			try:
				index = int(index)
			except(ValueError):
				print("ERROR: [Index Error] Index not valid")
				return
			if index == 0:
				return
			if index > totalRes:
				print("ERROR: [Index Error] Index out of range")
			
			if results[index][0][:3] == '[D]':
				threading.Thread(target=directoryManager, name='Download manager', args=(IPDatabase, localData, results, index)).start()
			
			else:
				threading.Thread(target=download, name='Download Thread', args=(IPDatabase, localData, results[index])).start()
			#download(IPDatabase, localData, results[index])
		elif command == 'downloads':
			print(localData.currentDownloads())

		elif command == 'info': #Info
			print('PyShare [Version'+str(localData.currentVersion)+']')
			print('Nick : '+localData.nickName)	
			print('Directory shared: '+ str(localData.directoriesShared()))
			print("Files & Directories shared: "+ str(len(localData.files.keys())))
			string, connections = IPDatabase.currentConnections()
			print(string)

		elif command == 'clear': #Clear
			if os.system('clear') == 1:
				os.system('cls')

		elif command == 'help': #Help
			localData.helpPrint()

		elif command == 'exit': #Exit
			print('EXITING...')
			localData.exit(IPDatabase)
			massDisconnect(IPDatabase)
			localData.kill = True
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(('127.0.0.1', 44450))
			temp='--'
			s.send(utils.formatNumber(len(temp)).encode())
			s.send(temp.encode())
			sys.exit()
			
		else:
			print('ERROR: [\'' +command+ '\']  is not a recognized command')
			print(">>> Commands: \'Connect\' , \'Disconnect\' , \'Search\' \n>>> \'Help\' for help.")

def directoryManager(IPDatabase, localData, results, index):
	downloadInfo = results[index]
	path=downloadInfo[1]
	res=[]
	for key in results.keys():
		if path in results[key][1]:
			if results[key][0][:3] == '[D]':
				pass
			else:
				res.append(results[key])
	print('Downloading... There are '+str(len(res))+' files to download')
	for results in res:
		download(IPDatabase, localData, results)
				
	
def printResults(IPDatabase, results, totalRes):
	print('_________________________________________')
	print('Results: '+str(totalRes)+'\nID: Filename:')	
	lastUser = None
	for index in results.keys():
		if lastUser != results[index][2]:
			print('User: '+ str(IPDatabase.getNick(results[index][2])) + ' ('+str(results[index][2])+')') 
			lastUser = results[index][2]
		print('    ['+str(index)+'] '+str(results[index][0][:3])+'  '+str(results[index][0][3:]))

def download(IPDatabase, localData, fileInfo):
	#file info = (filename , filepath , ip)
	ip=fileInfo[2]
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	i=0
	while i<=5:
		try:
			s.connect((ip, 44450))
			break
		except (socket.error):
			print('socket error')
			i+=1
			if i==5:
				return None
	
	if True: 
		utils.throw(s, '-3')
		port = int(utils.catch(s))
		s.close()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, port))
		filePath = encrypt.encrypt(str(fileInfo[1]), IPDatabase.table[ip].key)
		utils.throw(s, filePath)
		download = localData.newDownload(fileInfo)
		
		FTS.recvFile(localData, download, s, fileInfo[0][3:], IPDatabase.table[ip].key)

def sendSearch(IPDatabase, ip, term):
	
	user = IPDatabase.table[ip]
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	i=0
	while i<=5:
		try:
			s.connect((ip, 44450))
			break
		except (socket.error):
			print('socket error')
			i+=1
			if i==5:
				return []
	try:
		temp='-2'
		utils.throw(s, temp)
		
		port = utils.catch(s) #get the new port
		s.close()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ip, int(port))) #Connect
		eTerm = encrypt.encrypt(term, IPDatabase.table[ip].key)
		utils.throw(s, eTerm)
		#Send the term
	
		packets = int(s.recv(4).decode()) #get the total number of packets
		master=''
		index =0
		packetSize = 1024
		while index < packets:
			data= s.recv(packetSize)
			while len(data)< packetSize:
				if index == packets-1:
					break
				temp = s.recv(packetSize-len(data))
				data =data+temp
			master=master+data.decode()
			index+=1
		
		master = encrypt.refract(master, user.key)

		res=[]
		if master=='':
			return []
		for packet in master.split('|'):
				mid = packet.find(",")
				temp=(packet[:mid], packet[mid+1:])
				res.append(temp)
		
		s.close()
		
		return res
	
	except (socket.error):
		print("Connection Failed")
		s.close()
		return []
		
def search(IPDatabase, term):
	"""
	manages the searches
	returns a dictionary that is in the format:
	[index] = ( filename, filepath, ip)
	"""
	
	results = []
	for ip in IPDatabase.table:
		res = sendSearch( IPDatabase, ip, term)
		results.append((res,ip))
	_results= {}
	i=0
	for result in results:
		for index in result[0]:
			i+=1
			# ( filename , filepath , ip)
			_results[i]=(index[0],index[1],result[1])
	return _results
	
def removeConnection(IPDatabase, ip):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	try:
		s.connect((ip, 44450))
		utils.throw(s,'-1')
		s.close()
	except (socket.error):
		pass

	IPDatabase.rmIP(ip)

def setUpConnection(IPDatabase, localData, ip, auto=False):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	i=0
	while i < 5:
		try:
			s.connect((ip, 44450))
			utils.throw(s, '-0')
			break
		except (socket.error):
			i+=1
			if auto == False:
				ip = input("Oops.. the IP that you entered was incorrect or the peer is not responding \nPlease enter a new IP or [0]' to exit: ")
			if auto == True:
				pass
			if ip.lower() == "0":
				return []
			if i >5:
				return []

	try:
		port = utils.catch(s)
		s.close()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		#print('connecting')
		s.connect((ip, int(port)))
		ip =s.getpeername()[0]
		#('making key')
		key = encrypt.genKey(s)
		#print('sending nickname')
		myNick = encrypt.encrypt(localData.nickName,key)
		utils.throw(s, myNick)
		
		#print('receiving nickname')
		data=utils.catch(s)
		nick=encrypt.refract(data, key)
		
		peerList=[]
		data=s.recv(4)
		for i in range(int(data.decode())): 
			peerList.append(encrypt.refract(utils.catch(s),key))
		
		result= IPDatabase.addIP(ip, key, nick)
		if auto == False:
			if result == 0:
				print('IP Table: Added \''+ IPDatabase.table[ip].nick +'\' with IP [' + IPDatabase.table[ip].ip+ '] correctly')
			else:
				print('IP Table: \'' +IPDatabase.table[ip].nick+'\' Already in table')
				s.close()
				return peerList
		s.close()
			
	except(socket.error):
		if auto== False:
			print('Connection failded: not adding new node')
		return []
				
def massDisconnect(IPDatabase):
	string, connections = IPDatabase.currentConnections()
	for id in connections:
		removeConnection(IPDatabase, connections[id])
		
		
		
		