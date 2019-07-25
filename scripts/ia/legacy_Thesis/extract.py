from os import listdir, getcwd, chdir, makedirs
from os.path import isfile, join, exists
import time
from datetime import datetime
import json
import requests
import internetarchive
from SPARQLWrapper import SPARQLWrapper, JSON
from config import sparql, IA_access, file_type, PrintException
from internetarchive import get_session

def get_files(work_dir):
	NOIDs=pull_NOIDs()
	IA_ID=search_IA()
	ovlist=generate_overlap_list(NOIDs, IA_ID)
	download(ovlist, file_type, work_dir)

def pull_NOIDs():
	sparqlData = SPARQLWrapper(sparql)
	sparqlData.setReturnFormat(JSON)
	ERA_IDs = {}
	query = "prefix dcterm: <http://purl.org/dc/terms/> prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix ual: <http://terms.library.ualberta.ca/id/> select ?item ?id where {?item ual:unicorn ?id; dcterm:type 'Thesis'^^xsd:string; <http://terms.library.ualberta.ca/identifiers/hasCollection> 'Theses and Dissertations'^^xsd:string . filter(?id != '')}"
	sparqlData.setQuery(query)
	results = sparqlData.query().convert()['results']['bindings']
	for triple in results:
		ERA_IDs[triple['id']['value']] = triple['item']['value']
	print ('As of %s there are %s thesis with unicorn in triplestore' % (datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), len(ERA_IDs)))
	#write to file
	with open('ERA_IDs.json', 'w') as ERA:
		json.dump(ERA_IDs, ERA)

	return (ERA_IDs)

def search_IA():
	#authenticate to Internet Archives
	s = get_session(config=IA_access)
	s.access_key
	'C9khuFEwAKAj5Y5X'
	#search IA/ualberta thesis collection
	search = internetarchive.search_items('collection:ualberta_theses')
	print ('As of %s there are %s items in thesis collection of Internet Archives' % (datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), len(search)))
	json_file = open('IA_only.json')
	json_str = json_file.read()
	json_data = json.loads(json_str)
	print ('%s items of %s are already downloaded -- Skipping metadata search for these items' %(len(json_data), len(search)))
	IA_IDs = {}
	No_CatKey = []
	for i, result in enumerate(search):
	    itemid = result['identifier']
	    if itemid in json_data.keys():
	    	print ('skipping metadata search for %s' %(itemid))
	    	IA_IDs[json_data[itemid]] = itemid
	    else:
		    print ('searching metadata in item %s of %s -- item ID: %s' %(i+1, len(search), itemid))
		    #search for call_numbers
		    q = 'http://archive.org/metadata/' + itemid + '/metadata/call_number'
		    r = requests.get(q).json()
		    if 'result' not in r.keys():
		    	#if field call_number was not found, search for catkey
		    	q = 'http://archive.org/metadata/' + itemid + '/metadata/caltkey'
		    	r = requests.get(q).json()
		    	if 'result' in r.keys():
		    		IA_IDs[r['result']] = itemid
		    	else:
		    		No_CatKey.append(itemid)
		    else:
		    	IA_IDs[r['result']] = itemid
	#write to file
	with open('IA_IDs.json', 'w') as IA:
		json.dump(IA_IDs, IA)
	#items in IA that does not have CatKey/CallNumber are ignored in this proce
	with open('No_CatKey.json', 'w') as No_Cat:
		json.dump(No_CatKey, No_Cat)
	return(IA_IDs)

def generate_overlap_list(ERA_IDs, IA_IDs):
	overlaps = {}
	IA_only = {}
	for id in IA_IDs.keys():
		if id in ERA_IDs.keys():
			overlaps[id] = {}
			overlaps[id]['IA_key'] = IA_IDs[id]
			overlaps[id]['ERA_key'] = ERA_IDs[id]
		else:
			IA_only[IA_IDs[id]] = id

	with open('overlaps.json', 'w') as over:
		json.dump(overlaps, over)

	with open('IA_only.json', 'w') as IAonly:
		json.dump(IA_only, IAonly)

	print ('There are %s thesis that are only in Internet Archives -- %s thesis are in IA and Triplestore' %(len(IA_only), len(overlaps)))
	return (IA_only)

def download(IA_only, file_type, work_dir):
	for i in file_type:
		filetype = i.replace('_marc.', '').replace('_meta.', '').replace('_djvu.', '').replace('.', '')
		print (filetype)
		print ('getting %s files' %(filetype))
		folder = 'files/%s' %(filetype)
		if not exists(folder):
			makedirs(folder)
		chdir(folder)
		for index, itemid in enumerate(IA_only.keys()):
			filename = itemid + i
			if isfile(filename):
				print ('%s of type %s is in folder -- skipping download' %(itemid, filetype))
			else:
				print (str(index+1) + ' of ' + str(len(IA_only)) + ' downloading ' + str(itemid) + ' -- format: ' + str(filetype))
				item = internetarchive.get_item(itemid)
				file = item.get_file(itemid + i)
				try:
					file.download()
				except:
					PrintException()
		chdir(work_dir)
			
if __name__ == "__main__":
	get_files()

