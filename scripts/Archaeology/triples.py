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
from archFinal_triples import main as csv_gen

def main():
	csv_file = 'batchArchaelogy-%s.csv' %(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	csv_gen(csv_file)
	itemType = 'http://purl.org/ontology/bibo/Image'
	visibility = 'http://terms.library.ualberta.ca/public'
	collection = 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/44/55/8t/46/44558t46k'
	base = 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/'
	contributor1 = 'Bryan, Alan L., Dr.'
	contributor2 = 'Gruhn, Dr. Ruth'
	#create a dict for creators from ImageData
	creators = get_creator()
	uuids = get_Jupiter_UUIDs()
	with open(csv_file, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			creator = ''
			uu_id = generate_uuid(uuids)
			file = row['fileName']
			# extract a 4-digit year from filename
			sort_year = get_sortYear(file)
			description = row['description']
			title = row['title']
			subject = row['subject'].split('|')
			dateCreated = row['dateCreated']
			rights = row['rights'].replace('© ', '')
			language = row['language']
			spatial = row['spatial'].split('|')
			if file in creators.keys():
				creator = creators[file]
			else:
				creator = row['creator'].replace('© ', '')

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
				filename.add((s, URIRef('http://purl.org/dc/terms/spatial'), Literal(spat)))
			filename.add((s, URIRef('http://purl.org/dc/elements/1.1/contributor'), Literal(contributor1)))
			filename.add((s, URIRef('http://purl.org/dc/elements/1.1/contributor'), Literal(contributor2)))
			filename.add((s, URIRef('info:fedora/fedora-system:def/model#hasModel'), Literal('IRItem')))
			filename.add((s, URIRef('http://purl.org/ontology/bibo/owner'), Literal('eraadmi@ualberta.ca')))
			if sort_year != None:
				filename.add((s, URIRef('http://terms.library.ualberta.ca/sortYear'), Literal(sort_year)))
				filename.add((s, URIRef('http://purl.org/dc/terms/created'), Literal(sort_year)))
			elif dateCreated != '':
				sort_year = get_sortYear(dateCreated)
				filename.add((s, URIRef('http://purl.org/dc/terms/created'), Literal(dateCreated)))
				filename.add((s, URIRef('http://terms.library.ualberta.ca/sortYear'), Literal(sort_year)))
			if creator != '':
				filename.add((s, URIRef('http://purl.org/dc/elements/1.1/creator'), Literal(creator)))
			folder = 'triples'
			output = "%s/%s.nt" %(folder, file)
			print (output)
			if not exists(folder):
				makedirs(folder)
			filename.serialize(destination=output, format='nt')

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
		print ('error')

def generate_uuid(uuids):
	#if the UUID exists in Jupiter, generate a new one
	try:
		uu_id = str(uuid.uuid4())
		if uu_id not in uuids:
			return (uu_id)
		else:
			generate_uuid(uuids)
	except:
		print ('error')

def get_sortYear(filename):
	sortYear = re.search('\d{4}$', filename)
	if sortYear:
		return (sortYear.group(0))
	else:
		sortYear = re.search('\d{4}$', filename.split('-')[0])
		if sortYear:
			return (sortYear.group(0))

def get_creator():
	imageData = {}
	with open ('output.txt', 'r') as f: 
		metadata = f.readline()
		for line in f:
			if 'Image:' in line:
				image = resolveNames(line, 'imageData')
			if 'Byline[2,80]' in line:
				temp = re.sub("\\n","",re.sub("(^.\s+)","",line, re.MULTILINE))
				imageData[image]= re.sub('Byline\[2,80\]: ','',temp)
	return (imageData)

def resolveNames(objectName,Type):
    match = ''
    flag = 'T'
    #strips, cases, and removes path & extension from filename 
    objectName = objectName.lower().strip()
    objectName = re.search('(.+/{1}|(^))(.+)\.tif',objectName).group(3)
    #converts all names from inconsistent use of dashes and period delimiters to a consistant use of dash delimiters
    objectName = re.sub('([.]+)','-',objectName)
    #strips any trailing underscores
    if objectName.endswith('_'): objectName = objectName.rstrip('_')
    #catch-all regex for resolving object names according to 11 existing name variations. If names were passed directly, 
    #we would not be able to treat file names as unique identifiers for use in the database. With an updated mimsy 
    #database, new failed mimsy matches will require adjustments or additions to this regex. Consider it the botteneck in 
    #the script.
    resolvedObjectName = re.search('(^[-.0-9]+[_]?[0-9]?)$|(^[-.0-9]{12}[_|rl]*)$|(^[-.0-9]{12}[ab]*_d)$|(^[-.0-9]+[-_a-z]*)_[vs][0-9][0-9]*|(^[-+0-9]{12}_\w)[_\W]|(.+lot)|(^[0-9][0-9]?-[0-9][0-9]?$)|(589-[-0-9]{7}_\D)|(2011_1_1)production_3years_aug93|(.+[.]pdf)|(^(2005|2011).+)|(^[-.0-9]+[_]?[\D]?[_]?[\D])[\D]*$|^[-0-9]_and.*',objectName)
    #tests that the regex resolved the name for one of the 11 known matches and passes the match on, otherwise throws a 
    #message
    if resolvedObjectName:
        flag = 'F'
        for i in range(1,14):
            if resolvedObjectName.group(i) is not None: 
                flag = 'T'
                match = resolvedObjectName.group(i)
    if flag == 'F': print(objectName)
    return match

if __name__ == "__main__":
	main()