import csv
import numpy as np
import pickle
import Configuration as CF
import Feature_Characters
import Feature_HTML
import time

def pre_data():
	# return file csv extract feature from url
	reader = csv.reader(open(CF.DIR_DATA_TRAIN, "r"))
	writer = csv.writer(open(CF.DIR_DATA_TRANFORM, "a"))
	# writer.writerow(properities())
	i = 0
	arr = []
	st = time.time()
	for row in reader:
		if i > 5500:
			print (row)
			st = time.time()
			feature = Feature_Characters.generated(row[0])
			feature.extend(Feature_HTML.generate(row[0]))
			feature.append(int (row[1]))
			print (feature)
			# if (time.time()-st <= 50):
			writer.writerow(feature)
			print ("time = ", time.time()-st)
		i += 1
		if (i%50 == 0):
			print (i)
		if i==6500:
			break
# pre_data()
