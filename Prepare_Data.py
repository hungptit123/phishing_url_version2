import csv
import numpy as np
import pickle
import Configuration as CF
import Feature_Extraction
import Feature
import time

def pre_data():
	# return file csv extract feature from url
	reader = csv.reader(open(CF.DIR_DATA_TRAIN, "r"))
	writer = csv.writer(open(CF.DIR_DATA_TRANFORM, "w"))
	# writer.writerow(properities())
	i = 0
	arr = []
	st = time.time()
	for row in reader:
		if i > 0:
			st = time.time()
			feature = Feature_Extraction.generated(row[0])
			feature.extend(Feature.generate(row[0]))
			feature.append(int (row[1]))
			writer.writerow(feature)
			print (row, "  :  time = ", time.time()-st)
		i += 1
pre_data()

def extract_feature(url):
	feature = Feature_Extraction.generated(url)
	feature.extend(Feature.generate(url))
	# print (feature)
	return feature

# def tinh():
# 	reader = csv.reader(open(CF.DIR_DATA_TRANFORM, "r"))
# 	data = {}
# 	data['0'] = 0
# 	data['1'] = 0
# 	for row in reader:
# 		if len(row) > 0:
# 			data[row[-1]] += 1
# 	print (data)
# tinh()

# extract_feature("http://www.van-sant.si/components/com_akeeba/controllers/drive/auth/vi")