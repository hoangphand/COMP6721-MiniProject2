import csv
from PIL import Image

DS1_IMG_HEIGHT = 32
DS1_IMG_WIDTH = 32
DS1_TRAIN_SIZE = 1960
DS1_VAL_SIZE = 514
DS1_LABEL_SIZE = 51
DS1_TRAIN_PATH = 'ds/ds1/ds1Train.csv'
DS1_VAL_PATH = 'ds/ds1/ds1Val.csv'

DS2_IMG_HEIGHT = 32
DS2_IMG_WIDTH = 32
DS2_TRAIN_SIZE = 6400
DS2_VAL_SIZE = 2000
DS2_LABEL_SIZE = 10
DS2_TRAIN_PATH = 'ds/ds2/ds2Train.csv'
DS2_VAL_PATH = 'ds/ds2/ds2Val.csv'

def load_dataset(dataset_path, label_size):
	label = []
	dataset = []
	with open(dataset_path, 'rb') as input_file:
		reader = csv.reader(input_file)

		for row in reader:
			label.append(int(row[len(row) - 1]))
			dataset.append([int(row[i]) for i in range(0, len(row) - 1)])

	count_label = []
	for i in range(label_size):
		count_label.append(0)

	for row in label:
		count_label[row] = count_label[row] + 1

	return (dataset, label, count_label)

# test = 4

# first_img = training_set[test]
# first_img[:] = [first_img[i:i + IMG_WIDTH] for i in range(0, 1024, 32)]

# image = Image.new("1", (IMG_WIDTH, IMG_HEIGHT))
# pixels = image.load()

# for i in range(0, IMG_WIDTH):
# 	for j in range(0, IMG_HEIGHT):
# 		pixels[i, j] = first_img[i][j]

# image.show()
# print(training_label[test])
# print(training_label)
# print(training_set)