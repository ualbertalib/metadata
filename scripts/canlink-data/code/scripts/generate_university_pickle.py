import pickle
from SPARQLWrapper import JSON, SPARQLWrapper, RDFXML, N3

dbp_sparql = "http://dbpedia.org/sparql/"
dbp_data = SPARQLWrapper(dbp_sparql)
dbp_data.setReturnFormat(JSON)

query = """select distinct ?Concept ?rdfs ?sameAs where {?Concept <http://purl.org/linguistics/gold/hypernym> <http://dbpedia.org/resource/University> . 
optional{?Concept <http://www.w3.org/2000/01/rdf-schema#label> ?rdfs} .
optional{?Concept <http://dbpedia.org/property/country> ?c} .
optional{?Concept <http://dbpedia.org/ontology/country> ?cc} .
optional{?Concept <http://www.w3.org/2002/07/owl#sameAs> ?sameAs}
filter((?c = "Canada"^^<http://www.w3.org/1999/02/22-rdf-syntax-ns#langString> || ?cc = <http://dbpedia.org/resource/Canada>) && contains(str(?sameAs), 'http://www.wikidata.org/entity/'))}"""
dbp_data.setQuery(query)  # set the query
results = dbp_data.query().convert()
universities = {}
for re in results["results"]["bindings"]:
	if 'rdfs' in re.keys():
		if re['rdfs']['xml:lang'] == 'en':
			if re['rdfs']['xml:lang'] not in universities.keys():
				universities[re['rdfs']['value']] = []
				universities[re['rdfs']['value']].append(re['Concept']['value'])
				if 'sameAs' in re.keys():
					if 'http://www.wikidata.org/entity/' in re['sameAs']['value']:
						universities[re['rdfs']['value']].append(re['sameAs']['value'])
			else:
				if 'sameAs' in re.keys():
					if 'http://www.wikidata.org/entity/' in re['sameAs']['value']:
						if re['sameAs']['value'] not in universities[re['rdfs']['value']]:
							universities[re['rdfs']['value']].append(re['sameAs']['value'])

pickle_out = open("universities-1.pickle","wb")
pickle.dump(universities, pickle_out)
pickle_out.close()