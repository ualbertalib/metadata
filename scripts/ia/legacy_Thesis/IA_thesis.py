import re
from os import listdir, getcwd, chdir, makedirs
from os.path import isfile, join, exists
import pymarc
import json
import time
from datetime import datetime
import requests
from extract import get_files
from rdflib import Graph, URIRef, Literal
from config import degree_level, thesisLevel, Jupiter_predicates, institution, mypath, fedora, collection, PrintException
import uuid

work_dir = getcwd() 
#download files that are not in Jupiter (and have catkey) form Ineternet Archives
#get_files(work_dir)
chdir(work_dir)

def main():
	output = []
	data = {}
	mapp = []
	uuids = get_Jupiter_UUIDs()
	departments = get_department()
	for filename in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
		try:
			with open(join(mypath, filename), 'rb') as xml:
				filename = filename.replace('_marc.xml', '')
				reader = pymarc.marcxml.parse_xml_to_array(xml)
				#a place to store the fieldData
				data[filename] = {
							'title': [],
							'subject': {},
							'graduation_date': [],
							'dissertant': [],
							'department': [],
							'institution': [],
							'level': [],
							'degree': [],
							'unicorn': [],
							'abstract': []
							}
				#get requried fields form each record
				for record in reader:
					dat = get_notes(record, data, filename)
					dat = get_title(record, data, filename)
					dat = get_author(record, data, filename)
					dat = get_subjects(record, data, filename)
					dat = get_institution(record, data, filename)[0]
					dep = get_institution(record, data, filename)[1]
					dat = get_date(record, data, filename)
					dat = get_unicorn(record, data, filename)
					dat = get_level(record, data, filename)
					if len(dat[filename]['degree']) == 0:
						dat = get_degree(record, data, filename, dep, departments)
			#print (data)
		except:
			PrintException()
	#create triples and write to file
	for item in dat.keys():
		try:
			#generate a random UUID
			uu_id = generate_uuid(uuids)
			s = URIRef('%s/%s/%s/%s/%s/%s' %(fedora, uu_id[0:2], uu_id[2:4], uu_id[4:6], uu_id[6:8], uu_id))
			filename = s[0:10]
			download_link = "https://ia800101.us.archive.org/11/items/%s/%s.pdf" %(item, item)
			#create a Graph for the item
			filename = Graph()
			for key in dat[item].keys():
				for mapp in Jupiter_predicates:
					if key in mapp["mapping"]:
						p = URIRef(mapp["uri"])
				if isinstance(dat[item][key], list) and len(dat[item][key]) > 0:
					obj = dat[item][key][0]
					#print (obj)
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
				#add license triple
				filename.add((s, URIRef('http://purl.org/dc/elements/1.1/rights'), Literal('This thesis is made available by the University of Alberta Libraries with permission of the copyright owner solely for non-commercial purposes. This thesis, or any portion thereof, may not otherwise be copied or reproduced without the written consent of the copyright owner, except to the extent permitted by Canadian copyright law.')))
				#add Internet Archives ID
				filename.add((s, URIRef('http://terms.library.ualberta.ca/internetarchive'), Literal(download_link)))
			folder = 'triples'
			output = "%s/%s.nt" %(folder, item)
			if not exists(folder):
				makedirs(folder)
			filename.serialize(destination=output, format='nt')
		except:
			PrintException()

def get_subjects(record, data, filename):
	for fieldNum in ['600', '610', '650', '651']:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for i, field in enumerate(record.get_fields(fieldNum)):	
					sub = 'subject' + str(i+1)
					data[filename]['subject'][sub] = []
					for subfield in field:
						#append this subfield value to the correct field data in the record bucket
						data[filename]['subject'][sub].append(subfield[1].replace('.', ''))
		except:
			PrintException()
	return(data)

def get_title(record, data, filename):
	for fieldNum in ['245', '246']:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for field in record.get_fields(fieldNum):	
					for subfield in field:
						if subfield[0] == 'a' or subfield[0] == 'b':
						#append this subfield value to the correct field data in the record bucket
							data[filename]['title'].append(subfield[1].replace('.', ''))
		except:
			PrintException()
	return(data)

def get_author(record, data, filename):
	for fieldNum in ['100', '110', '245']:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for field in record.get_fields(fieldNum):	
					for subfield in field:
						if (subfield[0] == 'a' or subfield[0] == 'b') and (fieldNum == '100' or fieldNum == '110'):
						#append the dissertant value
							data[filename]['dissertant'].append(subfield[1].replace('.', ''))
					#if the value could not be found in 100 or 110 then access it from the 245$c
					if len(data[filename]['dissertant']) == 0:
						if (subfield[0] == 'c') and (fieldNum == '245'):
							data[filename]['dissertant'].append(subfield[1].replace('.', ''))
		except:
			PrintException()
	return(data)

def get_institution(record, data, filename):
	department = ''
	for fieldNum in ['710']:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for field in record.get_fields(fieldNum):	
					for subfield in field:
						if subfield[0] == 'b':
						#append the department
							department = subfield[1].replace('Dept', 'Department').replace('.', '')
							data[filename]['department'].append(subfield[1].replace('.', ''))
						#append the institution 
						if subfield[0] == 'a':
							if subfield[1] not in data[filename]['institution']:
								data[filename]['institution'].append(subfield[1].replace('.', ''))
		except:
			PrintException()
	return(data, department)	

