import os, time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from sockserver import SocketServer
 
class Decrypter(object):
 	'''
	Creates a RSA public and private key and creates and starts a sockserver
	'''
 	def __init__(self):
 		rg = Random.new().read
		self.privateKey = RSA.generate(2048)
		self.publicKey = self.privateKey.publickey()
		self.pubkeyStr = self.publicKey.exportKey('PEM')
		self.server = SocketServer(8888,self.pubkeyStr,self.privateKey)
		self.server.start()

	'''
	returns true is the server is still running
	'''
	def serverRunning(self):
		return self.server.isRunning()

	'''
	adds a MacHash to the whitelist
	'''	
	def addWhitelist(self,MacHash):
		self.server.addWhitelist(MacHash)
		
	'''
	Broadcasts a message to all the clients
	'''
	def broadcast(self,msg):
		self.server.broadcast(msg)
		
	'''
	Kills the server
	'''
	def stopServer(self):
		pid = os.getpid()
		os.kill(pid,9)
		self.server.join()
	
	'''
	Puts the whole buffer in an array and returs that array
	'''
	def parseAll(self):
		toReturn = []
		while 1:
			msg = self.server.nextReceived()
			if msg is -1:
				break
			toReturn.append(msg)
		return toReturn
			
if __name__ == "__main__":
	try:
		test = Decrypter()
		while test.serverRunning():
			#string = raw_input("")
			#test.broadcast(string)
			time.sleep(1)
			if test.server.hasReceived():
				print "\nNEW MESSAGES"
			test.parseAll()		
	except:
		test.stopServer()
		raise


