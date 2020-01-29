from SPARQLWrapper import JSON, SPARQLWrapper
import pickle

sparql = "http://206.167.181.235:7200/repositories/csh"
sparqlData = SPARQLWrapper(sparql)
sparqlData.setReturnFormat(JSON)
csh = {}

'''query = """select * where {{?s <http://www.w3.org/2004/02/skos/core#prefLabel> ?o optional{?s <http://www.w3.org/2004/02/skos/core#altLabel> ?oo} . filter(?s != <http://canlink.library.ualberta.ca/subject/canadian-subject-headings>)}} """
sparqlData.setQuery(query)  # set the query
results = sparqlData.query().convert()
for i, result in enumerate(results['results']['bindings']):
	id = result['s']['value']
	if id not in csh.keys():
		csh[id] = {}
		subject = result['o']['value']
		csh[id]['subject'] = subject
		if 'oo' in result.keys():
			alt = result['oo']['value']
			csh[id]['alt'] = []
			csh[id]['alt'].append(alt)
	else:
		if 'alt' in csh[id].keys():
			csh[id]['alt'].append(alt)
		else:
			csh[id]['alt'] = []
			csh[id]['alt'].append(alt)

pickle_out = open("csh.pickle","wb")
pickle.dump(csh, pickle_out)
pickle_out.close()'''


query = """select * where {{?s <http://www.w3.org/2004/02/skos/core#prefLabel> ?o . filter(?s != <http://canlink.library.ualberta.ca/subject/canadian-subject-headings>)}} """
sparqlData.setQuery(query)  # set the query
results = sparqlData.query().convert()
for i, result in enumerate(results['results']['bindings']):
	subject = result['o']['value'].lower()
	if subject not in csh.keys():
		csh[subject] = result['s']['value']
		

pickle_out = open("csh-1.pickle","wb")
pickle.dump(csh, pickle_out)
pickle_out.close()