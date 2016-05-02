import os, time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from sockserver import SocketServer
 
class Decrypter(object):
 	
 	def __init__(self):
 		rg = Random.new().read
		self.privateKey = RSA.generate(2048)
		self.publicKey = self.privateKey.publickey()
		self.pubkeyStr = self.publicKey.exportKey('PEM')
		self.server = SocketServer(8888,self.pubkeyStr,self.privateKey)
		self.server.start()
	
	def serverRunning(self):
		return self.server.isRunning()
		
	def def addWhitelist(self,MacHash):
		self.server.addWhitelist(MacHash)
		
	def broadcast(self,msg):
		self.server.broadcast(msg)
		
	def stopServer(self):
		pid = os.getpid()
		os.kill(pid,9)
		self.server.join()
		
	def parseAll(self):
		while 1:
			msg = self.server.nextReceived()
			if msg is -1:
				break
			self.parse(msg)
		
	def parse(self, msg):
		print "says: " + msg
		
			
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


