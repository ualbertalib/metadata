from SPARQLWrapper import SPARQLWrapper, JSON

sparql = "http://206.167.181.124:9999/blazegraph/namespace/gillingham_20180222/sparql"  # dev, 1 hour to transform

sparqlData = SPARQLWrapper(sparql)
sparqlData.setReturnFormat(JSON)
q = "prefix ualids: <http://terms.library.ualberta.ca/identifiers/> prefix info: <info:fedora/fedora-system:def/model#> prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT distinct ?resource WHERE {?resource info:hasModel 'GenericFile'^^xsd:string . FILTER (NOT EXISTS {{?resource ualids:remote_resource 'dataverse'^^xsd:string}})}"
sparqlData.setQuery(q)
results = sparqlData.query().convert()['results']['bindings']
with open("noids.txt", "a") as o:
	for r in results:
		s = r['resource']['value'].replace("gillingham", "mycombe2") + "/characterization"
		o.write ("'" + s + "'" + "\n")