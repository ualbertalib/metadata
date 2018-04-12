from SPARQLWrapper import SPARQLWrapper, JSON
import re

def main():

	ns = [{"prefix": "bg", "uri": "http://206.167.181.124:7200/repositories/era-dd"},
	{"prefix": "premis", "uri": "http://www.loc.gov/premis/rdf/v1#"},
	{"prefix": "rdfs", "uri": "http://www.w3.org/2000/01/rdf-schema#"},
	{"prefix": "ual", "uri": "http://terms.library.ualberta.ca/"},
	{"prefix": "ualids", "uri": "http://terms.library.ualberta.ca/identifiers/"},
	{"prefix": "ualid", "uri": "http://terms.library.ualberta.ca/id/"},
	{"prefix": "ualdate", "uri": "http://terms.library.ualberta.ca/date/"},
	{"prefix": "ualrole", "uri": "http://terms.library.ualberta.ca/role/"},
	{"prefix": "ualthesis", "uri": "http://terms.library.ualberta.ca/thesis/"},
	{"prefix": "info", "uri": "info:fedora/fedora-system:def/model#"},
	{"prefix": "dcterm", "uri": "http://purl.org/dc/terms/"},
	{"prefix": "pcdm", "uri": "http://pcdm.org/models#"},
	{"prefix": "works", "uri": "http://pcdm.org/works#"},
	{"prefix": "rdf", "uri": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"},
	{"prefix": "fedora", "uri": "http://fedora.info/definitions/v4/repository#"},
	{"prefix": "iana", "uri": "http://www.iana.org/assignments/relation/"},
	{"prefix": "dc", "uri": "http://purl.org/dc/elements/1.1/"},
	{"prefix": "acl", "uri": "http://projecthydra.org/ns/auth/acl#"},
	{"prefix": "webacl", "uri": "http://www.w3.org/ns/auth/acl#"},
	{"prefix": "scholar", "uri": "http://scholarsphere.psu.edu/ns#"},
	{"prefix": "rels", "uri": "info:fedora/fedora-system:def/relations-external#"},
	{"prefix": "vivo", "uri": "http://vivoweb.org/ontology/core#"},
	{"prefix": "bibo", "uri": "http://purl.org/ontology/bibo/"},
	{"prefix": "mrels", "uri": "http://id.loc.gov/vocabulary/relators/"},
	{"prefix": "prism", "uri": "http://prismstandard.org/namespaces/basic/3.0/"},
	{"prefix": "cc", "uri": "http://creativecommons.org/ns#"},
	{"prefix": "fabio", "uri": "http://purl.org/spar/fabio/"},
	{"prefix": "lang", "uri": "http://id.loc.gov/vocabulary/iso639-2/"},
	{"prefix": "mrel", "uri": "http://id.loc.gov/vocabulary/relators/"},
	{"prefix": "naf", "uri": "http://id.loc.gov/authorities/names/"},
	{"prefix": "swrc", "uri": "http://ontoware.org/swrc/ontology#"},
	{"prefix": "schema", "uri": "http://schema.org/"},
	{"prefix": "ldp", "uri": "http://www.w3.org/ns/ldp#"},
	{"prefix": "use", "uri": "http://pcdm.org/use#"},
	{"prefix": "ebucore", "uri": "http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#"},
	{"prefix": "ore", "uri": "http://www.openarchives.org/ore/terms/"},
	]

	sparql = "http://206.167.181.124:9999/blazegraph/namespace/gillingham_20180222/sparql"  # dev, 1 hour to transform
	Terms = "http://206.167.181.124:7200/repositories/era-dd"

	sparqlData = SPARQLWrapper(sparql)
	sparqlData.setReturnFormat(JSON)
	sparqlTerms = SPARQLWrapper(Terms)
	sparqlTerms.setReturnFormat(JSON)

	with open ("checksums.txt", "r") as f:
		checksums = {}
		for line in f:
			c = line.split("------")[0]
			noid = line.split("------")[1].replace(".xml\n", "")
			if c not in checksums.keys():
				checksums[c] = [noid] 
			else:
				checksums[c].append(noid)

	'''with open("duplicates.tsv", "w+") as o:
		for i in checksums.keys():
			if len(checksums[i]) > 1:
				o.write(i + "\t" + str(checksums[i]) + "\n")'''

	def getNS(predicate):
		for i in ns:
			prefix = ''
			if i['uri'] in predicate:
				return (predicate.replace(i['uri'], '').split("/")[-1])

	def getPredicates():
		GT = {}
		generic = {}
		query = "PREFIX ual: <http://terms.library.ualberta.ca/> select ?oldPredicate where { graph ual:generic { ?predicate ual:required 'true' ; ual:backwardCompatibleWith ?oldPredicate } }"
		sparqlTerms.setQuery(query)
		results = sparqlTerms.query().convert()['results']['bindings']
		for triple in results:
			variable = getNS(triple['oldPredicate']['value'])
			generic[variable] = triple['oldPredicate']['value']
			
		thesis = {}
		query = "PREFIX ual: <http://terms.library.ualberta.ca/> select ?oldPredicate where { graph ual:thesis { ?predicate ual:required 'true'; ual:backwardCompatibleWith ?oldPredicate } }"
		sparqlTerms.setQuery(query)
		results = sparqlTerms.query().convert()['results']['bindings']
		for triple in results:
			variable = getNS(triple['oldPredicate']['value'])
			thesis[variable] = triple['oldPredicate']['value']
		GT['generic'] = generic 
		GT['thesis'] = thesis
		return(GT)

	def getType(uri):
		typ = ''
		query = "prefix dcterm: <http://purl.org/dc/terms/> prefix info: <info:fedora/fedora-system:def/model#> prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT distinct ?type WHERE  {<%s> info:hasModel 'GenericFile'^^xsd:string . optional{<%s> dcterm:type ?type} }" %(uri, uri)
		sparqlData.setQuery(query)
		results = sparqlData.query().convert()['results']['bindings']
		for r in results:
			try:
				type = r['type']['value']
			except:
				pass
			if type == "Thesis":
				return ("Thesis")
			else:
				return ("generic")

	def findDups():
		final = []
		for key in checksums.keys():
			if key != '':
				if len(checksums[key]) > 1:
					count = {}
					for i in checksums[key]:
						weight = 0
						uri = "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/" + i[0:2] + "/" + i[2:4] + "/" + i[4:6] + "/" + i[6:8] + "/" + i 
						type = getType(uri)
						print (i, type)
						if type == "generic":
							generic_v = ''
							generic_p = ''
							predicate_count = {}
							for j in predicate['generic'].keys():
								generic_v = generic_v + " ?" +j 
								generic_p = generic_p + " . optional {<" + uri + ">" + " <" + predicate['generic'][j] + ">" + " ?" + j + "}" 
								predicate_count[j] = "false"
							query = "prefix info: <info:fedora/fedora-system:def/model#> prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT distinct %s where {<%s> info:hasModel 'GenericFile'^^xsd:string %s }" %(generic_v, uri, generic_p)
							sparqlData.setQuery(query)
							results = sparqlData.query().convert()['results']['bindings']
							for r in results:
								for v in predicate['generic'].keys():
									try:
										value = r[v]['value']
										weight = weight + 1
										count[i] = [] 
										predicate_count[v] = "true"
									except:
										pass
						elif type == "Thesis":
							thesis_v = ''
							thesis_p = ''
							predicate_count = {}
							for j in predicate['thesis'].keys():
								thesis_v = thesis_v + " ?" +j 
								thesis_p = thesis_p + " . optional {<" + uri + ">" + " <" + predicate['thesis'][j] + ">" + " ?" + j + "}" 
								predicate_count[j] = "false"
							query = "prefix info: <info:fedora/fedora-system:def/model#> prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT distinct %s where {<%s> info:hasModel 'GenericFile'^^xsd:string %s }" %(thesis_v, uri, thesis_p)
							sparqlData.setQuery(query)
							results = sparqlData.query().convert()['results']['bindings']
							for r in results:
								for v in predicate['thesis'].keys():
									try:
										value = r[v]['value']
										weight = weight + 1
										count[i] = [] 
										predicate_count[v] = "true"
									except:
										pass
						try:
							count[i].append(predicate_count)
							count[i].append(weight)
						except:
							print (i)
					final.append(count)
					#print (count)
					print ("next")
		print (final)
		with open ("t.tsv", "w+") as file:
			for i in final:
				for j in i.keys():
					file.write(str(j) + str(i[j]) + "\n")
				file.write("\n")

	predicate = getPredicates()
	findDups()


if __name__ == "__main__":
    main()