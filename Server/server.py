import calculator, databaseserver, time

class server:
	def __init__(self, timedelay):
	
		self.Calculator = calculator()
		self.Databaseserver =  databaseserver(20, 30)
		self.Databaseserver.run_sql_file("createLocations.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("createRanges.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("createSniffers.sql", self.Databaseserver.db)
		self.Databaseserver.run_sql_file("createUsers.sql", self.Databaseserver.db)
	
	
	
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

	def setLocation(self):
		ALLRadii =  self.Databaseserver.getinfoforcalculatorquickversion(id)
		lastforradiiid
		counter = 0
		splitpoints
		#splitarray
		for radii in ALLRadii:
			if lastforradiiid != radii[0]:
				lastforradiiid = radii[0]
				radii.pop(0)
				splitarray = radii[ splitpoints[-1]: counter + 1 ]
				splitpoints.append(counter)				
				if len(splitarray) >= 2:
					calcutedpoint = self.Calculator.calculatepoint(Radii)
					if len(calculatepoint[0]) = 3: 
						self.Databaseserver.setLocations(id,time.strftime('%Y-%m-%d %H:%M:%S'), calculatepoint[0][0], calculatepoint[0][1])
					else:
						self.Databaseserver.setLocations(id,time.strftime('%Y-%m-%d %H:%M:%S'), calculatepoint[0][0], calculatepoint[0][1], calculatepoint[0][2])
			else:
				lastforradiiid = radii[0]
				radii.pop(0)
			counter += 1
			
					
	def startcalculator(self)
		while True:
			self.setLocation()
			self.Databaseserver.clean
	