def get_date(record, data, filename):
	for fieldNum in ['260', "264"]:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for field in record.get_fields(fieldNum):
					for subfield in field:
						#appending the date field (graduation date)
							if subfield[0] == 'c':
								date = re.sub(r'[\[/\]/\./\?]+', '', subfield[1])
								if date[-1] == '-':
									date = date.replace('-', '0')
								data[filename]['graduation_date'].append(date)
		except:
			PrintException()
	return(data)

def get_unicorn(record, data, filename):
	for fieldNum in ['001']:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for field in record.get_fields(fieldNum):
					#appending the date field (unicorn)
					data[filename]['unicorn'].append(str(field).replace('=001  ', ''))
		except:
			PrintException()
	return(data)

def get_level(record, data, filename):
	for fieldNum in ['502']:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for field in record.get_fields(fieldNum):
					for subfield in field:
						# append this subfield value to the correct field data in the record bucket
							if subfield[0] == 'a':
								#remove extra text from the subfield 
								level = subfield[1].split('--')[0].replace('Thesis', '').replace('(', '').replace(')', '').replace('University of Alberta', '').replace('-', '').lstrip()
								level = re.sub(r'[0-9]+', '', level).lstrip()
								#print ('1', level)
								##generate thesis level mapping##
								#if level not in mapp:
								#mapp.append(level)
								for i in thesisLevel:
									#if the mapping exists use the uri
									if level in i['mapping']: 
										data[filename]['level'].append(i['uri'])
								if len(data[filename]['level']) == 0:
									data[filename]['level'].append(subfield[1])
		except:
			PrintException()

	return(data)

def get_degree(record, data, filename, department, departments):
	for fieldNum in ['502']:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for field in record.get_fields(fieldNum):
					for subfield in field:
						# append this subfield value to the correct field data in the record bucket
							if subfield[0] == 'a' or  subfield[0] == 'b':
								#remove extra text from the subfield 
								level = subfield[1].split('--')[0].replace('Thesis', '').replace('(', '').replace(')', '').replace('University of Alberta', '').replace('-', '').lstrip()
								level = re.sub(r'[0-9]+', '', level).lstrip()
								for i in degree_level:
									if level in i['mapping']:
										#if the mapping exists use the useForm
										data[filename]['degree'].append(i['useForm'])
										break
								#If degree was not in mappings, use the degree levels for the deparment
								if len(data[filename]['degree']) == 0:
									for i in thesisLevel:
										if level in i['mapping']: 
											if department != '':
												for key in departments.keys():
													if department in key:
														for n, deg in enumerate(departments[key]):
															if i['useForm'] in deg:
																degree = departments[key][n]
																data[filename]['degree'].append(degree)
																break
								if len(data[filename]['degree']) == 0:
									data[filename]['degree'].append(subfield[1])
		except:
			PrintException()

	return(data)

def get_notes(record, data, filename):
	for fieldNum in ["500"]:
		#if the desired field exists in this marc record, access it
		try:
			if fieldNum in record:
				#iterate over the subfield in this field
				for field in record.get_fields(fieldNum):
					for subfield in field:
						#appending the date field (graduation date)
							if subfield[0] == 'a':
								if 'for the degree of' in subfield[1]:
									data[filename]['degree'].append((subfield[1].split('for the degree of ')[1]).split(',')[0])
		except:
			PrintException()
	return(data)

def get_Jupiter_UUIDs():
	#query Jupiter solr for all UUIDs (community, collection, Item and thesis)
	try:
		response = requests.get('http://solrcloud.library.ualberta.ca:8080/solr/jupiter/select?fl=id&fq=has_model_ssim:("IRCommunity" OR "IRCollection" OR "IRItem" OR "IRThesis")&indent=on&q=id:*&rows=10000&wt=json').json()
		jupiter_items = response['response']['numFound']
		print ('As of %s there are %s items in Jupiter' % (datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), jupiter_items))
		uuids = []
		for item in response['response']['docs']:
			if item['id'] not in uuids:
				uuids.append(item['id'])

		return (uuids)
	except:
		PrintException()

def generate_uuid(uuids):
	#if the UUID exists in Jupiter, generate a new one
	try:
		uu_id = str(uuid.uuid4())
		if uu_id not in uuids:
			return (uu_id)
		else:
			generate_uuid(uuids)
	except:
		PrintException()

def get_department():
	department_levels = {}
	try:
		response = requests.get('http://solrcloud.library.ualberta.ca:8080/solr/jupiter/select?fl=departments_tesim AND degree_ssim&fq=degree_ssim:[* TO *] AND departments_tesim:[* TO *]&indent=on&q=id:*&rows=10000&wt=json').json()
		jupiter_items = response['response']['numFound']
		for item in response['response']['docs']:
			if item['departments_tesim'][0] not in department_levels.keys():
				department_levels[item['departments_tesim'][0]] = []
				department_levels[item['departments_tesim'][0]].append(item['degree_ssim'][0])
			else:
				if item['degree_ssim'][0] not in department_levels[item['departments_tesim'][0]]:
					department_levels[item['departments_tesim'][0]].append(item['degree_ssim'][0])

		return(department_levels)
	except:
		PrintException()

if __name__ == "__main__":
	main()
