from requests import get
from requests import head
from SPARQLWrapper import JSON, SPARQLWrapper
from datetime import datetime
import time

ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')

sparqlData = "http://localhost:9999/blazegraph/namespace/gillingham_20180222/sparql" 
sparql = SPARQLWrapper(sparqlData)
splitBy = {}
'''with open("list.txt", "r") as file:
	l = []
	for line in file:
		if line.replace("\n", "") not in l:
			l.append(line.replace("\n", ""))'''

query = "prefix ualids: <http://terms.library.ualberta.ca/identifiers/> prefix fedora: <http://fedora.info/definitions/v4/repository#> prefix ldp: <http://www.w3.org/ns/ldp#> prefix dcterm: <http://purl.org/dc/terms/> prefix info: <info:fedora/fedora-system:def/model#> prefix ual: <http://terms.library.ualberta.ca/> SELECT distinct ?resource WHERE {?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type ?type . FILTER(str(?type) != 'Thesis'^^xsd:string) . FILTER (NOT EXISTS {?resource ualids:remote_resource 'dataverse'^^xsd:string})}"
sparql.setReturnFormat(JSON)
sparql.setQuery(query)
results = sparql.query().convert()['results']['bindings']
with open("out.txt", "w+") as file:
	for r in results:
		headers = {'Content-type': 'text/xml',}
		group = r['resource']['value'].split('/')[6]
		splitBy[group] = "/".join(r['resource']['value'].split('/')[:7])
	print (str(len(splitBy)) + " batches")
	i = 0
	for group in splitBy.keys():
		i = i + 1
		g = "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/" + group
		q = "prefix ualids: <http://terms.library.ualberta.ca/identifiers/> prefix fedora: <http://fedora.info/definitions/v4/repository#> prefix ldp: <http://www.w3.org/ns/ldp#> prefix dcterm: <http://purl.org/dc/terms/> prefix info: <info:fedora/fedora-system:def/model#> prefix ual: <http://terms.library.ualberta.ca/> SELECT distinct ?resource WHERE {?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type ?type . FILTER(str(?type) != 'Thesis'^^xsd:string && contains(str(?resource), '%s')) . FILTER (NOT EXISTS {?resource ualids:remote_resource 'dataverse'^^xsd:string})}" %(g)
		sparql.setQuery(q)
		result = sparql.query().convert()['results']['bindings']
		for re in result:
			response = head(re['resource']['value'].replace('gillingham', 'mycombe2'), headers=headers, auth=('fedoraAdmin', 'HN4di2015'))
			if str(response) != '<Response [200]>':
				file.write(re['resource']['value'].replace('gillingham', 'mycombe2') + "\t" + str(response) + "\n")
		tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
		print("walltime for " + group + " batch number: " + str(i) + " of " + str(len(splitBy)), datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))


