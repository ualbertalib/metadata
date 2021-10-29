file = open('WCW.xml', 'r')
xml = file.readlines()
data = {}
for i, line in enumerate(xml):
	if '<marc:record>' in line:
		record = None
		leader = None
		ctrl = None
		tag = None
	if 'marc:leader' in line:
		#leader = line .split('marc:leader>')[1].split('</marc:leader')[0]
		leader = str(i+1)
		data[leader] = {} 
	if 'marc:controlfield' in line: 
		ctrl = line.split('marc:controlfield>')[1].split('</marc:controlfield')[0]
	if '<marc:datafield' in line:
		tag = line.split('tag="')[1].split('"')[0]
		j = 1
		while '</marc:datafield' not in xml[i+j]:
			if '<marc:subfield' in xml[i+j]:
				code = xml[i+j].split('code="')[1].split('"')[0]
				sub_val = xml[i+j].split('>')[1].split('</')[0]
				subf = tag + code
				data[leader][subf] = sub_val
			j += 1
			
		pass

elements = {}

for i in data.keys():
	for j in data[i]:
		if j not in elements.keys():
			elements[j] = 1
		else:
			elements[j] += 1


print (elements)
print (len(elements))



