from SPARQLWrapper import JSON, SPARQLWrapper
import re
from rdflib import URIRef, Literal, Graph
sparqlData = "http://206.167.181.123:9999/blazegraph/namespace/terms/sparql"
sparqlData = SPARQLWrapper(sparqlData)
sparqlData.setReturnFormat(JSON)
for subgraph in ['community', 'collection', 'generic', 'thesis', 'oai_pmh', 'oai_etdms', 'instances']:
	sparqlData.setQuery("prefix ual: <http://terms.library.ualberta.ca/> select distinct ?s where {graph ual:%s  {?s ?p ?o} }" %(subgraph))
	r = sparqlData.query().convert()['results']['bindings']
	i = 0
	graph = Graph()
	print ('starting constructing triples for ' + subgraph)
	for re in r:
		i += 1	
		print (i)
		sparqlData.setQuery("prefix ual: <http://terms.library.ualberta.ca/> construct {<%s> ?p ?o} where {graph ual:%s {<%s> ?p ?o} }" %(re['s']['value'], subgraph, re['s']['value']))
		result = sparqlData.query().convert()['results']['bindings']
		for triple in result:
			p = URIRef(triple['predicate']['value'])
			s = URIRef(triple['subject']['value'])
			if triple['object']['type'] =='uri':
				o = URIRef(triple['object']['value'])
			else:
				o = Literal(triple['object']['value'])
			graph.add((s, p, o))
			filename = 'terms/' + str(subgraph) + '.nt'
	graph.serialize(destination=filename, format='nt')
	graph.remove((None,None,None))
	print ('finished triples for ' + subgraph)