import MySQLdb, datetime, time

class databaseserver:
	'''
	The constructor of the databaserver class sets the timedelay for when information in the database is not legit anymore and sets an timer for when the database needs to be cleaned
	'''
	def __init__(self, timedelay, timecleanup):
		self.timedelay = timedelay
		self.timecleanup = timecleanup
		
	'''
	opens an connection with an database using an database object as property it also initilises an cursor object for the database
	'''	
	def openConnection(self):
		self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
						 user="root",         # your username
						 passwd="Biertaart",  # your password
						 db="tracking")        # name of the data base
		#create cursor object that will allow excution of queries
		self.cur = self.db.cursor()

	'''
	closes the connection with the database deleting the database object as property it also deletes the cursor object for the database
	'''
	def closeconnection(self):
		self.cur.close()
		self.db.close()

	'''
	Runs an external sql file given within the parameters of the function
	'''
	def run_sql_file(self, filename):
		self.openConnection()
		file = open(filename, 'r')
		sql = s = " ".join(file.readlines())
		#cursor = connection.cursor()
		self.cur.execute(sql)
		self.db.commit()
		self.closeconnection()
	
	'''
	returns all Radii coupled to an userid given in the parameters
	'''
	def getRadii(self, id):	
		self.openConnection()
		#timenow = time.strftime('%Y-%m-%d %H:%M:%S')	
		self.cur.execute("SELECT * FROM Ranges WHERE ID = "+ id +" AND Time > DATE_SUB(NOW(), INTERVAL "+ self.timedelay +" SECONDS) ")
		for row in self.cur.fetchall():
			#print row[0]
			#print self.cur.fetchall()
		toreturn = self.cur.fetchall()
		self.closeconnection()
		return toreturn

	'''
	returns all information from a sniffer coupled to an id given in the parameters
	'''
	def getSniffer(self, id):
		self.openConnection()
		self.cur.execute("SELECT * FROM Sniffers WHERE ID = "+ id)
		toreturn = self.cur.fetchall()
		self.closeconnection()
		return toreturn

	'''
	returns all machashes from all users
	'''
	def getMacHash(self):
		self.openConnection()
		self.cur.execute("SELECT MacHash FROM Users")
		toreturn = self.cur.fetchall()
		self.closeconnection()
		return toreturn

	'''
	sets a 2d locations or a 3d location
	'''
	def setLocations(self, userid, x, y, z = None ):
		self.openConnection()
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

	'''
	deletest all information from location and ranges which is older then the property timecleanup
	'''			
	def cleanDB(self):
		self.openConnection()
		query = "DELETE FROM Locations  WHERE Time > DATE_SUB(NOW(), INTERVAL "+ str(self.timecleanup) +" MINUTE)"
		self.cur.execute(query)
		self.db.commit()
		query = "DELETE FROM Ranges WHERE Time > DATE_SUB(NOW(), INTERVAL "+ str(self.timecleanup) +" MINUTE)"
		self.cur.execute(query)
		self.db.commit()
		self.closeconnection()

	'''
	gets all id's from all Users 
	'''	
	def getIDs(self):
		self.openConnection()
		self.cur.execute("SELECT ID FROM Users")
		toreturn = self.cur.fetchall()
		self.closeconnection()
		return toreturn
		
	'''
	sets property timedelay
	'''	
	def settimedelay(self, timedelay):
		self.timedelay = timedelay

	'''
	sets property timecleanup
	'''	
	def setCleanupTime(self, timecleanup):
		self.timecleanup = timecleanup
		
	'''
	deprecated function
	'''	
	def getInfoForCalculator(self):
		self.openConnection()	
		self.cur.execute("SELECT Users_ID, X, Y, Z, Ranges.Range FROM Ranges  INNER JOIN Sniffers ON Ranges.Sniffers_ID = Sniffers.ID WHERE Ranges.Time > DATE_SUB(NOW(), INTERVAL "+ str(self.timedelay) +" SECOND) ORDER BY Users_ID")
		toreturn = self.cur.fetchall()
		self.closeconnection()
		return toreturn

	'''
	returns all machashes from all users
	'''
	def getUsers(self):
		self.openConnection()
		self.cur.execute("SELECT * FROM Users")
		toreturn = self.cur.fetchall()
		self.closeconnection()
		return toreturn

	'''
	sets sniffer either 2d or 3d into the database wheter z is filled in or not
	'''
	def setSniffer(self, id, name,x, y, z = None):
		self.openConnection()
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
	
	'''
	sets range
	'''
	def setRanges(self, sniffersid, userid, time, ranges ):
		self.openConnection()
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

	'''
	returns userid based on given machash
	'''
	def getIDFromMac(self, machash):
		self.openConnection()
		self.cur.execute("SELECT `ID` FROM Users WHERE `MacHash` = '" + str(machash)+"'")
		toreturn = self.cur.fetchall()
		self.closeconnection()
		return toreturn

	'''
	returns snifferid based on given sniffername
	'''
	def getSnifferIDFromName(self, name):
		self.openConnection()
		self.cur.execute("SELECT `ID` FROM Sniffers WHERE NAME = '" + str(name)+"'")
		toreturn = self.cur.fetchall()
		self.closeconnection()
		return toreturn
		
			
		
if __name__ == "__main__":
	obj = databaseserver(400000, 20)
	obj.run_sql_file("../SQL/createSniffers.sql")
	obj.setLocations(1, 6, 5)
	print obj.getUsers()
	
	
		
