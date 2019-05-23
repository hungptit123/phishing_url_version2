from sklearn.ensemble import RandomForestClassifier as rfc
import csv
import numpy as np 
import pickle
import time
import Feature_Characters
import Feature_HTML

label = ["SAFE", "PHISHING"]
filename = 'finalized_model.sav'

def extract_feature(url):
	feature = Feature_Characters.generated(url)
	feature.extend(Feature_HTML.generate(url))
	return feature

def Predict_Randomforest(url):
	model = pickle.load(open(filename, "rb"))
	st = time.time()
	feature = extract_feature(url)
	x_test = []
	x_test.append(feature)
	x_test = np.asarray(x_test)
	predict = model.predict(x_test)
	return label[predict[0]]

# url = "http://www.execglobalnet.com/"

# print ("URL = {}\nLabel = {}".format(url,Predict_Randomforest(url)))