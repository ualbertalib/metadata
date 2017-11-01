import json
from SPARQLWrapper import JSON, SPARQLWrapper
from rdflib import URIRef, Literal, Graph



def commit(g, s, p, o):
	sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql", returnFormat=JSON)
	sparql.setMethod("POST")
	if o.startswith("http") or o.startswith("info:fedora"):
		query = "INSERT DATA {graph <http://terms.library.ualberta.ca/%s> { <%s> <%s> <%s> } }" % (g, s, p, o)
	else:
		query = "INSERT DATA {graph <http://terms.library.ualberta.ca/%s> { <%s> <%s> \"%s\" } }" % (g, s, p, o)
	sparql.setQuery(query)
	sparql.query()


for profileType in ['collection', 'community', 'generic', 'thesis']:
	print(profileType)
	filename = '%s/profile.json' % (profileType)
	with open(filename, 'r+') as f:
		source = json.load(f)
		for subject in source.keys():		
			for predicate in source[subject].keys():	
				if 'acceptedValues' in predicate:
					for value in source[subject]['acceptedValues']:
						if 'uri' in value:
							commit(profileType, URIRef(subject), URIRef('http://terms.library.ualberta.ca/acceptedValue'), URIRef(value['uri']))
							commit('instances', URIRef(value['uri']), URIRef("http://terms.library.ualberta.ca/onForm"), Literal(value['onForm']))
							commit('instances', URIRef(value['uri']), URIRef("http://terms.library.ualberta.ca/label"), Literal(value['label']))
						else:
							print(subject, value)
				else:
					for value in source[subject][predicate]:
						if value != '':
							s = URIRef(subject)
							p = URIRef(predicate)
							if value.startswith("http://") or value.startswith("info:fedora"):
								o = URIRef(value)
							else:
								o = Literal(value)
							commit(profileType, s, p, o)
