from SPARQLWrapper import JSON, SPARQLWrapper
sparqlData = "http://localhost:9999/blazegraph/namespace/gillingham_20180222/sparql"
sparqlData = SPARQLWrapper(sparqlData)
sparqlData.setReturnFormat(JSON)
query = "prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix dcterm: <http://purl.org/dc/terms/> select ?s (COUNT(?dep) AS ?count) where {?s dcterm:type 'Thesis'^^xsd:string . ?s <http://id.loc.gov/vocabulary/relators/ths> ?dep . filter(?dep != '')} group by ?s having (?count > 1) order by DESC(?count)"
sparqlData.setQuery(query) 
results = sparqlData.query().convert()
with open('multiple_supervisors.tsv', 'w+') as supervisor:
	supervisor.write("NOID" + "\t" + "Number of Supervisors" + "\n")
	for result in results['results']['bindings']:
		supervisor.write(result['s']['value'].split("/")[-1] + "\t" + result['count']['value'] + "\n")
	supervisor.close()
with open('multiple_supervisors.txt', 'w+') as supervisor:
	for result in results['results']['bindings']:
		supervisor.write(result['s']['value'].split("/")[-1] + "\n")
	supervisor.close()

query = "prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix dcterm: <http://purl.org/dc/terms/> select distinct ?s (COUNT(?dep) AS ?count) where {?s dcterm:type 'Thesis'^^xsd:string . ?s <http://vivoweb.org/ontology/core#AcademicDepartment> ?dep . filter(?dep != '')} group by ?s having (?count > 1) order by DESC(?count)"
sparqlData.setQuery(query) 
results = sparqlData.query().convert()
with open('multiple_departments.tsv', 'w+') as department:
	department.write("NOID" + "\t" + "Number of Departments" + "\n")
	for result in results['results']['bindings']:
		department.write(result['s']['value'].split("/")[-1] + "\t" + result['count']['value'] + "\n")
	department.close()
with open('multiple_departments.txt', 'w+') as department:
	for result in results['results']['bindings']:
		department.write(result['s']['value'].split("/")[-1] + "\n")
	department.close()

query = "prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix dcterm: <http://purl.org/dc/terms/> select distinct ?s (COUNT(?dep) AS ?count) where {?s dcterm:creator ?dep . filter(?dep != '')} group by ?s having (?count > 1) order by DESC(?count)"
sparqlData.setQuery(query) 
results = sparqlData.query().convert()
with open('multiple_creators.tsv', 'w+') as creator:
	creator.write("NOID" + "\t" + "Number of Creators" + "\n")
	for result in results['results']['bindings']:
		creator.write(result['s']['value'].split("/")[-1] + "\t" + result['count']['value'] + "\n")
	creator.close()
with open('multiple_creators.txt', 'w+') as creator:
	for result in results['results']['bindings']:
		creator.write(result['s']['value'].split("/")[-1] + "\n")
	creator.close()
