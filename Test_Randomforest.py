from sklearn.ensemble import RandomForestClassifier as rfc
import csv
import numpy as np 
import pickle
import time

label = ["SAFE", "PHISHING"]
m = 2400
n_feature = 40

def readData():
	file = open("Dataset/train.csv","r")
	reader = csv.reader(file)
	data = []
	for row in reader:
		if len(row) > 0:
			data.append(row)
	data = np.asarray(data)
	dataX = data[:, :n_feature]
	dataX = dataX.astype(np.float32)
	dataY = data[:, n_feature:]
	dataY = dataY.astype(np.int8)
	return dataX, dataY

filename = 'finalized_model.sav'
def Random_forest_train():
	dataX, dataY = readData()
	dataY = dataY.reshape(dataY.shape[0])
	x_train = dataX[:m, :]
	x_test = dataX[m:, :]
	y_train = dataY[:m]
	y_test = dataY[m:]
	acc_av = 0
	for i in range(10):
		n_estimators = 100
		model = rfc(n_estimators = n_estimators)
		model.fit(x_train, y_train)
		# save the model to disk
		pickle.dump(model, open(filename, 'wb'))
		score = model.score(x_test, y_test)
		acc_av += score
	print (acc_av/10)
	# control to n_estimators
	# f = open("Result_ACC/RFR/result.csv", "w")
	# for i in range(100,101):
	# 	acc = 0.0
	# 	n_estimators = i
	# 	for j in range(10):
	# 		model = rfc(n_estimators = n_estimators)
	# 		model.fit(x_train, y_train)
	# 		# save the model to disk
	# 		pickle.dump(model, open(filename, 'wb'))
	# 		score = model.score(x_test, y_test)
	# 		acc += score
	# 	acc = acc/10
	# 	f.write("%d,%f\n"%(i,acc))
Random_forest_train()

def test_model():
	dataX, dataY = readData()
	dataY = dataY.reshape(dataY.shape[0])
	x_train = dataX[:m, :]
	x_test = dataX[m:, :]
	y_train = dataY[:m]
	y_test = dataY[m:]

	for i in range(100):
		n_estimators = 100
		model = rfc(n_estimators = n_estimators)
		model.fit(x_train, y_train)
		# save the model to disk
		pickle.dump(model, open(filename, 'wb'))
		score = model.score(x_test, y_test)
		print ("acc = ", score)

		acc_pre = np.max(model.predict_proba(x_train),1)
		# print (acc_pre[:1000])
		label_pre = model.predict(x_train)
		for i in range(len(acc_pre)):
			if label_pre[i]!=y_train[i]:
				if (acc_pre[i] > 0.8):
					print ("label_predict = {}, label_Real = {}, ACC = {}".format(label_pre[i], 
												y_train[i], acc_pre[i]))
					y_train[i] = label_pre[i]

