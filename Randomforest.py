from sklearn.ensemble import RandomForestClassifier as rfc
import csv
import numpy as np 
import pickle
import Prepare_Data as PD
import time

label = ["SAFE", "PHISHING"]

def readData():
	file = open("Dataset/data_tranform.csv","r")
	reader = csv.reader(file)
	data = []
	for row in reader:
		if len(row) > 0:
			data.append(row)
	data = np.asarray(data)
	# np.random.shuffle(data)
	dataX = data[:, :40]
	dataX = dataX.astype(np.float32)
	dataY = data[:, 40:]
	dataY = dataY.astype(np.int8)
	return dataX, dataY

filename = 'finalized_model.sav'
def Random_forest_train():
	# print (dataY.shape)
	m = 4800
	dataX, dataY = readData()
	dataY = dataY.reshape(dataY.shape[0])
	x_train = dataX[:m, :]
	x_test = dataX[m:, :]
	y_train = dataY[:m]
	y_test = dataY[m:]
	model = rfc(n_estimators = 10)
	model.fit(x_train, y_train)
	# save the model to disk
	pickle.dump(model, open(filename, 'wb'))
	score = model.score(x_test, y_test)
	print(score*100)
Random_forest_train()

def Accuracy_Randomforest(url):
	model = pickle.load(open(filename, "rb"))
	st = time.time()
	feature = PD.extract_feature(url)
	x_test = []
	x_test.append(feature)
	x_test = np.asarray(x_test)
	predict = model.predict(x_test)
	return label[predict[0]]