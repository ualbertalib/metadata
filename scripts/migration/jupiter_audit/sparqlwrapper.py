from SPARQLWrapper import SPARQLWrapper, JSON

endpoint = SPARQLWrapper("http://206.167.181.124:9999/blazegraph/namespace/gillingham_20180222/sparql")

queryString = "select ?s where { ?s ?p ?o } "

endpoint.setQuery(queryString)
endpoint.setReturnFormat(JSON)
results = endpoint.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"]["value"])