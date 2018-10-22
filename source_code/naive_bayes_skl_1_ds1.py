from __future__ import division
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
import sys
import image_util

(train_set, train_label, count_label) = image_util.load_dataset(image_util.DS1_TRAIN_PATH, image_util.DS1_LABEL_SIZE)

# clf = GaussianNB()
clf = BernoulliNB()
clf.fit(train_set, train_label)

(val_set, val_label, val_count_label) = image_util.load_dataset(image_util.DS1_VAL_PATH, image_util.DS1_LABEL_SIZE)

predictions = clf.predict(val_set)

correct_count = 0
for row in range(image_util.DS1_VAL_SIZE):
	print("prediction: " + str(predictions[row]))
	print("actual: " + str(val_label[row]))

	if predictions[row] == val_label[row]:
		correct_count = correct_count + 1

print(correct_count / image_util.DS1_VAL_SIZE)
