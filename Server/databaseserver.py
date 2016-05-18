import MySQLdb, datetime, time

class databaseserver:
	def __init__(self, timedelay, timecleanup):
		self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
						 user="root",         # your username
						 passwd="Biertaart",  # your password
						 db="tracking")        # name of the data base

		
		#create cursor object that will allow excution of queries
		self.cur = db.cursor()
		self.timedelay = timedelay
		self.timecleanup = timecleanup
	
	def run_sql_file(filename, connection):
		file = open(filename, 'r')
		sql = s = " ".join(file.readlines())
		cursor = connection.cursor()
		cursor.execute(sql)
		connection.commit()
	
	def getRadii(self, id):	
		#timenow = time.strftime('%Y-%m-%d %H:%M:%S')	
		self.cur.execute ("SELECT * FROM Ranges WHERE ID = "+ id +" AND Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		for row in self.cur.fetchall():
			#print row[0]
			#print self.curfetchall()
			return self.curfetchall()
			
	def getsniffer(self, id):
		self.cur.execute ("SELECT * FROM Sniffers WHERE ID = "+ id)
		return self.curfetchall()
	
	def setLocations(self, userid,time, x, y, z = None ):
		self.cur.excute ("SELECT  FROM Locations WHERE Users_ID = "+ userid)
		result = self.cur.fetchall()
		if len(result) is 0:
			if z is None:
				self.cur.excute (" INSERT INTO Locations(`Users_ID`, `X`, `Y`, `Time`) VALUES("+ userid +", "+ x +", "+ y +", "+ time +")  ")
				self.db.commit()
			else
				self.cur.excute (" INSERT INTO Locations(`Users_ID`, `X`, `Y`, `Z`, `Time`) VALUES("+ userid +", "+ x +", "+ y +", "+ z +", "+ time +")  ")
				self.db.commit()
		else:
			if z is None:
				self.cur.excute (" Update INTO Locations(`Users_ID`, `X`, `Y`, `Time`) VALUES("+ userid +", "+ x +", "+ y +", "+ time +")WHERE Users_ID = " + userid)
				self.db.commit()
			else
				self.cur.excute (" Update INTO Locations(`Users_ID`, `X`, `Y`, `Z`, `Time`) VALUES("+ userid +", "+ x +", "+ y +", "+ z +", "+ time +") WHERE Users_ID = " + userid)
				self.db.commit()
				
	def cleanDB(self):
		self.cur.execute ("DELETE  * FROM Ranges, Locations  WHERE Time > DATE_SUB(NOW(), INTERVAL "+ self.timecleanup +" MINUTES) ")
		self.db.commit()
		
	def getIDs(self):
		self.cur.execute ("SELECT ID FROM Users)
		return self.curfetchall()
		
	
	def settimedelay(self, timedelay):
		self.timedelay = timedelay
	
	def settimecleanup(self, timecleanup):
		self.timecleanup = timecleanup
		
	def getinfoforcalculator(self, userid):
		self.cur.execute ("SELECT Sniffers.X, Sniffers.Y, Sniffers.Z, Ranges.Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID=Sniffers.ID WHERE Ranges.Users_ID = " + userid + " AND Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		for row in self.cur.fetchall():
			if row[2] == None:
				row[2] = 0			
		return self.curfetchall()
		
	def __getinfoforcalculatorquickversion(self):
		self.cur.excute ("Sniffers.X, Sniffers.Y, Sniffers.Z, Ranges.Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID=Sniffers.ID INNER JOIN Sniffers ON Sniffers.ID=Users.ID WHERE Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		
	def getinfoforcalculatorquickversion(self):	
		self.cur.excute ("SELECT Users_ID, X, Y, Z, Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID = Sniffers.ID ORDER BY Users_ID AND Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS)")
			
		
if __name__ == "__main__":
	
	
		
