import re, time
class textreader:
	def __init__(self, textfile):
		f = open(textfile, 'r')
		self.errorWords = ["BSSID", "WPA2", "WPA", "Elapsed:", "[J[1;1H" , "[0m[2J[?25l[2J", "[1;1H", "OPN", "WEP","\x1b[J\x1b[?25h"]
		self.__parseAerodumpTooServer(f)
		
		
	
		
	def __parseAerodumpTooServer(self, textfile):
		for line in textfile:
			self.__parser(line)

	def __parser(self,string):
		containwords = False
		if string.strip() == "":
			containwords = True
		for errorWord in self.errorWords:
			if errorWord in string:
				containwords = True
		if containwords == False:
			#print string.strip()			
			string = " ".join(string.split())
			splitted = string.split(" ")
			#print splitted
			if "not" in splitted[0]:
				Mac = splitted[2]
				power = splitted[3]
			else:
				Mac = splitted[1]
				power = splitted[2]
			lts = time.strftime('%Y-%m-%d %H:%M:%S')	
			
			if power in "-1":
				return
			print "MAC: " + Mac + " LTS: " + lts + " POWER: " + power
			
if __name__ == "__main__":
	Textreader = textreader('test.txt')
