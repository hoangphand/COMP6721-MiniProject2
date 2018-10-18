from __future__ import division
import csv
from PIL import Image
import sys

IMG_HEIGHT = 32
IMG_WIDTH = 32
NO_OF_CHARACTERS = 51
training_label = []
training_set = []
with open('ds/ds1/ds1Train.csv', 'rb') as input_file:
	reader = csv.reader(input_file)

	for row in reader:
		training_label.append(int(row[len(row) - 1]))
		training_set.append([int(row[i]) for i in range(0, len(row) - 1)])

training_set_size = len(training_set)

count_label = []
for i in range(NO_OF_CHARACTERS):
	count_label.append(0)

for row in training_label:
	count_label[row] = count_label[row] + 1

prior_els = []

for i in range(len(count_label)):
	el = []
	for j in range(len(training_set[0])):
		el.append(0)
	prior_els.append(el)

for i in range(len(training_set)):
	for j in range(len(training_set[0])):
		prior_els[training_label[i]][j] = prior_els[training_label[i]][j] + training_set[i][j]

validation_label = []
validation_set = []
with open('ds/ds1/ds1Val.csv', 'rb') as input_file:
	reader = csv.reader(input_file)

	for row in reader:
		validation_label.append(int(row[len(row) - 1]))
		validation_set.append([int(row[i]) for i in range(0, len(row) - 1)])

test = 0
correct_count = 0

for test in range(len(validation_set)):
	predictions = []
	for i in range(len(count_label)):
		tmp = 1
		for j in range(len(training_set[0])):
			if validation_set[test][j] == 1:
				tmp = tmp * (prior_els[i][j] + 1) / (count_label[i])
			else:
				tmp = tmp * (count_label[i] - prior_els[i][j] + 1) / (count_label[i]) 
		predictions.append(tmp * count_label[i] / training_set_size)

	prediction = -1

	for i in range(len(count_label)):
		if predictions[i] > prediction:
			prediction = predictions[i]
			ans = i

	print("prediction: " + str(ans))
	print("actual: " + str(validation_label[test]))

	if ans == validation_label[test]:
		correct_count = correct_count + 1

print(correct_count / len(validation_set))
