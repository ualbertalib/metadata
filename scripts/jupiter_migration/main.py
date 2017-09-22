from config import sparql, namespaces
from SPARQLWrapper import JSON
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, DCTERMS, RDF

def main():
	for objectType in ["collection", "community", "generic", "thesis"]:
		getTriples(objectType)		

def getTriples(objectType):
	query = ""
	for key in namespaces.keys():
		query = query + "%: % " % ( namespace[key]['PREFIX'], namespace[key]['uri'])
		query = "SELECT * WHERE {GRAPH ual:%s {?property ?annotation ?value} }" % (ptype)
	print(query)
	#sparql.setReturnFormat(JSON)
	#sparql.setQuery(query)
	#results = sparql.query().convert()
	#for result in results['results']['bindings']:

if __name__ == "__main__":
	main()