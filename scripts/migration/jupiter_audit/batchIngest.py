from SPARQLWrapper import JSON, SPARQLWrapper
import json

with open("list_complete.txt", "r") as file:
	l = []
	for line in file:
		if line.replace("\n", "") not in l:
			l.append(line.replace("\n", ""))
print (len(l))
sparqlData = "http://localhost:9999/blazegraph/namespace/gillingham_20180222/sparql"
sparql = SPARQLWrapper(sparqlData)
sparql.setReturnFormat(JSON)
f = []
with open("batch_ingested.tsv", "w+") as o:
	for i in l:
		# query = "select ?batch where { <%s> <http://fedora.info/definitions/v4/repository#created> ?batch }" %(i) # http://terms.library.library.ca/id/ingestbatch does not exists
		query = "select ?batch where { <%s> <http://terms.library.library.ca/identifiers/ingestbatch> ?batch . filter(?batch != '') }" %(i) # http://terms.library.library.ca/id/ingestbatch does not exists
		sparql.setQuery(query)
		results = sparql.query().convert()['results']['bindings']
		for r in results:
			o.write(i + "\t" + r['batch']['value'] + "\n")

			