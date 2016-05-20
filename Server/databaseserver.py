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
	
	def run_sql_file(self, filename, connection):
		file = open(filename, 'r')
		sql = s = " ".join(file.readlines())
		cursor = connection.cursor()
		cursor.execute(sql)
		connection.commit()
	
	def getRadii(self, id):	
		#timenow = time.strftime('%Y-%m-%d %H:%M:%S')	
		self.cur.execute("SELECT * FROM Ranges WHERE ID = "+ id +" AND Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		for row in self.cur.fetchall():
			#print row[0]
			#print self.cur.fetchall()
			return self.cur.fetchall()
			
	def getsniffer(self, id):
		self.cur.execute("SELECT * FROM Sniffers WHERE ID = "+ id)
		return self.cur.fetchall()
	
	def setLocations(self, userid, x, y, z = None ):
		self.cur.execute("SELECT * FROM Locations WHERE Users_ID = "+ str(userid))
		result = self.cur.fetchall()
		if len(result) is 0:
			if z is None:
				self.cur.execute(" INSERT INTO Locations(`Users_ID`, `X`, `Y`, `Time`) VALUES("+ str(userid) +", "+ str(x) +", "+ str(y) +", NOW())  ")
				self.db.commit()
			else:
				self.cur.execute(" INSERT INTO Locations(`Users_ID`, `X`, `Y`, `Z`, `Time`) VALUES("+ str(userid) +", "+ str(x) +", "+ str(y) +", "+ str(z) +", NOW())  ")
				self.db.commit()
		else:
			if z is None:
				self.cur.execute("UPDATE Locations SET `X`="+ str(x) +", `Y`="+ str(y) +", `Z`= NULL, `Time`=NOW() WHERE `Users_ID`=" + str(userid))
				self.db.commit()
			else:
				self.cur.execute("UPDATE Locations SET `X`="+ str(x) +", `Y`="+ str(y) +", `Z`="+ str(z) +", `Time`=NOW() WHERE `Users_ID`=" + str(userid))
				self.db.commit()
				
	def cleanDB(self):
		self.cur.execute("DELETE  * FROM Ranges, Locations  WHERE Time > DATE_SUB(NOW(), INTERVAL "+ self.timecleanup +" MINUTES) ")
		self.db.commit()
		
	def getIDs(self):
		self.cur.execute("SELECT ID FROM Users")
		return self.cur.fetchall()
		
	
	def settimedelay(self, timedelay):
		self.timedelay = timedelay
	
	def settimecleanup(self, timecleanup):
		self.timecleanup = timecleanup
		
	def getinfoforcalculator(self, userid):
		self.cur.execute("SELECT Sniffers.X, Sniffers.Y, Sniffers.Z Ranges.Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID=Sniffers.ID WHERE Ranges.Users_ID = " + userid + " AND Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		for row in self.cur.fetchall():
			if row[2] == None:
				row[2] = 0			
		return self.cur.fetchall()
		
	def __getinfoforcalculatorquickversion(self):
		self.cur.execute("Sniffers.X, Sniffers.Y, Sniffers.Z Ranges.Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID=Sniffers.ID INNER JOIN Sniffers ON Sniffers.ID=Users.ID WHERE Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		return self.cur.fetchall()
		
	def getinfoforcalculatorquickversion(self):	
		self.cur.execute("SELECT Users_ID, X, Y, Z, Ranges.Range FROM Ranges  INNER JOIN Sniffers ON Ranges.Sniffers_ID = Sniffers.ID WHERE Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ str(self.timedelay) +" SECOND) ORDER BY Users_ID")
		return self.cur.fetchall()
	
	def getusers(self):
		self.cur.execute("SELECT * FROM Users")
		return self.cur.fetchall()

	def setsniffer(self, id, name,x, y, z = None):
		result = self.cur.execute("SELECT * FROM Sniffers WHERE `ID` = "+ str(id))
		result = self.cur.fetchall()
		if len(result) is 0:
			if z is None:
				self.cur.execute(" INSERT INTO Sniffers(`ID`, `NAME`, `X`, `Y`) VALUES("+ str(id) +", "+ name +", "+ str(x) +", "+ str(y))
				self.db.commit()
			else:
				self.cur.execute(" INSERT INTO Sniffers(`ID`, `NAME`, `X`, `Y`, `Z`) VALUES("+ str(id) +", "+ name +", "+ str(x) +", "+ str(y) +", "+ str(z))
				self.db.commit()
		else:
			if z is None:
				self.cur.execute("UPDATE Locations SET `NAME`="+ name +", `X`="+ str(x) +", `Y`="+ str(y) +", `Z`= NULL, WHERE `ID`=" + str(id))
				self.db.commit()
			else:
				self.cur.execute("UPDATE Locations SET `NAME`="+ name +", `X`="+ str(x) +", `Y`="+ str(y) +", `Z`= "+ str(z) +", WHERE `ID`=" + str(id))
				self.db.commit()

	def setRanges(self, userid, sniffersid, range):
		result = self.cur.execute("SELECT * FROM Ranges WHERE Users_ID = "+ str(userid)+" AND Sniffers_ID = "+ str(sniffersid))
		result = self.cur.fetchall()
		if len(result) is 0:
			self.cur.execute(" INSERT INTO Ranges(`Users_ID`, `Sniffers_ID`, `Range`, `Time`) VALUES("+ str(userid) +", "+ str(sniffersid) +", "+ str(range) +", NOW()")
		else:
			self.cur.execute("UPDATE Ranges SET `Users_ID`="+ str(userid) +", `Sniffers_ID`="+ str(sniffersid) +", `Range`="+ str(range) +", `Time`=NOW() WHERE `Users_ID`=" + str(userid) +" AND Sniffers_ID = "+ str(sniffersid))
			self.db.commit() 
	
	
	
	
			
		
if __name__ == "__main__":
	obj = databaseserver(400000, 20)
	#print obj.getusers()
	print obj.getinfoforcalculatorquickversion()
	obj.setLocations(1, 6, 5)
	
	
		
