import csv, os
from config import data_links
vocab = {}
for file in os.listdir(data_links['vocab']):
	f = file.split('.')[0]
	vocab[f] = {}
	with open(os.path.join(data_links['vocab'], file), 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			#print (row['Value'])
			vocab[f][row['Value']] = row['URI']


print (vocab)
