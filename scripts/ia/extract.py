import os
import time 
import json
import requests
import internetarchive
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = "http://206.167.181.124:9999/blazegraph/namespace/gillingham_20180222/sparql"  # dev, 1 hour to transform

sparqlData = SPARQLWrapper(sparql)
sparqlData.setReturnFormat(JSON)
ERA_IDs = {}
query = "prefix dcterm: <http://purl.org/dc/terms/> prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix ual: <http://terms.library.ualberta.ca/id/> select ?item ?id where {?item ual:unicorn ?id; dcterm:type 'Thesis'^^xsd:string; <http://terms.library.ualberta.ca/identifiers/hasCollection> 'Theses and Dissertations'^^xsd:string . filter(?id != '')}"
sparqlData.setQuery(query)
results = sparqlData.query().convert()['results']['bindings']
for triple in results:
	ERA_IDs[triple['id']['value']] = triple['item']['value']

with open('ERA_IDs.json', 'w') as ERA:
	json.dump(ERA_IDs, ERA)

#s3 for Danoosh
from internetarchive import get_session
c = {'s3': {'access': 'C9khuFEwAKAj5Y5X', 'secret': '8s5NsWQzx1wTKfAd'}}
s = get_session(config=c)
s.access_key
'C9khuFEwAKAj5Y5X'

search = internetarchive.search_items('collection:ualberta_theses')

IA_IDs = {}
for i, result in enumerate(search):
    itemid = result['identifier']
    print (i, itemid)
    q = 'http://archive.org/metadata/' + itemid + '/metadata/call_number'
    r = requests.get(q).json()
    if 'result' not in r.keys():
    	q = 'http://archive.org/metadata/' + itemid + '/metadata/caltkey'
    	'''r = requests.get(q).json()
    	if 'result' in r.keys():
    		IA_IDs[r['result']] = itemid'''
    else:
    	IA_IDs[r['result']] = itemid

with open('IA_IDs.json', 'w') as IA:
	json.dump(IA_IDs, IA)

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

print (len(IA_only), len(overlaps))

os.chdir('files/')
for index, itemid in enumerate(IA_only.keys()):
	print (str(index) + ' of ' + str(len(IA_only)) + ' downloading' + str(itemid))
	item = internetarchive.get_item(itemid)
	marx = item.get_file(itemid + '_marc.xml')
	meta = item.get_file(itemid + '_meta.xml')
	marc = item.get_file(itemid + '_meta.mrc')
	marc.download()
	#meta.download()
