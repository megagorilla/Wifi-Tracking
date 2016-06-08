import os, thread, time, subprocess,hashlib,sys, threading, socket,re
from station import Station
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA
from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue, Empty

class sniffer(threading.Thread):
	
	def __init__(self, device = "", channel = None):
		threading.Thread.__init__(self)
		self.stations = []
		self.whitelist = []
		self.device = device
		self.channel = channel
		self.running = True
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_address = ('localhost', 8888)
		print >>sys.stderr, 'connecting to %s port %s' % server_address
		self.sock.connect(server_address)
		string =  self.sock.recv(2048)
		string = string.split(":name=")
		self.name = string[1]
		print string[0]
		self.publicKey = RSA.importKey(string[0])
		self.myPrivateKey = RSA.generate(2048)
		self.myPublicKey = self.myPrivateKey.publickey()
		self.myPubkeyStr = self.myPublicKey.exportKey('PEM')
		tosend = self.myPubkeyStr + ":name=" + self.name
		self.sock.sendall(tosend)
		isnotlast = True
		received = ""
		while isnotlast:
			received = received + self.sock.recv(2048)
			if "LAST" in received:
				isnotlast = False
		received = received.replace(";LAST","")
		self.whitelist = received.split(";")
		print"\n\nWHITELIST:\n"
		print self.whitelist
		self.io_q = Queue()
		self.errorWords = ["BSSID", "WPA2", "WPA", "Elapsed:", "[J[1;1H" , "[0m[2J[?25l[2J", "[1;1H", "OPN", "WEP","\x1b[J\x1b[?25h"]

				
		
	def setDevice(self,device):
		self.device = device
		
	def setChannel(self,channel):
		self.channel=channel
	
	def __find_station(self, Mac):
		MacHash = self.__hash(Mac)
		counter = 0
		for station in self.stations:
			if MacHash == station.getMacHash():
				return counter
			else:
				counter += 1
		return -1

	def runCommand(self,str):
		try:
			toReturn = os.popen(str).read()
		except:
			print "couldn't execute command"
		finally:
			return toReturn
	
	def __find_str(self,s, char):
		index = 0
		if char in s:
		    c = char[0]
		    for ch in s:
		        if ch == c:
		            if s[index:index+len(char)] == char:
		                return index
		        index += 1
		return -1
	   
	def __hash(self,str):
		return hashlib.sha512(str).hexdigest()
	
	
	def getWlans(self):
		list = []
		out = self.runCommand("sudo airmon-ng")
		while True:
			loc = self.__find_str(out,"wlan")
			if loc == -1:
				break
			list.append(out[loc:loc+5])
			out = out[loc+5:]
		return list
	
	def getMons(self):
		list = []
		out = self.runCommand("sudo airmon-ng")
		while True:
			loc = self.__find_str(out,"mon")
			if loc == -1:
				break
			list.append(out[loc:loc+4])
			out = out[loc+4:]
		return list
	
	def init_sniffers(self):
		wlans = self.getWlans()
		print wlans
		print "these devices wil init: " + str(wlans)
		self.runCommand("sudo airmon-ng check kill")
		for wlan in wlans:
			self.runCommand("sudo airmon-ng start " + wlan)
	
	def init_sniffer(self,wlan):
		self.runCommand("sudo airmon-ng check kill")
		self.runCommand("sudo airmon-ng start " + wlan)
	
	def stop(self):
		self.running = False
		
	def run(self):
		try:
			self.__startDump()
		except KeyboardInterrupt:
			self.join(1)
			if self.isAlive():
				raise

	def __startDump(self):
 		print "airodump is starting"
 		try:
 			self.runCommand("sudo rm sniffdump*")
 		except:
 			print "sniffdump file didn't exist"
 		finally:
 			self.runCommand("sudo gnome-terminal -e 'airodump-ng " + self.device + 
 			" --channel " + str(self.channel) + " --output-format csv --write sniffdump'")
 			while self.running:
 				try:
 					f = open("sniffdump-01.csv","r")
 					content = f.read()
 					f.close()
 					self.__processFile(content)
 				except KeyboardInterrupt:
 					break
 				except IOError as inst:
 					if inst.args[0] is 2:
 						print inst.args
 						print "no such file"
 					else:
 						print inst.args
 						raise
 				finally:
 					time.sleep(1)
				
	def __encrypt(self,string):
		cipher = PKCS1_OAEP.new(self.publicKey)
		return cipher.encrypt(string)
		
	def __processFile(self,content):
 		if __name__ == "__main__":
 			os.system("clear")
 		head = "Station MAC, First time seen, Last time seen, Power, # packets, BSSID, Probed ESSIDs"
 		start = self.__find_str(content,head)
 		content = content[start:]
 		lines = content.split("\n")
 		lines = lines[1:len(lines)-2]
 		location = ""
 		try:
 			for line in lines:
 				splitted = line.split(",")
 				Mac = splitted[0].strip(' \t\n\r')
 				lts = splitted[2].strip(' \t\n\r')
 				power = splitted[3].strip(' \t\n\r')
 				location = self.__find_station(Mac)
 				
 				if power in "-1":
 					continue
 				checkCounter = 0
  				while 1:
  					if ((location == -1) or (self.stations[location].getlts() not in lts)) and (self.__hash(Mac) in self.whitelist):
  						tosend = self.__encrypt(self.name+";"+self.__hash(Mac)+";"+lts+";"+power)
						print "SENDING" + self.name+";"+self.__hash(Mac)+";"+lts+";"+power
  						self.sock.sendall(tosend)
  						string =  self.sock.recv(2048)
  						if ("OK" in string) or (checkCouter is 3):
 							break
 						checkCounter += 1
 					else:
 						break
 				
 				if location == -1:
 					stat = Station(self.__hash(Mac),lts,power)
 					self.stations.append(stat)
 				else:
 					self.stations[location].setlts(lts)
 					self.stations[location].setpower(power)
 		except IndexError:
 			print "Small error in processFile, recovering as fast as possible"
 		except KeyboardInterrupt:
 			raise
  		if __name__ == "__main__":
  			for station in self.stations:
  				station.display()
			print"\n\nWHITELIST:\n"
			print self.whitelist
	
	def queueChecker(self):
		time.sleep(3)
		while 1:
		    try:
		        # Block for 1 second.
		        item = self.io_q.get(True, 0.1)	
		        self.io_q.task_done()
		    except Empty:
		        # No output in either streams for a second. Are we done?
		        if self.proc.poll() is not None:
		            break
		    else:
		        identifier, line = item
		        self.__procesLine(line)
		print "QUEUECHECKER ENDED QUEUECHECKER ENDED QUEUECHECKER ENDED QUEUECHECKER ENDED QUEUECHECKER ENDED"
	
