import configparser, os

class personalData():
	"""
	nick-> str(nickname)
	files-> dic(the files shared)
	kill-> bool(wether the server should shutdown or not)
	share-> str(name of the directory shared)
	currentVersion-> tuple(current version)
	"""
	
	
	
	__slots__=('nickName', 'files', 'kill', 'share','currentVersion', 'nodes', \
		'downloads','current', 'downloadLocation', 'totalDownloads', 'config')
	
	def __init__(self):
		"""creates a file directory listing of the shared files. also read from a file about the\
		nickname and other data saved previously about the user"""
		
		settings = configparser.SafeConfigParser(allow_no_value=True)
		list=settings.read('data/settings.cfg')
		if not 'data/settings.cfg' in list:
			print('no configuration file present.. making one')
			self.makeConfigFile(settings)
			share = ['']
			self.nodes = []
		else:
			share, nodes = self.openConfig(settings)
			self.nodes = nodes
		
		
		self.files = self.loadFiles(share)		
		self.share = share
		self.kill= False
		self.downloads = {}
		self.currentVersion = (0,2,1)
		self.totalDownloads = 0
		self.current = 0
		self.config = settings

	def exit(self, IPDatabase):
		config = self.config
		string, dic = IPDatabase.currentConnections()
		preKnown = config.get("UserSettings", 'knownNodes')
		for key in dic.keys():
			if str(dic[key]) not in preKnown:
				preKnown=preKnown+','+str(dic[key])
		
		with open('data/settings.cfg', 'w') as configfile:
			config.write(configfile) 
		
		
	def directoriesShared(self):
		master = ''
		for x in self.share:
			master=master+str(x)+' , '
		if len(master) > 0:
			master = master[:-3]
		
		return master
		
	def makeConfigFile(self, settings):
		settings.add_section('UserSettings')
		settings.set('UserSettings', 'share', '')
		settings.set('UserSettings', 'download', '~/Downloads')
		settings.set('UserSettings', 'nickname', 'Anonymous')
		settings.set('UserSettings', 'knownNodes', 'None')
		self.nickName = 'Anonymous'
		self.downloadLocation = '~/Downloads'
		with open('data/settings.cfg', 'w') as configfile:
			settings.write(configfile)
	
	def openConfig(self, settings):
		if settings.has_section('UserSettings'):
			try:
				self.nickName = settings.get('UserSettings','nickname')
			except(configparser.NoOptionError):
				print('ERROR: [ConfigError] IndexError: Configuration file missing \"nickname\" attribute. Setting to default')
				settings.set('UserSettings', 'nickname', 'Anonymous')
				self.nickName = 'Anonymous'
			
			try:
				nodes = settings.get('UserSettings','knownNodes').split(',')
				if len(nodes) == 1 and nodes[0]=='':
					nodes=[]
			except(configparser.NoOptionError):
				print('ERROR: [ConfigError] IndexError: Configuration file missing \"knownNodes\" attribute. Setting to default')
				settings.set('UserSettings', 'knownNodes', '')
				nodes = []
			
			try:
				share = settings.get('UserSettings', 'share').split(',')
				
			except(configparser.NoOptionError):
				print('ERROR: [ConfigError] IndexError: Configuration file missing \"share\" attribute. Setting to default')
				settings.set('UserSettings', 'share', '')
				share = []
			
			try:
				download = settings.get('UserSettings','download')
				self.downloadLocation = download
			except(configparser.NoOptionError):
				print('ERROR: [ConfigError] IndexError: Configuration file missing \"download\" attribute. Setting to default')
				settings.set("UserSettings", 'download', '~/Downloads')
				self.downloadLocation = '~/Downloads'
			
			with open('data/settings.cfg', 'w') as configfile:
				settings.write(configfile)
			
			return share, nodes
		
		else:
			self.makeConfigFile(settings)
		
	def addFiles(self, newDirectory):
		for root, dirs, files in os.walk(newDirectory):
			for dirr in dirs:
				self.files[root+dirr+'/'] = str('[D]'+dirr)
			for file in files:
				self.files[root+'/'+file] = str('[F]'+file)
		
		current=self.config.get('UserSettings', 'share')
		current=current+' , '+str(newDirectory)
		self.config.set('UserSettings','Share', str(current))
		
		with open('data/settings.cfg', 'w') as configfile:
			self.config.write(configfile)
				
	def loadFiles(self, listOfDirectories):
		fileDic={}

	
		for element in listOfDirectories:
			if element != '':
				for root, dirs, files in os.walk(element):
					for dirr in dirs:
						fileDic[root+'\\'+dirr+'/'] = str('[D]'+dirr)
					for file in files:
						fileDic[root+'/'+file] = str('[F]'+file)
			
		if len(fileDic) == 0:
			print("\nno files loaded. Remember to update the sharing directorys")
	
		return fileDic
	
	def newDownload(self, fileInfo):
		#fileInfo = (filename , filepath , ip)
		ID =self.totalDownloads+1
		self.downloads[ID] = self.download( ID , fileInfo)
		self.totalDownloads+=1
		self.current+=1
		return self.downloads[ID]
	
	def finishDownload(self, ID):
		del self.downloads[ID]
		self.current -= 1

	def currentDownloads(self):
		master="Current Downloads ["+ str(self.current)+'] '+'Total Downloads: '+ str(self.totalDownloads)+'\n'
		for download in self.downloads:
			master= master+str(self.downloads[download])+'\n'
		return master
	
	def helpPrint(self):
		#79 wide
		print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
		print("%Peer-to-peer File Sharing Help[Version: "+str(self.currentVersion[0])+"."+str(self.currentVersion[1])+"."+str(self.currentVersion[2])+"]                            %")
		print("%                                                                             %")
		print('%Commands: \'Connect\', \'Disconnect\', \'Search\', \'Info\', \'Exit\'                  %')
		print('%                                                                             %')
		print('%Connect   -> Manually connect to a new client via IP address                 %')
		print('%Reconnect -> Reconnect to a already connected client                         %')
		print('%Disconnect-> disconnects you from a client with an IP address or Nickname    %')
		print('%Search    -> Search known clients for files                                  %')
		print('%Info      -> Information about your current install and program              %')
		print('%Exit      -> Attempts to exit the program                                    %')
		print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
		
	class download():
		#everythin in Kb
		__slots__=('progressBar','ID', 'progress', 'size', 'ip', 'fileName')
		
		def __init__(self, ID, fileInfo):
			self.fileName = fileInfo[0]
			self.ip = fileInfo[2]
			self.progressBar=''
			self.progress = 0
			self.ID = ID
		
		def setSize(self, size):
			#in Kb
			self.size = size

		def update(self):
			self.progress += 1
		
		def updateBar(self):
			self.progressBar = self.progressBar+'#'
		
		def __str__(self):
			name = self.fileName
			if len(name) > 20:
				name = name[3:10]+'...'
			master= ' '+str(name)+' ('+str(self.progress)+'Kb//'+str(self.size)+'Kb) ['+str(self.progressBar)
			
			while len(master) < 77:
				master=master+' '
			master = master+']'
			return master
			
