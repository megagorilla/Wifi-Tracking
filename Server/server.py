from calculator import calculator
from databaseserver import databaseserver
from decrypter import Decrypter
from datetime import datetime
import sys, os, time


class server:
	'''
	Constructor of the server class
	This creates a new databaseserver object, a new calculator object and a Decrypter object
	It checks if all of the tables are created in the database
	args:
	timedelay: The maximum age in seconds a range can be for usage in the calculator
	timecleanup: The maximum age of a database entry in the Range table in minutes
	return: NAN
	'''
	def __init__(self, timedelay, timecleanup):	
		self.Databaseserver =  databaseserver(timedelay, timecleanup)
		self.Calculator = calculator()
		self.Decrypterserver = Decrypter()
		self.Databaseserver.run_sql_file("../SQL/createUsers.sql")
		self.Databaseserver.run_sql_file("../SQL/createSniffers.sql")
		self.Databaseserver.run_sql_file("../SQL/createRanges.sql")
		self.Databaseserver.run_sql_file("../SQL/createLocations.sql")

	'''
	Converts 
	'''
	def convertTuplesToArray(self, tple):
		arraywitharray = []
		for tupleinarray in tple:
			arraywitharray.append(list(tupleinarray))
		return arraywitharray

	'''
	Get the raddi of every avalabile user with every avalible sniffer and then uses that too calculate either a 2d or 3d position and to parse that towards the database
	'''
	def setLocations(self):
		ALLRadiiTuple =  self.Databaseserver.getInfoForCalculator()
		ALLRadii = self.convertTuplesToArray(ALLRadiiTuple)
		lastRadiiID = 0
		counter = 0
		splitPoints = []
		splitArray = []
		calcArray = []
		for radii in ALLRadii:
			if counter == 0:
				lastRadiiID = radii[0]
				splitPoints.append(0)
			if lastRadiiID != radii[0]:
				dataBaseId = lastRadiiID
				lastRadiiID = radii[0]
				radii.pop(0)
				splitArray = ALLRadii[ splitPoints[-1]: counter]
				for splitter in splitArray:
					if splitter[2] is None:
						splitter.pop(2)
				splitPoints.append(counter)
				counter = counter + 1				
				if len(splitArray) > 1:
					calculatedPoint = self.Calculator.calculatePoint(splitArray)
					if len(calculatedPoint[0]) is 3: 
						self.Databaseserver.setLocations(dataBaseId, calculatedPoint[0][0], calculatedPoint[0][1], calculatedPoint[0][2])
					else:
						self.Databaseserver.setLocations(dataBaseId, calculatedPoint[0][0], calculatedPoint[0][1])
						
			else:	
				lastRadiiID = radii[0]
				radii.pop(0)
				
			if (counter) == len(ALLRadii):
				dataBaseId = lastRadiiID
				splitArray = ALLRadii[ splitPoints[-1]: counter + 1]
				splitPoints.append(counter)
				for splitter in splitArray:
					if splitter[2] is None:
						splitter.pop(2)				
				if len(splitArray) > 1:
					calculatedPoint = self.Calculator.calculatedPoint(splitArray)
					if len(calculatedPoint[0]) is 3: 
						self.Databaseserver.setLocations(dataBaseId, calculatedPoint[0][0], calculatedPoint[0][1], calculatedPoint[0][2])
					else:
						self.Databaseserver.setLocations(dataBaseId, calculatedPoint[0][0], calculatedPoint[0][1])
			counter = counter + 1
	'''
	runs the setlocations method
	'''
	def runCalculator(self):
		self.setLocations()
		self.Databaseserver.cleanDB()
		
	'''
	adds machashes to the snifferwhitelist
	'''
	def addToWhitelist(self):
		for machash in self.Databaseserver.getMacHash():
			self.Decrypterserver.addWhitelist(machash[0])
			
	'''
	Parse the information gained from the sniffer to an array and then that gets parsed into the database
	'''
	def parseSnifferToArray(self, Sniffer):
		returnarray = []
		for element in Sniffer:
			element = element.split(';')
			print element
			snifferID = self.Databaseserver.getSnifferIDFromName(element[0])[0][0]
			userID = self.Databaseserver.getIDFromMac(element[1])[0][0]
			lts = element[2]
			power = self.Calculator.convertPowerToRange(float(element[3]))
			power = abs(power) * 4
			self.Databaseserver.setRanges(snifferID,userID,lts,power)
		
	'''
	adds machashes to whitelist and then continuesly adds new snifferinformation and locations to the database
	'''
	def startserver(self):
		self.addToWhitelist()
		#try:
		while self.Decrypterserver.serverRunning():
			time.sleep(1)
			self.parseSnifferToArray(self.Decrypterserver.parseAll())
			self.runCalculator()
			print "still rummming"
	
	
		'''except Exception as x:		
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			self.Decrypterserver.stopServer()
			raise'''



'''
The main mostly used for testing purposes
'''
if __name__ == "__main__":
	Server = server(4000000, 30)
	#try:
	'''test =  Server.parseSnifferToArray(["sniff#1;91abea155fdf14c519923f0c512814e373d997c037aea13c64f89c450796c95d;2016-05-20 14:33:18;20"])
	print test
	Server.setLocations()'''
	Server.startserver()
	'''except Exception as x:		
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		Server.Decrypterserver.stopServer()
		raise'''
	
