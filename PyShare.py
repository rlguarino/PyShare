"""
	PyShare
	Author: Ross Guarino (www.github.com/EosStyx)
	
	Peer to peer file sharing program that operates without a central server.
	Writen in python3 
"""
from libs import host, user, networkStorage, personalData
import threading, sys, os

def start():
	print("Welcome to PyShare")
	if sys.version_info[:2] < (3,0):
		raise "must use python 3.x"
	if sys.platform.startswith('linux'):
		platform = 'linux'
	elif sys.platform.startswith('win'):
		platform = 'windows'
	else:
		raise 'windows or linux required'
	
	print("checking config...    ", end='')
	sys.stdout.flush()
	localData = personalData.personalData()
	print('[Done]')
	sys.stdout.flush()
	print('Starting Database...       ',end='')
	sys.stdout.flush()
	IPDatabase = networkStorage.nodeDatabase()
	for nodes in localData.nodes:
		threading.Thread(target=user.setUpConnection, name='Host Thread', args=(IPDatabase, localData, nodes, True)).start()
	print("[Done]")
	

	run(IPDatabase, localData)
	
	
def run(IPDatabase, localData):
	hostThread = threading.Thread(target=host.main, name='Host Thread', args=(IPDatabase, localData))
	hostThread.start()
	#start the server and client threads main loop.
	#may restart them if needed
	userThread = threading.Thread(target=user.main, name='User Thread',args=(IPDatabase, localData))
	userThread.start()
start()