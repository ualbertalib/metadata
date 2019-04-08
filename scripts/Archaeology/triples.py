import csv
import uuid
import re
import requests
import json
import time
from datetime import datetime
from rdflib import Graph, URIRef, Literal
from os import listdir, getcwd, chdir, makedirs
from os.path import isfile, join, exists
from archFinal2 import main as csv_gen

def main():
	files = []
	che = {}
	csv_file = 'batchArchaelogy-%s.csv' %(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	csv_gen(csv_file)
	itemType = 'http://purl.org/ontology/bibo/Image'
	language = 'No linguistic content'
	visibility = 'http://terms.library.ualberta.ca/public'
	collection = 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/bc/f5/86/ac/bcf586ac-ab61-49e1-839f-b9f517839e9e'
	community = 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/01/7b/59/83/017b5983-6bca-47d1-9760-0435ed3aedd8'
	base = 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat'
	default_contributor1 = 'Dr. Bryan, Alan L'
	default_contributor2 = 'Dr. Gruhn, Ruth'
	default_creator = 'University of Alberta, Department of Anthropology'
	default_rights = 'u"\u00A9" University of Alberta, Department of Anthropology'

	uuids = get_Jupiter_UUIDs()
	with open(csv_file, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			spatial = ''
			temporal = ''
			contributor = ''
			maker = ''
			dateCreated = ''
			description = ''
			title = ''
			subject = ''
			uu_id = generate_uuid(uuids)
			file = row['fileName']
			#check for duplicates
			if file not in files:
				files.append(file)
			else:
				if file not in che.keys():
					che[file] = 1
				else:
					che[file] += 1
			# extract a 4-digit year from filename
			dateCreated = row['dateCreated']
			if dateCreated != '':
				sort_year = get_sortYear(dateCreated)
			else:
				sort_year = get_sortYear(file)
				dateCreated = sort_year
			description = row['description']
			title = row['title']
			subject = row['subject'].split('|')
			if row['rights'] != '':
				rights = row['rights']
			else:
				rights = default_rights
			if row['contributor'] != '':
				contributor = row['contributor'].split(';')
			if row['maker'] != '' and row['maker'] != 'unknown':
				maker = row['maker']
			if row['spatial'] != '':
				spatial = row['spatial'].split('|')
			if row['temporal'] != '|':
				temporal = row['temporal'].split('|')
			if row['creator'] != '':
				creator = row['creator'].replace('© ', '')
			else:
				creator = default_creator

			s = URIRef('%s/%s/%s/%s/%s/%s' %(base, uu_id[0:2], uu_id[2:4], uu_id[4:6], uu_id[6:8], uu_id))
			#create a Graph for the item
			filename = Graph()
			#add Model
			filename.add((s, URIRef('http://purl.org/dc/terms/title'), Literal(title)))
			#add collection triple
			filename.add((s, URIRef('http://pcdm.org/models#memberOf'), URIRef(collection)))
			#add accessRights
			filename.add((s, URIRef('http://purl.org/dc/terms/accessRights'), URIRef(visibility)))
			#add depositor triple
			filename.add((s, URIRef('http://terms.library.ualberta.ca/depositor'), Literal('era@ualberta.ca')))
			filename.add((s, URIRef('http://purl.org/dc/terms/language'), Literal(language)))
			#add license triple
			filename.add((s, URIRef('http://purl.org/dc/elements/1.1/rights'), Literal(rights)))
			filename.add((s, URIRef('http://purl.org/dc/terms/description'), Literal(description)))
			filename.add((s, URIRef('http://purl.org/dc/terms/type'), URIRef(itemType)))
			#add subject
			for sub in subject:
				filename.add((s, URIRef('http://purl.org/dc/elements/1.1/subject'), Literal(sub)))
			for spat in spatial:
				if len(spat) > 0:
					filename.add((s, URIRef('http://purl.org/dc/terms/spatial'), Literal(spat)))
			for temp in temporal:
				if len(temp) > 0:
					filename.add((s, URIRef('http://purl.org/dc/terms/temporal'), Literal(temp)))
			#filename.add((s, URIRef('http://purl.org/dc/elements/1.1/contributor'), Literal(default_contributor1)))
			#filename.add((s, URIRef('http://purl.org/dc/elements/1.1/contributor'), Literal(default_contributor2)))
			if contributor != '':
				for con in contributor:
					filename.add((s, URIRef('http://purl.org/dc/elements/1.1/contributor'), Literal(con)))
			if maker != '' and maker not in contributor:
				filename.add((s, URIRef('http://purl.org/dc/elements/1.1/contributor'), Literal(maker)))
			filename.add((s, URIRef('info:fedora/fedora-system:def/model#hasModel'), Literal('IRItem')))
			filename.add((s, URIRef('http://purl.org/ontology/bibo/owner'), Literal('eraadmi@ualberta.ca')))
			if dateCreated != '':
				filename.add((s, URIRef('http://terms.library.ualberta.ca/sortYear'), Literal(sort_year)))
				filename.add((s, URIRef('http://purl.org/dc/terms/created'), Literal(dateCreated)))
			if creator != '':
				filename.add((s, URIRef('http://purl.org/dc/elements/1.1/creator'), Literal(creator)))
			folder = 'triples'
			output = "%s/%s.nt" %(folder, file)
			if not exists(folder):
				makedirs(folder)
			filename.serialize(destination=output, format='nt')
	print (len(che))

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
		print ('error getting Jupiter UUIDs from solr')

def generate_uuid(uuids):
	#if the UUID exists in Jupiter, generate a new one
	try:
		uu_id = str(uuid.uuid4())
		if uu_id not in uuids:
			return (uu_id)
		else:
			generate_uuid(uuids)
	except:
		print ('error generating UUID')

def get_sortYear(filename):
	sortYear = re.search('\d{4}$', filename)
	if sortYear:
		return (sortYear.group(0))
	else:
		sortYear = re.search('\d{4}$', filename.split('-')[0])
		if sortYear:
			return (sortYear.group(0))

if __name__ == "__main__":
	main()