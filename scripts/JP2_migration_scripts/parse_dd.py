import csv
from config import data_links, namespaces

data_d = data_links['mappings']

with open(data_d, 'r') as file:
	reader = csv.DictReader(file)
	map = {}
	for row in reader:
		m = ''
		peel = row['MODS/METS'].split('>')
		jp = row['JPII']
		#print (jp, peel)
		for level in peel:
			#print (level)
			att_value = None
			att_tag = None
			if '+' not in level:
				attrib = level.strip().split(' ')[1:]
				field = level.strip().split(' ')[0]
				if len(attrib) != 0:
					att_value= attrib[0].split('=')[1]
					att_tag = attrib[0].split('=')[0]
					for i in range(1,len(attrib)):
						att_value += ' ' + attrib[i]
			if att_tag != None:
				m += field+'[@'+att_tag+'="'+att_value+'"]/'
			else:
				m += field+'/'
		print (m[0:-1])



