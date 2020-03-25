from SPARQLWrapper import JSON, SPARQLWrapper, RDFXML, N3

sparql = "http://206.167.181.124:7200/repositories/cldi-test-7"
dbp_sparql = "http://dbpedia.org/sparql/"
dbp_data = SPARQLWrapper(dbp_sparql)
dbp_data.setReturnFormat(JSON)
sparqlData = SPARQLWrapper(sparql)
sparqlData.setCredentials("admin", "4Metadata!")
sparqlData.setReturnFormat(JSON)

geo = {"type": "FeatureCollection"}
features = []

query = """select ?institution ?num_of_docs (count (distinct ?resource) as ?num_of_docs) where {?resource <http://purl.org/dc/terms/publisher> ?institution} group by ?institution order by DESC(?num_of_docs)"""
sparqlData.setQuery(query)  # set the query
results = sparqlData.query().convert()
for i, result in enumerate(results['results']['bindings']):
    print (i)
    url =result['institution']['value'] 
    uni = url.replace('http://canlink.library.ualberta.ca/institution/', '').replace('_', ' ')
    docs = result['num_of_docs']['value']
    query = """select ?lat ?long where {?s rdfs:label "%s"@en; geo:lat ?lat; geo:long ?long} LIMIT 10""" %(uni)
    dbp_data.setQuery(query)  # set the query
    results = dbp_data.query().convert()
    for re in results["results"]["bindings"]:
    	feature = {"type": "Feature"}
    	feature["properties"] = {
    		"name": str(uni),
    		"items": str(docs),
            "url": str(url),
            "search_link": "?page=1?q=" + url + "?search_type=institution?l=25?so=Relevance?facet=?facet_type=page?f=",
    		"lng": float(re["long"]["value"]),
    		"lat": float(re["lat"]["value"])
    	}
    	feature["geometry"] = {
    		"type": "Point",
    		"coordinates": [float(re["long"]["value"]),float(re["lat"]["value"])]
    	}
    	features.append(feature)
geo["features"] = features

print (geo)