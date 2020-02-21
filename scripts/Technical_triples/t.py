import requests
from Passwords import passwords
import re
from SPARQLWrapper import JSON, SPARQLWrapper, RDFXML, N3

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
} limit 200"""
sparqlData.setQuery(query)  # set the query
results = sparqlData.query().convert()
for i, result in enumerate(results['results']['bindings']):
	fixity = None
	subject = result['s']['value'].replace('mycombe', 'gillingham2')
	fixity = result['o']['value'].replace('mycombe', 'gillingham2')
	response = requests.get(fixity, headers=headers, auth=(user, passwd)).text
	matched = re.search("#fixity/\S+", response)
	if matched:
		print (response.replace(matched.group(), '#fixity>'))
