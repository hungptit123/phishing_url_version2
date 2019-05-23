import tensorflow as tf 
import numpy as np
import pickle
import cv2
import csv
from sklearn.neighbors import KNeighborsClassifier as KNN

n = 40 #num feature
m_size = 0
m = 2400

def readData():
	global m_size
	file = open("Dataset/train.csv","r")
	reader = csv.reader(file)
	data = []
	i = 0
	for row in reader:
		data.append(row)
	data = np.asarray(data)
	# print (data.shape)
	# np.random.shuffle(data)
	dataX = data[:, :n]
	m_size = dataX.shape[0]
	dataX = dataX.astype(np.float32)
	dataY = data[:, n:]
	dataY = dataY.astype(np.int8)
	return dataX, dataY
# readData()

def minize(dataX):
	x_max = np.max(dataX, axis = 0)
	x_min = np.min(dataX, axis = 0)
	avange = np.sum(dataX, axis = 0)/m_size
	for i in range(n):
		r = x_max[i] - x_min[i]
		if r==0:
			r = 1
		if r < 0:
			r = abs(r)
		dataX[: , i:i+1] = (dataX[: , i:i+1] - avange[i])/r
	return dataX
def run_KNN():
	f = open("Result_ACC/KNN/result.csv", "w")
	dataX, dataY = readData()
	dataX = minize(dataX)
	dataY = dataY.reshape(dataY.shape[0])
	x_train = dataX[:m, :]
	x_test = dataX[m:, :]
	y_train = dataY[:m]
	y_test = dataY[m:]
	# acc_max = 0
	# neighbors = 0
	# n_neighbors = 24
	# for i in range(1,100):
	# 	knn = KNN(n_neighbors = i, algorithm = "ball_tree", 
	# 					weights = "distance")
	# 	knn.fit(x_train, y_train)
	# 	result = knn.score(x_test, y_test)
	# 	f.write("%d,%f\n"%(i,result))
	# 	if acc_max < result:
	# 		neighbors = i
	# 		acc_max = result
	# print (acc_max)
	# print (neighbors)
	knn = KNN(n_neighbors = 24, algorithm = "ball_tree", 
						weights = "distance")
	knn.fit(x_train, y_train)
	result = knn.score(x_test, y_test)
	
run_KNN()