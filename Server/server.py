from calculator import calculator
from databaseserver import databaseserver
from decrypter import Decrypter



class server:
	def __init__(self, timedelay, timecleanup):	
		self.Databaseserver =  databaseserver(timedelay, timecleanup)
		self.Calculator = calculator()
		self.Decrypterserver = Dectrypter()
		self.Databaseserver.run_sql_file("../SQL/createUsers.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createSniffers.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createRanges.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createLocations.sql", self.Databaseserver.db)

	def converttuplestoarray(self, array):
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

	def startcalculator(self):
		while True:
			self.setLocations()
			self.Databaseserver.cleanDB()

	def addtowhitelist(self):
		for machash in self.Databaseserver.getmachash():
			self.Decrypter.addWhitelist()
		


	def startdecrypter(self):
		while self.Decrypterserver.serverRunning():
			#string = raw_input("")
			#test.broadcast(string)
			time.sleep(1)
			if test.server.hasReceived():
				print "\nNEW MESSAGES"
			test.parseAll()
		except:
			test.stopServer()
			raise



if __name__ == "__main__":
	Server = server(4000000, 30)
	Server.setLocations()

	
