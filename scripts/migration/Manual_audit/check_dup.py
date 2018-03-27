from SPARQLWrapper import JSON, SPARQLWrapper
import json
from config import sparqlData

with open("list.txt", "r") as file:
	l = []
	for line in file:
		if line.replace("\n", "") not in l:
			l.append(line.replace("\n", ""))
print (len(l))
sparql = SPARQLWrapper(sparqlData)
sparql.setReturnFormat(JSON)
f = []
with open("test.tsv", "w+") as o:
	for i in l:
		query = "PREFIX dcterm: <http://purl.org/dc/terms/> select ?title where { <%s> dcterm:title ?title }" %(i)
		sparql.setQuery(query)
		results = sparql.query().convert()['results']['bindings']
		for r in results:
			q = 'PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> PREFIX dcterm: <http://purl.org/dc/terms/> select ?s where { ?s dcterm:title "%s"^^xsd:string }' %(r['title']['value'].replace('"', ''))
			sparql.setQuery(q)
			result = sparql.query().convert()['results']['bindings']
			for re in result:
				if re['s']['value'] not in l:
					o.write(re['s']['value'] + "\t" + i + "\t" + r['title']['value'].replace('"', '') + "\n")
print (len(f))

