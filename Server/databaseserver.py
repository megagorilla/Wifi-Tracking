import MySQLdb, datetime, time

class databaseserver:
	def __init__(self, timedelay, timecleanup):
		self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
						 user="root",         # your username
						 passwd="Biertaart",  # your password
						 db="tracking")        # name of the data base

		
		#create cursor object that will allow excution of queries
		self.cur = self.db.cursor()
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
			#print self.cur.fetchall()
			return self.cur.fetchall()
			
	def getsniffer(self, id):
		self.cur.execute ("SELECT * FROM Sniffers WHERE ID = "+ id)
		return self.cur.fetchall()
	
	def setLocations(self, userid,time, x, y, z = None ):
		self.cur.excute ("SELECT * FROM Locations WHERE Users_ID = "+ userid)
		result = self.cur.fetchall()
		if len(result) is 0:
			if z is None:
				self.cur.excute (" INSERT INTO Locations(`Users_ID`, `X`, `Y`, `Time`) VALUES("+ userid +", "+ x +", "+ y +", NOW())  ")
				self.db.commit()
			else:
				self.cur.excute (" INSERT INTO Locations(`Users_ID`, `X`, `Y`, `Z`, `Time`) VALUES("+ userid +", "+ x +", "+ y +", "+ z +", NOW())  ")
				self.db.commit()
		else:
			if z is None:
				self.cur.excute (" Update INTO Locations(`Users_ID`, `X`, `Y`, `Time`) VALUES("+ userid +", "+ x +", "+ y +", NOW())WHERE Users_ID = " + userid)
				self.db.commit()
			else:
				self.cur.excute (" Update INTO Locations(`Users_ID`, `X`, `Y`, `Z`, `Time`) VALUES("+ userid +", "+ x +", "+ y +", "+ z +", NOW()) WHERE Users_ID = " + userid)
				self.db.commit()
				
	def cleanDB(self):
		self.cur.execute ("DELETE  * FROM Ranges, Locations  WHERE Time > DATE_SUB(NOW(), INTERVAL "+ self.timecleanup +" MINUTES) ")
		self.db.commit()
		
	def getIDs(self):
		self.cur.execute ("SELECT ID FROM Users")
		return self.cur.fetchall()
		
	
	def settimedelay(self, timedelay):
		self.timedelay = timedelay
	
	def settimecleanup(self, timecleanup):
		self.timecleanup = timecleanup
		
	def getinfoforcalculator(self, userid):
		self.cur.execute ("SELECT Sniffers.X, Sniffers.Y, Sniffers.Z Ranges.Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID=Sniffers.ID WHERE Ranges.Users_ID = " + userid + " AND Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		for row in self.cur.fetchall():
			if row[2] == None:
				row[2] = 0			
		return self.cur.fetchall()
		
	def __getinfoforcalculatorquickversion(self):
		self.cur.execute("Sniffers.X, Sniffers.Y, Sniffers.Z Ranges.Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID=Sniffers.ID INNER JOIN Sniffers ON Sniffers.ID=Users.ID WHERE Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		return self.cur.fetchall()
		
	def getinfoforcalculatorquickversion(self):	
		self.cur.execute("SELECT Users_ID, X, Y, Z, 'Range' FROM Ranges  INNER JOIN Sniffers ON Ranges.Sniffers_ID = Sniffers.ID WHERE Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ str(self.timedelay) +" SECOND) ORDER BY Users_ID")
		return self.cur.fetchall()

	def getusers(self):
		self.cur.execute("SELECT * FROM Users")
		return self.cur.fetchall()
	
			
		
if __name__ == "__main__":
	obj = databaseserver(50, 20)
	print obj.getusers()
	print obj.getinfoforcalculatorquickversion()
	
	
		
