import requests
from Passwords import passwords
import re
from SPARQLWrapper import JSON, SPARQLWrapper, RDFXML, N3
from time import sleep

passwd = passwords['gillingham2'][1]
user = passwords['gillingham2'][0]

headers = {'Content-type': 'application/n-triples'}

sparql = "http://triplestore.library.ualberta.ca:8080/repositories/fedora"
sparqlData = SPARQLWrapper(sparql)
sparqlData.setReturnFormat(JSON)

query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX dcterms: <http://purl.org/dc/terms/>
select distinct ?s ?o where { 
	?s <http://fedora.info/definitions/v4/repository#hasFixityService> ?o.
} limit 500000"""
sparqlData.setQuery(query)  # set the query
results = sparqlData.query().convert()
for i, result in enumerate(results['results']['bindings']):
	print ("processing %s of %s" %(i+1, len(results['results']['bindings'])))
	fixity = None
	subject = result['s']['value'].replace('mycombe', 'gillingham2')
	fixity = result['o']['value'].replace('mycombe', 'gillingham2')
	fresponse = requests.get(fixity, headers=headers, auth=(user, passwd)).text
	mresponse = requests.get(fixity.replace('fixity', 'metadata'), headers=headers, auth=(user, passwd)).text
	fmatched = re.search("#fixity/\S+", fresponse)
	if fmatched:
		print ("writing %s fixity" %(subject.split('/')[-1]))
		with open('fixity/%s.ttl' %(subject.split('/')[-1]), 'w') as file:
			file.write(fresponse.replace(fmatched.group(), '/fcr:fixity>').replace('premis:hasFixity', 'fedora:hasFixityService').replace('gillingham2', 'mycombe'))
			file.close()
	else:
		with open('fixity/fixity.log', 'a+') as fixlog:
			fixlog.write("no fixity reponse for %s\n" %(subject.split('/')[-1]))
			fixlog.close()
	if mresponse != '':
		print ("writing %s metadata" %(subject.split('/')[-1]))
		with open('metadata/%s.ttl' %(subject.split('/')[-1]), 'w') as mfile:
			mfile.write(mresponse.replace('gillingham2', 'mycombe'))
			mfile.close()
	else:
		with open('metadata/metadata.log', 'a+') as mlog:
			mlog.write("no metadata reponse for %s\n" %(subject.split('/')[-1]))
			mlog.close()
	sleep(1)

