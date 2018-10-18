import csv
from PIL import Image

IMG_HEIGHT = 32
IMG_WIDTH = 32
training_label = []
training_set = []
with open('ds/ds1/ds1Train.csv', 'rb') as input_file:
	reader = csv.reader(input_file)

	for row in reader:
		training_label.append(int(row[len(row) - 1]))
		training_set.append([int(row[i]) for i in range(0, len(row) - 1)])

# test = 4

# first_img = training_set[test]
# first_img[:] = [first_img[i:i + IMG_WIDTH] for i in range(0, 1024, 32)]

# image = Image.new("1", (IMG_WIDTH, IMG_HEIGHT))
# pixels = image.load()

# for i in range(0, IMG_WIDTH):
# 	for j in range(0, IMG_HEIGHT):
# 		pixels[i, j] = first_img[i][j]

count_label = []
for i in range(51):
	count_label.append(0)

for row in training_label:
	count_label[row] = count_label[row] + 1

for i in range(51):
	print(str(i) + ": " + str(count_label[i]))

# image.show()
# print(training_label[test])
# print(training_label)
# print(training_set)