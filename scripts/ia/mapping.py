import re
from os import listdir
from os.path import isfile, join
import pymarc
import json
from rdflib import Graph, URIRef, Literal
import uuid

thesisLevel = [
	{"uri": "http://purl.org/spar/fabio/BachelorsThesis",
	"mapping": ["B.Ed.", "B. Ed.", "B. Div.", "B.Div.", "B.D."]},
	{"uri": "http://purl.org/spar/fabio/MastersThesis",
	"mapping": ["Master's", 'Master', 'M. Sc.', 'M.A.', 'M.Ed.', 'M.A.', 'M.Sc.', 'M.A', 'M.Sc. ', 'M. Ed.', 'MSc.', 'M.S. ', 'M.S.']},
	{"uri": "http://purl.org/spar/fabio/DoctoralThesis",
	"mapping": ["Doctoral", "Ph.D.", "Ph. D.", "PhD"]}]

Jupiter_predicates = [{"uri": "http://purl.org/dc/terms/title",
	"mapping": ["title"]},
	{"uri": "http://terms.library.ualberta.ca/graduationDate",
	"mapping": ["graduation_date"]},
	{"uri": "http://terms.library.ualberta.ca/dissertant",
	"mapping": ["dissertant"]},
	{"uri": "http://terms.library.ualberta.ca/department",
	"mapping": ["department"]},
	{"uri": "http://ontoware.org/swrc/ontology#institution",
	"mapping": ["institution"]},
	{"uri": "http://terms.library.ualberta.ca/thesisLevel",
	"mapping": ["level"]},
	{"uri": "http://purl.org/dc/elements/1.1/subject",
	"mapping": ["subject"]}]

institution = [{"uri": "http://id.loc.gov/authorities/names/n79058482",
	"mapping": ["University of Alberta", "U of A"]},
	{"uri": "http://id.loc.gov/authorities/names/n2009054054",
	"mapping": ["St. Stephen's College"]}]

fedora = "http://mycombe.library.ualberta.ca:8080/fedora/rest/prod"
collection = "http://mycombe.library.ualberta.ca:8080/fedora/rest/prod/44/55/8t/41/44558t416"


def main():
	mypath = "/home/danydvd/git/remote/metadata/scripts/ia/files/xml/"
	output = []
	data = {}
	mapp = []
	for filename in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
		with open(join(mypath, filename), 'rb') as xml:
			filename = filename.replace('_marc.xml', '')
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
				# iterate over all desired fields (each one represents one of the arrays in fieldData)
				write(dat[filename], output)
	print(dat)
	#for key in dat.keys():
		#print(dat[key]['level'])

	#print (m)

	g = Graph()

	for item in dat.keys():
		#generate a random UUID
		uu_id = str(uuid.uuid4())
		s = URIRef('%s/%s/%s/%s/%s/%s' %(fedora, uu_id[0:2], uu_id[2:4], uu_id[4:6], uu_id[6:8], uu_id))
		filename = s[0:10]
		#create a Graph for the item
		filename = Graph()
		for key in dat[item].keys():
			for mapp in Jupiter_predicates:
				if key in mapp["mapping"]:
					p = URIRef(mapp["uri"])
			if isinstance(dat[item][key], list) and len(dat[item][key]) > 0:
				obj = dat[item][key][0]
				for mapp in institution:
					if obj in mapp['mapping']:
						obj = mapp["uri"]
				if 'http://' in obj:
					o = URIRef(obj)
				else:
					o = Literal(obj)
				filename.add((s, p, o))
			elif isinstance(dat[item][key], dict):
				for k in dat[item][key].keys():
					o = Literal(dat[item][key][k])
					filename.add((s, p, o))
			#add Model
			filename.add((s, URIRef('info:fedora/fedora-system:def/model#hasModel'), Literal('IRThesis')))
			#add collection triple
			filename.add((s, URIRef('http://pcdm.org/models#memberOf'), URIRef(collection)))
			#add accessRights
			filename.add((s, URIRef('http://purl.org/dc/terms/accessRights'), URIRef('http://terms.library.ualberta.ca/public')))
			#add depositor triple
			filename.add((s, URIRef('http://terms.library.ualberta.ca/depositor'), Literal('era@ualberta.ca')))
		output = "out/%s.nt" %(uu_id)
		filename.serialize(destination=output, format='nt')
		




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
	for fieldNum in ['100', '110', '245']:
		# if the desired field exists in this marc record, access it
		if fieldNum in record:
			# iterate over the subfield in this field
			for field in record.get_fields(fieldNum):	
				for subfield in field:
					if (subfield[0] == 'a' or subfield[0] == 'b') and (fieldNum == '100' or fieldNum == '110'):
					# append this subfield value to the correct field data in the record bucket
						data[filename]['dissertant'].append(subfield[1].replace('.', ''))
				if len(data[filename]['dissertant']) == 0:
					if (subfield[0] == 'c') and (fieldNum == '245'):
						data[filename]['dissertant'].append(subfield[1].replace('.', ''))
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
