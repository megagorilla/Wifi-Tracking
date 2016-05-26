from calculator import calculator
from databaseserver import databaseserver
from decrypter import Decrypter
from datetime import datetime
import sys, os


class server:
	def __init__(self, timedelay, timecleanup):	
		self.Databaseserver =  databaseserver(timedelay, timecleanup)
		self.Calculator = calculator()
		self.Decrypterserver = Decrypter()
		self.Databaseserver.run_sql_file("../SQL/createUsers.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createSniffers.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createRanges.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createLocations.sql", self.Databaseserver.db)

	def convertTuplesToArray(self, array):
		arraywitharray = []
		for tupleinarray in array:
			arraywitharray.append(list(tupleinarray))
		return arraywitharray

	def setLocations(self):
		ALLRadiiTuple =  self.Databaseserver.getinfoforcalculatorquickversion()
		ALLRadii = self.converttuplestoarray(ALLRadiiTuple)
		lastforradiiid = 0
		counter = 0
		splitpoints = []
		splitarray = []
		calcarray = []
		for radii in ALLRadii:
			if counter == 0:
				lastforradiiid = radii[0]
				splitpoints.append(0)
			if lastforradiiid != radii[0]:
				databaseid = lastforradiiid
				lastforradiiid = radii[0]
				radii.pop(0)
				splitarray = ALLRadii[ splitpoints[-1]: counter]
				for splitter in splitarray:
					if splitter[2] is None:
						splitter.pop(2)
				splitpoints.append(counter)
				counter = counter + 1				
				if len(splitarray) > 1:
					calculatepoint = self.Calculator.calculatepoint(splitarray)
					if len(calculatepoint[0]) is 3: 
						self.Databaseserver.setLocations(databaseid, calculatepoint[0][0], calculatepoint[0][1], calculatepoint[0][2])
					else:
						self.Databaseserver.setLocations(databaseid, calculatepoint[0][0], calculatepoint[0][1])
						
			else:	
				lastforradiiid = radii[0]
				radii.pop(0)
				
			if (counter) == len(ALLRadii):
				databaseid = lastforradiiid
				splitarray = ALLRadii[ splitpoints[-1]: counter + 1]
				splitpoints.append(counter)
				for splitter in splitarray:
					if splitter[2] is None:
						splitter.pop(2)				
				if len(splitarray) > 1:
					calculatepoint = self.Calculator.calculatepoint(splitarray)
					if len(calculatepoint[0]) is 3: 
						self.Databaseserver.setLocations(databaseid, calculatepoint[0][0], calculatepoint[0][1], calculatepoint[0][2])
					else:
						self.Databaseserver.setLocations(databaseid, calculatepoint[0][0], calculatepoint[0][1])
			counter = counter + 1

	def runcalculator(self):
		while True:
			self.setLocations()
			self.Databaseserver.cleanDB()

	def addTowWitelist(self):
		for machash in self.Databaseserver.getmachash():
			self.Decrypter.addWhitelist(machash)
	
	def parseArrayToDatabase(self, Array):
		for element in Array:
			self.Databaseserver.setRanges(element[1], element[0], element[2], element[3])	
		
					
		
	def parseSnifferToArray(self, Sniffer):
		counter = 0
		returnarray = []
		for element in Sniffer:
			#print split
			#print element
			element = element.split(';')
			#print "split  %s" % element
			#print element[0]
			element0 = self.Databaseserver.getSnifferIDFromName(element[0])
			returnarray.append([])
			returnarray[counter].append(element0[0][0])
			print "dont element 0"
			element1 = self.Databaseserver.getIDFromMac(element[1])
			returnarray[counter].append(element1[0][0])
			print "dont element 1"
			returnarray[counter].append(datetime.strptime(element[2], '%Y-%m-%d %H:%M:%S'))
			#returnarray[counter].append(element[2])
			print "dont element 2"	
			returnarray[counter].append(self.Calculator.convertPowerToRange(float(element[3])))
			print "dont element 3"
			print "done array  %s" % returnarray
			counter = counter + 1

		return returnarray
		
		

	def startserver(self):
		self.Decrypterserver.addtowhitelist()
		try:
			while self.Decrypterserver.serverRunning():
				time.sleep(1)
				'''
				#if test.server.hasReceived():
					#print "NEW MESSAGES"
				'''
				self.parseArrayToDatabase(self.parseSnifferToArray(self.Decrypterserver.parseAll()))
				self.runcalculator()
	
	
		except:
			Decrypterserver.stopServer()
			raise



if __name__ == "__main__":
	Server = server(4000000, 30)
	try:
		test =  Server.parseSnifferToArray(["sniffer1;08:00:27:18:15:a0;2016-05-20 14:33:18;15"])
		print test
		Server.parseArrayToDatabase(test)
		Server.setLocations()
	except Exception as x:		
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		Server.Decrypterserver.stopServer()
		raise
	
