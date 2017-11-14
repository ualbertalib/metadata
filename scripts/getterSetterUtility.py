"""A utility for moving data from one triplestore to another"""

from SPARQLWrapper import JSON, SPARQLWrapper
from rdflib import URIRef, Literal, Graph
import requests
import os

origin = SPARQLWrapper("http://example.org")
origin.setReturnFormat(JSON)
graph = Graph()
for triple in LIST_OF_TRIPLES:
	query = "construct {{<{}> ?p ?o}} where {{<{}> ?p ?o}}".format(triple['subject'], triple['subject'])
	origin.setQuery(query)
	results = origin.query().convert()
	for result in results['results']['bindings']:
		if result['object']['type'] == 'literal':
			graph.add((URIRef(result['subject']['value']), URIRef(result['predicate']['value']), Literal(result['object']['value'])))
		elif result['object']['type'] == 'uri':
			graph.add((URIRef(result['subject']['value']), URIRef(result['predicate']['value']), URIRef(result['object']['value'])))
graph.serialize(destination='temp.nt', format='nt')
requests.post(url="http://example.org", files={'file': open('temp.nt', 'rb')}, headers={'Content-Type': 'text/turtle'})
os.remove('temp.nt')
