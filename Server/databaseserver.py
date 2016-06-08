import MySQLdb, datetime, time

class databaseserver:
	def __init__(self, timedelay, timecleanup):
		self.timedelay = timedelay
		self.timecleanup = timecleanup
		
	def openconnection(self):
		
		
		self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
						 user="root",         # your username
						 passwd="Biertaart",  # your password
						 db="tracking")        # name of the data base

	
		#create cursor object that will allow excution of queries
		self.cur = self.db.cursor()

	def closeconnection(self):
		self.cur.close()
		self.db.close()
	
	def run_sql_file(self, filename):
		self.openconnection()
		file = open(filename, 'r')
		sql = s = " ".join(file.readlines())
		#cursor = connection.cursor()
		self.cur.execute(sql)
		self.db.commit()
		self.closeconnection()
	
	def getRadii(self, id):	
		self.openconnection()
		#timenow = time.strftime('%Y-%m-%d %H:%M:%S')	
		self.cur.execute("SELECT * FROM Ranges WHERE ID = "+ id +" AND Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		for row in self.cur.fetchall():
			#print row[0]
			#print self.cur.fetchall()
			self.closeconnection()
			return self.cur.fetchall()
			
	def getsniffer(self, id):
		self.openconnection()
		self.cur.execute("SELECT * FROM Sniffers WHERE ID = "+ id)
		self.closeconnection()
		return self.cur.fetchall()

	def getmachash(self):
		self.openconnection()
		self.cur.execute("SELECT MacHash FROM Users")
		self.closeconnection()
		return self.cur.fetchall()
	
	def setLocations(self, userid, x, y, z = None ):
		self.openconnection()
		self.cur.execute("SELECT * FROM Locations WHERE Users_ID = "+ str(userid))
		result = self.cur.fetchall()
		if len(result) is 0:
			if z is None:
				self.cur.execute(" INSERT INTO Locations(`Users_ID`, `X`, `Y`, `Time`) VALUES("+ str(userid) +", "+ str(x) +", "+ str(y) +", NOW())  ")
				self.db.commit()
				self.closeconnection()
			else:
				self.cur.execute(" INSERT INTO Locations(`Users_ID`, `X`, `Y`, `Z`, `Time`) VALUES("+ str(userid) +", "+ str(x) +", "+ str(y) +", "+ str(z) +", NOW())  ")
				self.db.commit()
				self.closeconnection()
		else:
			if z is None:
				self.cur.execute("UPDATE Locations SET `X`="+ str(x) +", `Y`="+ str(y) +", `Z`= NULL, `Time`=NOW() WHERE `Users_ID`=" + str(userid))
				self.db.commit()
				self.closeconnection()
			else:
				self.cur.execute("UPDATE Locations SET `X`="+ str(x) +", `Y`="+ str(y) +", `Z`="+ str(z) +", `Time`=NOW() WHERE `Users_ID`=" + str(userid))
				self.db.commit()
				self.closeconnection()
				
	def cleanDB(self):
		self.openconnection()
		query = "DELETE FROM Locations  WHERE Time > DATE_SUB(NOW(), INTERVAL "+ str(self.timecleanup) +" MINUTE)"
		self.cur.execute(query)
		self.db.commit()
		query = "DELETE FROM Ranges WHERE Time > DATE_SUB(NOW(), INTERVAL "+ str(self.timecleanup) +" MINUTE)"
		self.cur.execute(query)
		self.db.commit()
		self.closeconnection()
		
	def getIDs(self):
		self.openconnection()
		self.cur.execute("SELECT ID FROM Users")
		self.closeconnection()
		return self.cur.fetchall()
		
		
	
	def settimedelay(self, timedelay):
		self.openconnection()
		self.timedelay = timedelay
		self.closeconnection()
	
	def settimecleanup(self, timecleanup):
		self.openconnection()
		self.timecleanup = timecleanup
		self.closeconnection()
		
	def getinfoforcalculator(self, userid):
		self.openconnection()
		self.cur.execute("SELECT Sniffers.X, Sniffers.Y, Sniffers.Z Ranges.Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID=Sniffers.ID WHERE Ranges.Users_ID = " + userid + " AND Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		for row in self.cur.fetchall():
			if row[2] == None:
				row[2] = 0
		self.closeconnection()			
		return self.cur.fetchall()
		
	def __getinfoforcalculatorquickversion(self):
		self.openconnection()
		self.cur.execute("Sniffers.X, Sniffers.Y, Sniffers.Z Ranges.Range FROM Ranges INNER JOIN Sniffers ON Ranges.Sniffers_ID=Sniffers.ID INNER JOIN Sniffers ON Sniffers.ID=Users.ID WHERE Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		self.closeconnection()
		return self.cur.fetchall()
		
	def getinfoforcalculatorquickversion(self):
		self.openconnection()	
		self.cur.execute("SELECT Users_ID, X, Y, Z, Ranges.Range FROM Ranges  INNER JOIN Sniffers ON Ranges.Sniffers_ID = Sniffers.ID WHERE Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ str(self.timedelay) +" SECOND) ORDER BY Users_ID")
		self.closeconnection()
		return self.cur.fetchall()
	
	def getusers(self):
		self.openconnection()
		self.cur.execute("SELECT * FROM Users")
		self.closeconnection()
		return self.cur.fetchall()

	def setsniffer(self, id, name,x, y, z = None):
		self.openconnection()
		result = self.cur.execute("SELECT * FROM Sniffers WHERE `ID` = "+ str(id))
		result = self.cur.fetchall()
		if len(result) is 0:
			if z is None:
				self.cur.execute(" INSERT INTO Sniffers(`ID`, `NAME`, `X`, `Y`) VALUES('"+ str(id) +"', '"+ name +"', '"+ str(x) +"', '"+ str(y) +"'")
				self.db.commit()
				self.closeconnection()
			else:
				self.cur.execute(" INSERT INTO Sniffers(`ID`, `NAME`, `X`, `Y`, `Z`) VALUES("+ str(id) +", "+ name +", "+ str(x) +", "+ str(y) +", "+ str(z))
				self.db.commit()
				self.closeconnection()
		else:
			if z is None:
				self.cur.execute("UPDATE Locations SET `NAME`="+ name +", `X`="+ str(x) +", `Y`="+ str(y) +", `Z`= NULL, WHERE `ID`=" + str(id))
				self.db.commit()
				self.closeconnection()
			else:
				self.cur.execute("UPDATE Locations SET `NAME`="+ name +", `X`="+ str(x) +", `Y`="+ str(y) +", `Z`= "+ str(z) +", WHERE `ID`=" + str(id))
				self.db.commit()
				self.closeconnection()

	def setRanges(self, sniffersid, userid, time, ranges ):
		self.openconnection()
		print userid, sniffersid, time, ranges
		result = self.cur.execute("SELECT * FROM Ranges WHERE Users_ID = "+ str(userid)+" AND Sniffers_ID = "+ str(sniffersid))
		result = self.cur.fetchall()
		print "so far so good"
		if len(result) is 0:
			print "result is 0"
			query = "INSERT INTO Ranges(`Users_ID`, `Sniffers_ID`, Ranges.Range, `Time`) VALUES("+ str(userid) +", "+ str(sniffersid) +", "+ str(ranges) +", '"+ time + "')"
			self.cur.execute(query)
			self.db.commit()
			self.closeconnection()
		else:
			print "result is not 0"
			query = "UPDATE Ranges SET Ranges.Range="+ str(ranges) +", Time='"+ time +"' WHERE Users_ID=" + str(userid) +" AND Sniffers_ID="+ str(sniffersid)
			self.cur.execute(query)
			self.db.commit()
			self.closeconnection() 


	def getIDFromMac(self, machash):
		self.openconnection()
		self.cur.execute("SELECT `ID` FROM Users WHERE `MacHash` = '" + str(machash)+"'")
		self.closeconnection()
		return self.cur.fetchall()

	def getSnifferIDFromName(self, name):
		self.openconnection()
		self.cur.execute("SELECT `ID` FROM Sniffers WHERE NAME = '" + str(name)+"'")
		self.closeconnection()
		return self.cur.fetchall()
		
			
		
if __name__ == "__main__":
	obj = databaseserver(400000, 20)
	obj.run_sql_file("../SQL/createSniffers.sql")
	#print obj.getusers()
	#print obj.getinfoforcalculatorquickversion()
	obj.setLocations(1, 6, 5)
	print obj.getinfoforcalculatorquickversion()
	
	
		
