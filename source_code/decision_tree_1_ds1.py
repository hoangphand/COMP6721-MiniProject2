from __future__ import division
import csv
from PIL import Image
import sys
import image_util
import math

(train_set, train_label, count_label) = image_util.load_dataset(image_util.DS1_TRAIN_PATH, image_util.DS1_LABEL_SIZE)

first_entropy = 0

for i in range(image_util.DS1_LABEL_SIZE):
	p = count_label[i] / image_util.DS1_TRAIN_SIZE
	first_entropy = first_entropy - p * math.log(p, 2)

tree = {
	"index": -1,
	"outcome_0": -1,
	"outcome_1": -1,
	"node_0": [],
	"node_1": [],
	"parent": None,
	"note": -1
}
stack_of_features = []
stack_of_nodes = []

first_set = []
for i in range(image_util.DS1_TRAIN_SIZE):
	first_set.append(i)

start_feature = {
	"closed_list": [],
	"current_set": first_set,
	"entropy": first_entropy,
	"outcome": -1,
	"note": ""
}

stack_of_features.append(start_feature)
stack_of_nodes.append(tree)
list_outcomes = []

while len(stack_of_features) != 0:
	current_feature = stack_of_features.pop()
	current_node = stack_of_nodes.pop()

	if current_feature["outcome"] == -1:
		current_set = current_feature["current_set"]
		current_entropy = current_feature["entropy"]
		closed_list = current_feature["closed_list"]
		# STORE DETAILS OF THE MAX GAIN ATTRIBUTE
		max_gain = -1
		max_gain_index = -1
		max_gain_count_label = []

		outcome_0 = -1
		outcome_1 = -1

		for index in range(len(train_set[0])):
			if index not in closed_list:
				# MEMORIZE 0-SET AND 1-SET
				count_label_a = [[], []]
				# STORE INDICES OF ROWS WITH 0 VALUE AT "INDEX" ATTRIBUTE IN THE TRAIN_SET
				list_0 = []
				# STORE INDICES OF ROWS WITH 1 VALUE AT "INDEX" ATTRIBUTE IN THE TRAIN_SET
				list_1 = []

				for i in range(image_util.DS1_LABEL_SIZE):
					count_label_a[0].append(0)
					count_label_a[1].append(0)

				count_0 = 0
				count_1 = 0

				for i in range(len(current_set)):
					if train_set[current_set[i]][index] == 0:
						count_label_a[0][train_label[current_set[i]]] = count_label_a[0][train_label[current_set[i]]] + 1
						count_0 = count_0 + 1
						list_0.append(current_set[i])
					else:
						count_label_a[1][train_label[current_set[i]]] = count_label_a[1][train_label[current_set[i]]] + 1
						count_1 = count_1 + 1
						list_1.append(current_set[i])

				# CALCULATE ENTROPY OF 0-SET AND 1-SET
				h_0 = 0
				h_1 = 0

				for i in range(image_util.DS1_LABEL_SIZE):
					if count_label_a[0][i] != 0 and count_0 != 0:
						p_0 = count_label_a[0][i] / count_0
						h_0 = h_0 - p_0 * math.log(p_0, 2)

					if count_label_a[1][i] != 0 and count_1 != 0:
						p_1 = count_label_a[1][i] / count_1
						h_1 = h_1 - p_1 * math.log(p_1, 2)

				# CALCULATE GAIN
				gain = current_entropy - (count_0 / len(current_set)) * h_0 - (count_1 / len(current_set)) * h_1
				if gain > max_gain:
					max_gain_index = index
					max_gain = gain
					max_gain_entropy_0 = h_0
					max_gain_entropy_1 = h_1
					max_gain_list_0 = list_0
					max_gain_list_1 = list_1
					max_gain_count_label = count_label_a

		# ADD THE INDEX OF THE MAX GAIN INTO THE LIST OF DISCOVERED ATTRIBUTES
		closed_list.append(max_gain_index)
		current_node["index"] = max_gain_index

		if h_0 == 0:
			if len(max_gain_list_0) == 0:
				outcome_0 = -2
			else:
				for i in range(image_util.DS1_LABEL_SIZE):
					if max_gain_count_label[0][i] != 0:
						outcome_0 = i
						list_outcomes.append(i)
						break

		feature_0 = {
			"closed_list": closed_list,
			"current_set": max_gain_list_0,
			"entropy": max_gain_entropy_0,
			"outcome": outcome_0,
			# "note": "0"
		}
		node_0 = {
			"index": -1,
			"outcome_0": -1,
			"outcome_1": -1,
			"node_0": [],
			"node_1": [],
			"parent": current_node,
			"note": 0
		}

		if h_1 == 0:
			if len(max_gain_list_1) == 0:
				outcome_1 = -2
			else:
				for i in range(image_util.DS1_LABEL_SIZE):
					if max_gain_count_label[1][i] != 0:
						outcome_1 = i
						list_outcomes.append(i)
						break

		feature_1 = {
			"closed_list": closed_list,
			"current_set": max_gain_list_1,
			"entropy": max_gain_entropy_1,
			"outcome": outcome_1,
			# "note": "1"
		}
		node_1 = {
			"index": -1,
			"outcome_0": -1,
			"outcome_1": -1,
			"node_0": [],
			"node_1": [],
			"parent": current_node,
			"note": 1
		}

		stack_of_features.append(feature_0)
		stack_of_features.append(feature_1)
		stack_of_nodes.append(node_0)
		stack_of_nodes.append(node_1)

		current_node["outcome_0"] = outcome_0
		current_node["outcome_1"] = outcome_1

		if current_node["parent"] is not None:
			if current_node["note"] == 0:
				current_node["parent"]["node_0"] = current_node
			elif current_node["note"] == 1:
				current_node["parent"]["node_1"] = current_node
	else:
		if current_node["parent"] is not None:
			if current_node["note"] == 0:
				current_node["parent"]["node_0"] = current_node
			elif current_node["note"] == 1:
				current_node["parent"]["node_1"] = current_node

(val_set, val_label, val_count_label) = image_util.load_dataset(image_util.DS1_VAL_PATH, image_util.DS1_LABEL_SIZE)

correct_count = 0

for row in range(image_util.DS1_VAL_SIZE):
	current_node = tree
	prediction = -1
	while current_node["index"] != -1:
		value_at_index = val_set[row][current_node["index"]]
		if value_at_index == 0:
			current_node = current_node["node_0"]
		else:
			current_node = current_node["node_1"]
	if val_set[row][current_node["parent"]["index"]] == 0:
		if current_node["parent"]["outcome_0"] != -2:
			prediction = current_node["parent"]["outcome_0"]
		else:
			prediction = current_node["parent"]["outcome_1"]
	else:
		if current_node["parent"]["outcome_1"] != -2:
			prediction = current_node["parent"]["outcome_1"]
		else:
			prediction = current_node["parent"]["outcome_0"]

	print("prediction: " + str(prediction))
	print("actual: " + str(val_label[row]))

	if prediction == val_label[row]:
		correct_count = correct_count + 1

print(correct_count / image_util.DS1_VAL_SIZE)
