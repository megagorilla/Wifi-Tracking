import os, time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from sockserver import SocketServer
 
class Decrypter(object):
 	'''
	the constructor sets an random variable, privatekey to 2048, sets the publickey, sets the public keystring and sets an socketserver object and starts the socketserver
	'''
 	def __init__(self):
 		rg = Random.new().read
		self.privateKey = RSA.generate(2048)
		self.publicKey = self.privateKey.publickey()
		self.pubkeyStr = self.publicKey.exportKey('PEM')
		self.server = SocketServer(8888,self.pubkeyStr,self.privateKey)
		self.server.start()
	'''
	adds given variable machash to the socketserver object by calling socketserver object's addwhitelist function
	'''
	def serverRunning(self):
		return self.server.isRunning()
	'''
	adds given variable machash to the socketserver object by calling socketserver object's addwhitelist function
	'''	
	def addWhitelist(self,MacHash):
		self.server.addWhitelist(MacHash)
		
	def broadcast(self,msg):
		self.server.broadcast(msg)
		
	def stopServer(self):
		pid = os.getpid()
		os.kill(pid,9)
		self.server.join()
		
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


