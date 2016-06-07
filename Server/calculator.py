import MySQLdb, math, thread, time
from numpy import *
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


class calculator:

	def residuals2D(self, point, data):
		summ = [square(( square(p[0] - point[0]) + square(p[1] - point[1]) ) - square(p[2])) for p in data]
		return summ
	
	def residuals3D(self, point, data):
		summ = sum([square(( square(p[0] - point[0]) + square(p[1] - point[1]) + square(p[2] - point[2]) ) - square(p[3])) for p in data])
		return [summ,summ,summ]
		
		
	def plot(self, point, data):
		thread.start_new_thread(self.__plot, (point, data) )	
		
	
	def __plot(self, point, data):
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		for p in data:
				if len(p) == 4:
					circ = plt.Circle((p[0], p[1]), radius=p[3], color='b', alpha=0.5)
				else:
					circ = plt.Circle((p[0], p[1]), radius=p[2], color='b', alpha=0.5)
				circ2 = plt.Circle((p[0], p[1]), radius=0.01, color='r', alpha=1)
				ax.add_patch(circ)
				ax.add_patch(circ2) 
		circ = plt.Circle((point[0][0], point[0][1]), radius=10, color='g', alpha=0.5)
		ax.add_patch(circ)
		ax.autoscale()
		plt.show()		
		
	
	def calculatepoint(self,Data):
		data = []
		for dat in Data:
			data.append(list(dat))
		startPoints = self.calcStartPoints(Data)
		is3d = False
		for dat in data:
			if len(dat) == 4:
				if dat[2] == 0:
					dat.pop(2)
				else:
					is3d = True
		if is3d == True:
			#print "is 3d is true"
			#counter = 0
			dlist = []
			for dat in data:
				if len(dat) == 3:
					templist = list(dat)
					templist.append(templist[2])
					templist[2] = 0.0
					dlist.append(tuple(templist))
				else:
					dlist.append(dat)
			return leastsq(self.residuals3D,startPoints[:2] , args=(dlist))
		else:
			#print "is 3d is false"
			return leastsq(self.residuals2D, startPoints, args=(data))
		
	def setbeginpoint3D(self, beginpoint):
		self.beginpoint3D = beginpoint
	
	def setbeginpoint2D(self, beginpoint):
		self.beginpoint2D = beginpoint

	def convertPowerToRange(self, pwr):
		return pwr
		
	def calcStartPoints(self,points):
		xArr = []
		yArr = []
		zArr = []
		for point in points:
			xArr.append(point[0])
			yArr.append(point[1])
			zArr.append(point[2])
		return [max(xArr)/2,max(yArr)/2,max(zArr)/2]
		
if __name__ == "__main__":
	points4 = [[236,404,0,37*4],[267,740,0,60*4],[0,194,0,46*4]]

	obj = calculator()

	obj.plot(obj.calculatepoint(points4), points4)
	while 1:
		print "still runnimg"
		time.sleep(3)
	


