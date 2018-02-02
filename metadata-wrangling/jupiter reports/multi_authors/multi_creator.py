from SPARQLWrapper import JSON, SPARQLWrapper
import re
from rdflib import URIRef, Literal, Graph
sparqlData = "http://localhost:9999/blazegraph/namespace/gillingham_20171222/sparql"
sparqlData = SPARQLWrapper(sparqlData)
sparqlData.setReturnFormat(JSON)
sparqlData.setQuery("prefix dcterm: <http://purl.org/dc/terms/> select (count(?o) as ?au) ?s where {?s dcterm:creator ?o . filter(?o!='')} group by ?s having (?au > 1) ORDER BY DESC(?au)")
s = []
r = sparqlData.query().convert()['results']['bindings']
with open('multi_creator.tsv', 'w+') as out:
for triple in r:
	noid = triple['s']['value'].split('/')[-1]
	if noid not in s:
		s.append(noid)
		out.write(triple['s']['value'] + "\t" + triple['au']['value'] + "\n")
sparqlData.setQuery("prefix dcterm: <http://purl.org/dc/terms/> select (count(?o) as ?au) ?s where {?s dcterm:contributor ?o . filter(?o!='')} group by ?s having (?au > 1) ORDER BY DESC(?au)")
r = sparqlData.query().convert()['results']['bindings']
with open('multi_contributor.tsv', 'w+') as o:
	for triple in r:
		noid = triple['s']['value'].split('/')[-1]
		if noid not in s:
			s.append(noid)
			o.write(triple['s']['value'] + "\t" + triple['au']['value'] + "\n")
with open('multi_author.txt', 'w+') as f:
	for i in s:
		f.write(i + "\n")