def runCommand(str):
		try:
			toReturn = os.popen(str).read()
		except:
			print "couldn't execute command"
		finally:
			return toReturn

if __name__ == "__main__":
	wlan = ""
	print sys.argv
	if len(sys.argv) == 1 or "wlan" not in sys.argv[1]:
		while 1:
			print(runCommand("sudo airmon-ng | grep wlan"))
			x = raw_input('Which of these devices do you want to use?')
			if "wlan" in x:
				wlan = x
				break
			else:
				print "not a correct entry"
	else:
		wlan = sys.argv[1]
		
	if len(sys.argv) == 3:
		sniff = sniffer(channel = sys.argv[2])
	else:
		x = raw_input('Which channel do you want to sniff?')
		sniff = sniffer(channel = x)

	device = ""
	
	mons = sniff.getMons()
	print "Mons: " + str(mons)
	wlans = sniff.getWlans()
	print "wlans: " + str(wlans)
	if len(mons) is not len(wlans):
		sniff.init_sniffer(wlan)
		newmons = sniff.getMons()
		print "newMons: " + str(newmons)
		device = list(set(newmons)-set(mons))
		if len(device) is not 0:
			device = device[0]
			sniff.setDevice(device)
			try:
				sniff.start()
				while sniff.isAlive():
					print "still running"
					time.sleep(3)
			except:
				sniff.stop()
				sniff.join(1)
				raise
			finally:
				#sniff.runCommand("sudo killall airodump-ng")
				sniff.runCommand("sudo service network-manager restart")
				sniff.runCommand("sudo iw dev "+device+" del")
		else:
			print device
			print str(len(device))
			print "could not initialize"
			#sniff.runCommand("sudo killall airodump-ng")
			sniff.runCommand("sudo service network-manager restart")
	else:
		print "all devices are in use"
