#!/usr/bin/env python

#import json module
import json

# variable 'f' is set as file stream (handle)
f = open('era.json', 'r')
# variable 'json_string' is set to file content
json_string = f.read()

# variable 'original' is assigned the result of applying json.loads to json_string (makes the program read the contents as a python data structure)
original = json.loads(json_string)
# variable 'intermediate' is initialized as an empty dictionary
intermediate = {}

# variable 'arr' is assigned the value of dictionary 'original' with key 'objects' (an array of dictionaries) from original json 
arr = original['objects']
# 'obj' is each dictionary in 'arr'
for obj in arr:
	# variable 'pid' is assigned the content of 'pid' in variable 'obj' (and so on)
	pid = obj['pid']
	collection = obj['collection']
	datastream = obj['datastream']
	field = obj['field']
	value = obj['value']
	

# this is the most difficult of the program
# if there is no 'pid' in 'intermediate' then create a dictionary with key 'collection' containing the value of variable 'collection' 
# if there is no 'pid' value as key in 'intermediate' set it to a dictionary with keys' pid' and collection' and values array with single values of variables 'pid' and 'collection'
	if not pid in intermediate:
		intermediate[pid] = {
			'collection': [collection],
			'pid': [pid]
		}
	# if there is no 'datastream' value (used as key) in 'intermediate[pid]', set it to an empty dictionary
	if not datastream in intermediate[pid]:
		intermediate[pid][datastream]={}
	# if there is no 'field' value as key in 'intermediate[pid][datastream]', set it to start a new key in datastream dictionary
	if not field in intermediate[pid][datastream]:
		intermediate[pid][datastream][field] = [value]
	# otherwise, append additional values to  pid[datastream][field] list
	else:
		intermediate[pid][datastream][field].append(value)

# format
# variable 'result' is initialized as an empty list
result = []

# for each initial key in 'intermediate' create 'entry' dictionary where 'data' key contains value of 'pidkey' (content of each dictionary)
for pidkey in intermediate:
	entry = {
		'data': intermediate[pidkey]
	}
	# use method append to insert additional entries in 'result'
	result.append(entry)


# print result list with .dumps method with optional parameters
print json.dumps(result, sort_keys=True, indent=2, separators=(',', ': '))
