from SPARQLWrapper import JSON, SPARQLWrapper
import json

with open("list.txt", "r") as file:
	l = []
	for line in file:
		if line.replace("\n", "") not in l:
			l.append(line.replace("\n", ""))
print (len(l))
sparqlData = "http://localhost:9999/blazegraph/namespace/gillingham_20180222/sparql"
sparql = SPARQLWrapper(sparqlData)
sparql.setReturnFormat(JSON)
f = []

for i in l:
	query = "select ?predicate where { <%s> ?predicate ?batch }" %(i) # http://terms.library.library.ca/id/ingestbatch does not exists
	sparql.setQuery(query)
	results = sparql.query().convert()['results']['bindings']
	for r in results:
		if r['predicate']['value'] not in f:
			f.append(r['predicate']['value'])
with open("predicates.tsv", "w+") as o:
	for i in f:
		o.write(i + "\n")
			