class Station(object):
	
	def __init__(self, MacHash, lts, power,):
		self.MacHash = MacHash
		self.lts = lts
		self.power = power
		
	def getMacHash(self):
		return self.MacHash
		
	def setMacHash(self,MacHash):
		self.Machash = Machash

	def getlts(self):
		return self.lts
		
	def setlts(self, lts):
		self.lts = lts
		
	def getpower(self):
		return self.power
	
	def setpower(self,power):
		self.power = power
		
	def display(self):
		print "MacHash: " + str(self.MacHash) + " Power: " + str(self.power)
