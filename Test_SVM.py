import tensorflow as tf 
import numpy as np
import pickle
import cv2
import csv
from sklearn import svm

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
	dataX = data[:, :n]
	m_size = dataX.shape[0]
	dataX = dataX.astype(np.float32)
	dataY = data[:, n:]
	dataY = dataY.astype(np.int8)
	return dataX, dataY

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

def run_SVM():
	f = open("Result_ACC/SVM/result.csv", "r")
	dataX, dataY = readData()
	dataX = minize(dataX)
	dataY = dataY.reshape(dataY.shape[0])
	x_train = dataX[:m, :]
	x_test = dataX[m:, :]
	y_train = dataY[:m]
	y_test = dataY[m:]

	c = 1000
	gamma =  0.03
	model = svm.SVC(C = c, kernel = 'rbf', gamma = gamma)
	model.fit(x_train, y_train)
	result = model.score(x_test, y_test)
	print ("ACC = ", result)
	# c = 1000, gamma =  0.03
	# acc_max = 0
	# acc_c = 0
	# acc_gamma = 0
	# c = 1.0
	# for i in range(101):
	# 	for h in range(1,6):
	# 		gamma = h
	# 		for j in range(4):
	# 			model = svm.SVC(C = c, kernel = 'rbf', gamma = gamma)
	# 			model.fit(x_train, y_train)
	# 			result = model.score(x_test, y_test)
	# 			gamma = gamma/10
	# 			f.write("%d,%f,%f,%f\n" %(i,c,gamma,result))
	# 			if (acc_max < result):
	# 				acc_max = result
	# 				acc_c = c
	# 				acc_gamma = gamma
	# 	c += 10
	# 	if (c%10!=0):
	# 		c = c-c%10
	# print (acc_max)
	# print (acc_gamma)
	# print (acc_c)
run_SVM()