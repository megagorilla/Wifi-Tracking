import MySQLdb, math, thread, time
from numpy import *
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


class calculator:
	def __init__(self):
		self.beginpoint3D = [0.0, 0.0, 0.0]
		self.beginpoint2D = [0.0, 0.0]
			

	def residuals2D(self, point, data):
		summ = sum([square(( square(p[0] - point[0]) + square(p[1] - point[1]) ) - square(p[2])) for p in data])
		return [summ,summ]
	
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
		circ = plt.Circle((point[0][0], point[0][1]), radius=0.05, color='g', alpha=0.5)
		ax.add_patch(circ)
		ax.autoscale()
		plt.show()		
		
	
	def calculatepoint(self,data):
		is3d = False
		for dat in data:
			if len(dat) == 4:
				is3d = True
		if is3d == True:
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
			return leastsq(self.residuals3D, self.beginpoint3D, args=(dlist))
		else:
			return leastsq(self.residuals2D, self.beginpoint2D, args=(data))
		
	def setbeginpoint3D(self, beginpoint):
		self.beginpoint3D = beginpoint
	
	def setbeginpoint2D(self, beginpoint):
		self.beginpoint2D = beginpoint
		
	
		
		
	
		

if __name__ == "__main__":
	points1 = [ (-1.91373, -0.799904, 2.04001), (-0.935453, -0.493735, 0.959304), (0.630964, -0.653075, 0.728477), (0.310857, -0.018258, 0.301885), (0.0431084, 1.25321, 1.19012) ]
	points3 = [ (10.0,10.0, 0, 5.0) , (20.0,20.0,5.0), (20.0,10.0,5.0)]
	#points2 = [[10.0, 10.0, 5.0], [20.0, 20.0, 5.0], [20.0, 10.0, 5.0]]


	

	obj = calculator()

	obj.plot(obj.calculatepoint(points1), points1)
	#print "tuple"
	print obj.calculatepoint(points1)
	#print "array"
	print obj.calculatepoint(points3)
	while 1:
		print "still rummimg"
		time.sleep(3)
	


