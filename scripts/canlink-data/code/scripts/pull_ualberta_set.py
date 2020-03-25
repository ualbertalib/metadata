from SPARQLWrapper import JSON, SPARQLWrapper, RDFXML, N3
from rdflib import Graph

sparqlData = "http://triplestore.library.ualberta.ca:8080/repositories/fedora"
sparql = SPARQLWrapper(sparqlData)
sparql.setReturnFormat(JSON)

with open('ual.nt', 'a') as file:
	q = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX bibo: <http://purl.org/ontology/bibo/> select ?s where { ?s rdf:type bibo:Thesis } limit 22000"
	sparql.setQuery(q)
	results = sparql.query().convert()['results']['bindings']
	for i, r in enumerate(results):
		print (i)
		query = "construct {<%s> ?p ?o} where {<%s> ?p ?o}" %(r['s']['value'], r['s']['value'])
		sparql.setQuery(query)
		sparql.setReturnFormat(N3)
		result = sparql.query().convert()
		g = Graph()
		g.parse(data=result, format="n3")
		g.serialize("ual/"+r['s']['value'].split('/')[-1], format='n3')
