import re
from os import listdir
from os.path import isfile, join
import pymarc
import json

thesisLevel = [
	{"uri": "http://purl.org/spar/fabio/BachelorsThesis",
	"mapping": ["B.Ed.", "B. Ed.", "B. Div.", "B.Div.", "B.D."]},
	{"uri": "http://purl.org/spar/fabio/MastersThesis",
	"mapping": ["Master's", 'Master', 'M. Sc.', 'M.A.', 'M.Ed.', 'M.A.', 'M.Sc.', 'M.A', 'M.Sc. ', 'M. Ed.', 'MSc.', 'M.S. ', 'M.S.']},
	{"uri": "http://purl.org/spar/fabio/DoctoralThesis",
	"mapping": ["Doctoral", "Ph.D.", "Ph. D.", "PhD"]}]


def main():
	mypath = "/home/danydvd/git/remote/metadata/scripts/ia/files/xml/"
	output = []
	data = {}
	mapp = []
	for filename in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
		with open(join(mypath, filename), 'rb') as xml:
			reader = pymarc.marcxml.parse_xml_to_array(xml)
			# a place to store the fieldData
			data[filename] = {
						'title': [],
						'subject': {},
						'graduation_date': [],
						'dissertant': [],
						'department': [],
						'institution': [],
						'level': [],
						'abstract': []
						}

			for record in reader:
				dat = get_subjects(record, data, filename)
				dat = get_title(record, data, filename)
				dat = get_author(record, data, filename)
				dat = get_institution(record, data, filename)
				dat = get_date(record, data, filename)
				dat = get_level(record, data, filename, mapp)[0]

				write(dat[filename], output)
	print((dat))
 	#for key in dat.keys():
		#print(dat[key]['level'])

	#print (m)


def get_subjects(record, data, filename):
	for fieldNum in ['600', '610', '650', '651']:
		# if the desired field exists in this marc record, access it
		if fieldNum in record:
			# iterate over the subfield in this field
			for i, field in enumerate(record.get_fields(fieldNum)):	
				sub = 'subject' + str(i+1)
				data[filename]['subject'][sub] = []
				for subfield in field:
					# append this subfield value to the correct field data in the record bucket
					data[filename]['subject'][sub].append(subfield[1].replace('.', ''))
	return(data)

def get_title(record, data, filename):
	for fieldNum in ['245', '246']:
		# if the desired field exists in this marc record, access it
		if fieldNum in record:
			# iterate over the subfield in this field
			for field in record.get_fields(fieldNum):	
				for subfield in field:
					if subfield[0] == 'a' or subfield[0] == 'b':
					# append this subfield value to the correct field data in the record bucket
						data[filename]['title'].append(subfield[1].replace('.', ''))
	return(data)

def get_author(record, data, filename):
	for fieldNum in ['245', '100', '110']:
		# if the desired field exists in this marc record, access it
		if fieldNum in record:
			# iterate over the subfield in this field
			for field in record.get_fields(fieldNum):	
				for subfield in field:
					if (subfield[0] == 'a' or subfield[0] == 'b') and (fieldNum == '100' or fieldNum == '110'):
					# append this subfield value to the correct field data in the record bucket
						data[filename]['dissertant'].append(subfield[1].replace('.', ''))
					'''if len(data[filename]['dissertant']) == 0:
						if (subfield[0] == 'c') and (fieldNum == '245'):
							data[filename]['dissertant'].append(subfield[1].replace('.', ''))'''
	return(data)

def get_institution(record, data, filename):
	for fieldNum in ['710']:
		# if the desired field exists in this marc record, access it
		if fieldNum in record:
			# iterate over the subfield in this field
			for field in record.get_fields(fieldNum):	
				for subfield in field:
					if subfield[0] == 'b':
					# append this subfield value to the correct field data in the record bucket
						data[filename]['department'].append(subfield[1].replace('.', ''))
					if subfield[0] == 'a':
						if subfield[1] not in data[filename]['institution']:
							data[filename]['institution'].append(subfield[1].replace('.', ''))

	return(data)	

def get_date(record, data, filename):
	for fieldNum in ['260', "264"]:
		# if the desired field exists in this marc record, access it
		if fieldNum in record:
			# iterate over the subfield in this field
			for field in record.get_fields(fieldNum):
				for subfield in field:
					# append this subfield value to the correct field data in the record bucket
						if subfield[0] == 'c':
							data[filename]['graduation_date'].append(subfield[1])
	return(data)

def get_level(record, data, filename, mapp):
	for fieldNum in ['502']:
		# if the desired field exists in this marc record, access it
		if fieldNum in record:
			# iterate over the subfield in this field
			for field in record.get_fields(fieldNum):
				for subfield in field:
					# append this subfield value to the correct field data in the record bucket
						if subfield[0] == 'a':
							level = subfield[1].split('--')[0].replace('Thesis', '').replace('(', '').replace(')', '').replace('University of Alberta', '').replace('-', '').lstrip()
							level = re.sub(r'[0-9]+', '', level)
							#if level not in mapp:
							#	mapp.append(level)
							for i in thesisLevel:
								if level in i['mapping']: 
									data[filename]['level'].append(i['uri'])
									break
							if len(data[filename]['level']) == 0:
								data[filename]['level'].append(subfield[1])

	return(data, mapp)
def write(dat, output):
	for subject in dat['subject']:
			dat['subject'][subject] = '--'.join(dat['subject'][subject])
	#dat.append(dat)
	return(dat)


if __name__ == "__main__":
	main()
