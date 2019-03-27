#!/usr/bin/env python

import numpy
import rospy
import time
import matplotlib.pyplot as plt
import random

from random import randint
from grasp_clustering.msg import GraspInfo

class cluster_grasps(object): 
    def __init__(self):
	
	self.pub = rospy.Publisher("/labeled_grasp_info", GraspInfo, queue_size=1)        
	self.sub = rospy.Subscriber("/grasp_info", GraspInfo, self.alotlabel)


    def train_data(self):
	file = rospy.get_param('~train_filename')
        data = numpy.genfromtxt(fname=file, delimiter = ',', skip_header=1)
	dimension = 15
	nlab = 8
	
	data = data[:, 8:8+dimension]
	centroids = numpy.zeros((nlab, dimension))
	label = numpy.zeros((data.shape[0],1))
	centroidss = numpy.zeros((nlab, dimension))
	self.centers = numpy.zeros((nlab, dimension))

	for i in range(0,nlab):
		pu = randint(0,	data.shape[0])
		centroids[i,:] = data[pu,:]

	previ = centroids

	#plt.scatter(data[:,0], data[:,1], s = 10)
	#plt.scatter(centroids[:,0], centroids[:,1], color = 'green', s = 50)
		

	for i in range(0, data.shape[0]):
                dist = []
		for j in range(0, nlab):
			sumd = 0
			for k in range(0, dimension):
				sumd = sumd + (data[i,k] - centroids[j,k])**2
			sumd = sumd**0.5
			dist.append(sumd)
		label[i,0] = dist.index(min(dist)) + 1
	
	exit = 1
	while exit > 0.01:		
		for i in range(0, nlab):
			sums = 0
			counter = 0
			for j in range(0, data.shape[0]):
				if label[j,0] == i+1:
					sums = sums + data[j,:]
					counter = counter + 1
			
			centroidss[i,:] = sums/counter
			
		exit = (numpy.sum(centroidss - previ)**2)**0.5		
		previ = centroidss

		for i in range(0, data.shape[0]):
		        dist = []
			for j in range(0, nlab):
				sumd = 0
				for k in range(0, dimension):
					sumd = sumd + (data[i,k] - centroidss[j,k])**2
				sumd = sumd**0.5
				dist.append(sumd)
			label[i,0] = dist.index(min(dist)) + 1
	
	#plt.scatter(centroidss[:,0], centroidss[:,1], color = 'red', s = 50)
	#plt.show()
	self.centers = centroidss
	print('Done')	
	return centroidss

    def alotlabel(self, msg):	
	label = []	
        dist = []		
	for j in range(0, len(self.centers)):
		sumd = 0
		for k in range(0,len(msg.glove)):
			sumd = sumd + (msg.glove[k] - self.centers[j,k])**2
		sumd = sumd**0.5
		dist.append(sumd)
	label = dist.index(min(dist)) + 1
	message = GraspInfo()
	message.label = label
	message.glove = msg.glove
	message.emg = msg.emg
	self.pub.publish(message)
	

if __name__ == '__main__':    
	rospy.init_node('cluster_grasps', anonymous=True)
	cg = cluster_grasps()
	cg.train_data()		
	rospy.spin()

