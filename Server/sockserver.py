import socket, select, sys, time, threading, thread, os
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

class SocketServer(threading.Thread):

	def __init__(self, port, pubkey,privkey):
		threading.Thread.__init__(self)
		self.PORT = port
		self.RECV_BUFFER = 131072
		self.CONNECTION_LIST = []
		self.ADDRESS_LIST = []
		self.HOST = ''
		self.Received_messages = []
		self.CONN_NAMES = []
		self.CONN_PUBKEYS = []
		self.running = True
		self.pubkeyStr = pubkey
		self.privateKey = privkey
		
	def stop(self):
		self.running = False
		pid = os.getpid()
		os.kill(pid,9)
		
	def isRunning(self):
		return self.running
		
	def nextReceived(self):
		if len(self.Received_messages) > 0:
			return self.Received_messages.pop(0)
		else:
			return -1
			
	def nameExists(self,name):
		return (name in self.CONN_NAMES)
		
	def hasReceived(self):
		return len(self.Received_messages) > 0
		
	def clientthread(self,conn):
		try:
			#Sending message to connected client
			index = self.CONNECTION_LIST.index(conn)
			conn.send(self.pubkeyStr + ":name=" + self.CONN_NAMES[index])
			print "object length: " + str(len(self.pubkeyStr))
			data = conn.recv(self.RECV_BUFFER)
			if ":name=" in data:
				data = data.split(":name=")
				if data[1] in self.CONN_NAMES[index]:
					self.CONN_PUBKEYS.append(RSA.importKey(data[0]))
				else:
					print "data[1] = " + data[1] + "\nself.CONN_NAMES[index]= " + self.CONN_NAMES[index]
					raise ValueError("Could nog read public key from data")
			#infinite loop so that function do not terminate and thread do not end.
			while self.running:
			
				#Receiving from client
				data = conn.recv(self.RECV_BUFFER)
				reply = 'OK...' + data
				#print reply
				if not data: 
					break
		
				#conn.sendall(reply)
				cipher = PKCS1_OAEP.new(self.privateKey)
				toSend=""
				try:
					message = cipher.decrypt(data)
					self.Received_messages.append(message)
					toSend += "OK;"
				except ValueError as e:
					print "coulnd't decrypt, messagelength: " + str(len(msg)) + str(e.args)
					toSend += "ERR;"
				conn.send(toSend)
				
		except socket.error:
			print "a client left"
		except:
			raise
		finally:
			#came out of loop
			index = self.CONNECTION_LIST.index(conn)
			self.CONN_NAMES.pop(index)
			self.ADDRESS_LIST.pop(index)
			self.CONNECTION_LIST.pop(index)
			conn.close()
		
	def broadcast(self,string):
		for conn in self.CONNECTION_LIST:
			print "Sending to: " + str(conn) + " string: " + string
			conn.send(string+ "\n")
	
	def run(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print 'Socket created'
		try:
			self.sock.bind((self.HOST, self.PORT))
		
			print 'Socket bind complete'
			self.sock.listen(10)
			print 'Socket now listening'
		 	
			while self.running:
				#wait to accept a connection - blocking call
				print "waiting for new connection"
				conn, addr = self.sock.accept()
				print "new connection accepted"
				self.CONNECTION_LIST.append(conn)
				self.ADDRESS_LIST.append(addr)
				self.CONN_NAMES.append("sniffer#" + str(len(self.CONN_NAMES)))
				print 'Connected with ' + addr[0] + ':' + str(addr[1])
			
				#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
				thread.start_new_thread(self.clientthread ,(conn,))
		except socket.error , msg:
			print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
		except:
			print "Closing server"
			for conn in self.CONN_NAMES:
				
				conn.sendall("Closing server")
				conn.close()
			self.stop()
			self.sock.close()
			thread.exit()
			sys.exit()
			raise
		finally:
			self.sock.close()
			pid = os.getpid()
			os.kill(pid,9)

		
			

if __name__ == "__main__":
	server = SocketServer(8888)
	try:
		server.start()
		while server.isRunning():
			string = raw_input("Type something to broadcast:\n")
			server.broadcast(string)
			print server.Received_messages
	except:
		raise
	finally:
		print "stopping server"
		server.stop()
		server.sock.close()
		pid = os.getpid()
		os.kill(pid,9)
		server.join()
		
