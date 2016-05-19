import Calculator, Databaseserver

class server:
	def __init__(self):	
		self.Databaseserver =  databaseserver(40, 30)
		self.Calculator = calculator()
		self.Databaseserver.run_sql_file("../SQL/createLocations.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createRanges.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createSniffers.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("../SQL/createUsers.sql", self.Databaseserver.db)

	
	
		

	def setLocation(self):
		ALLRadii =  self.Databaseserver.getinfoforcalculatorquickversion()
		print ALLRadii
		lastforradiiid
		counter = 0
		splitpoints = []
		#splitarray
		for radii in ALLRadii:
			if counter == 0:
				lastforradiiid = radii[0]
				splitpoint[0] = 0
			if lastforradiiid is not radii[0]:
				lastforradiiid = radii[0]
				radii.pop(0)
				splitarray = ALLRadii[ splitpoints[-1]: counter + 1]
				print splitarray
				splitpoints.append(counter)				
				if len(splitarray) > 1:
					calcutedpoint = self.Calculator.calculatepoint(Radii)
					if len(calculatepoint[0]) is 3: 
						self.Databaseserver.setLocations(id,time.strftime('%Y-%m-%d %H:%M:%S'), calculatepoint[0][0], calculatepoint[0][1], calculatepoint[0][2])
					else:
						self.Databaseserver.setLocations(id,time.strftime('%Y-%m-%d %H:%M:%S'), calculatepoint[0][0], calculatepoint[0][1])
						
			else:
				lastforradiiid = radii[0]
				radii.pop(0)
			counter = counter + 1
			if (counter + 1) is len(ALLRadii):
				splitarray = ALLRadii[ splitpoints[-1]: counter + 1]
				print splitarray
				splitpoints.append(counter)				
				if len(splitarray) > 1:
					calcutedpoint = self.Calculator.calculatepoint(Radii)
					if len(calculatepoint[0]) is 3: 
						self.Databaseserver.setLocations(id,time.strftime('%Y-%m-%d %H:%M:%S'), calculatepoint[0][0], calculatepoint[0][1], calculatepoint[0][2])
					else:
						self.Databaseserver.setLocations(id,time.strftime('%Y-%m-%d %H:%M:%S'), calculatepoint[0][0], calculatepoint[0][1])
						
				
				

			
					
	def startcalculator(self):
		while True:
			self.setLocation()
			self.Databaseserver.clean

		
'''	
	def setLocation(self):
		allids = self.Databaseserver.getIDs()
		for id in allids:
			Radii =  self.Databaseserver.getinfoforcalculator(id)
			if len(Radii) >= 2:
				calcutedpoint = self.Calculator.calculatepoint(Radii)
				if len(calculatepoint[0]) = 3: 
					self.Databaseserver.setLocations(id,time.strftime('%Y-%m-%d %H:%M:%S'), calculatepoint[0][0], calculatepoint[0][1])
				else:
					self.Databaseserver.setLocations(id,time.strftime('%Y-%m-%d %H:%M:%S'), calculatepoint[0][0], calculatepoint[0][1], calculatepoint[0][2])
'''	

if __name__ == "__main__":
	Server = server()
	Server.setLocation()
	
