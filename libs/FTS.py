"""
	Author: Ross Guarino
	The module for communicating over a network with a PyShare client
"""
from libs import encrypt, utils
import socket, os, stat, math, sys


	
def sendFile(s, fileLocation, key):
	try:
		f = open(fileLocation, 'rb')
		fileSize = os.stat(fileLocation).st_size
		dataSize=1024
		segments = math.ceil(fileSize/dataSize)
		utils.throw(s, str(segments))
		index =0
		while index < segments:
			segment = f.read(dataSize)
			s.send(segment)
			index +=1
		f.close()
	except(socket.error):
		return
	
def recvFile(localData, download, s, fileName, key):
	try:
		location = localData.downloadLocation
	
		f=open(location+fileName, 'wb')
		packetSize =1024
		segments = int(utils.catch(s))
		download.setSize(segments)
		perHash = segments//40
		index =0
		while index < segments :
			if index%perHash == 0:
				download.updateBar()
				f.close()
				f=open(location+fileName, 'ab')
			data = s.recv(packetSize)
			i=0
			while len(data) != packetSize:
				if index == segments-1:
					break
				if i>1000:
					print('Download not finished')
					return
				temp = s.recv(packetSize-len(data))
				data = data+temp
				i=+1
		
			f.write(data)
			download.update()
			index += 1
		f.close()
		localData.finishDownload(download.ID)
		print("Download Finished!")
		
	except(socket.error):
		return