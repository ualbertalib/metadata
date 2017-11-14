from config import dates
from SPARQLWrapper import JSON, SPARQLWrapper
from rdflib import URIRef, Literal, Graph
import requests
import os

origin = SPARQLWrapper("http://sheff.library.ualberta.ca:9999/blazegraph/namespace/gillingham_2/sparql")
origin.setReturnFormat(JSON)
graph = Graph()
for triple in dates:
	query = "construct {{<{}> ?p ?o}} where {{<{}> ?p ?o}}".format(triple['subject'], triple['subject'])
	origin.setQuery(query)
	results = origin.query().convert()
	for result in results['results']['bindings']:
		if result['object']['type'] == 'literal':
			graph.add((URIRef(result['subject']['value']), URIRef(result['predicate']['value']), Literal(result['object']['value'])))
		elif result['object']['type'] == 'uri':
			graph.add((URIRef(result['subject']['value']), URIRef(result['predicate']['value']), URIRef(result['object']['value'])))
graph.serialize(destination='temp.nt', format='nt')
#requests.post(url="http://206.167.181.123:9999/blazegraph/namespace/dates/sparql", files={'file': open('temp.nt', 'rb')}, headers={'Content-Type': 'text/turtle'})
#os.remove('temp.nt')