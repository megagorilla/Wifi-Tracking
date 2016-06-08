import MySQLdb, math, thread, time
from numpy import *
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


class calculator:
	
	'''
	residuals2D is a method that details the algorhitm on how calculate a 2d position
	'''
	def residuals2D(self, point, data):
		summ = [square(( square(p[0] - point[0]) + square(p[1] - point[1]) ) - square(p[2])) for p in data]
		return summ
	
	'''
	residuals3D is a method that details the algorhitm on how calculate a 3d position
	'''
	def residuals3D(self, point, data):
		summ = sum([square(( square(p[0] - point[0]) + square(p[1] - point[1]) + square(p[2] - point[2]) ) - square(p[3])) for p in data])
		return [summ,summ,summ]
		
	'''
	plot is a method that calls __plot on a seperate thread
	'''	
	def plot(self, point, data):
		thread.start_new_thread(self.__plot, (point, data) )	
		
	'''
	__plot is a private method that opens a graphwindow filled with the raddii and the calculated location
	'''	
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
		
	'''
	calculatepoint is a method that calculates the location of a person based on a given 2d array, based on that 2d array it calculates a beginning point. 
	With that beginning point it either calculatus a 2d or a 3d location
	'''	
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
	
	'''
	convertPowerToRange is a yet to be written method that converts the pwr of a given wifi package to distance in centimeters
	'''
	def convertPowerToRange(self, pwr):
		return pwr
		
	'''
	calaculateavarage is a method that calculates the avarages of a given array
	'''		
	def calaculateavarage(self, array):
		return sum(array)/len(array)
		
		
	'''
	calcStartPoints is a method that calculates the starting points based of a 2d array given in the parameter, by taking the avarage of all the points in the 2d array
	'''	
	def calcStartPoints(self,points):
		xArr = []
		yArr = []
		zArr = []
		for point in points:
			xArr.append(point[0])
			yArr.append(point[1])
			zArr.append(point[2])
		return [self.calaculateavarage(xArr),self.calaculateavarage(yArr),self.calaculateavarage(zArr)]


'''
The main mostly used for testing purposes
'''		
if __name__ == "__main__":
	points4 = [[236,404,0,37*4],[267,740,0,60*4],[0,194,0,46*4]]

	obj = calculator()

	obj.plot(obj.calculatepoint(points4), points4)
	while 1:
		print "still runnimg"
		time.sleep(3)
	


