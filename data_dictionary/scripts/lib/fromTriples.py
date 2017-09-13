import json
from config import sparql
from SPARQLWrapper import JSON
import os


def main():
	transporter()


def transporter():
	if 'ubuntu' in os.getcwd():
		path = "/home/ubuntu/metadata/data_dictionary"
	else:
		path = "/home/zschoenb/Documents/Projects/metadata/data_dictionary"
	for ptype in ["collection", "generic", "thesis"]:
		profile = {}
		query = "PREFIX ual: <http://terms.library.ualberta.ca/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT * WHERE {GRAPH ual:%s {?property ?annotation ?value} }" % (ptype)
		sparql.setReturnFormat(JSON)
		sparql.setQuery(query)
		results = sparql.query().convert()
		for result in results['results']['bindings']:
			if result['property']['value'] not in profile.keys():
				profile[result['property']['value']] = {}
			if result['annotation']['value'] == 'http://terms.library.ualberta.ca/acceptedValue':
				if 'acceptedValues' not in profile[result['property']['value']]:
					profile[result['property']['value']]['acceptedValues'] = []
				query = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX ual: <http://terms.library.ualberta.ca/> SELECT * WHERE { GRAPH ual:instances { <%s> rdfs:label ?label ; ual:onForm ?onForm } }" % (result['value']['value'])
				sparql.setQuery(query)
				annotations = sparql.query().convert()
				for annotation in annotations['results']['bindings']:
					profile[result['property']['value']]['acceptedValues'].append({'uri': result['value']['value'], 'onForm': annotation['onForm']['value'], 'label': annotation['label']['value']})
			else:
				profile[result['property']['value']][result['annotation']['value']] = result['value']['value']

		filename = '%s/profiles/%s/profile.json' % (path, ptype)
		with open(filename, 'w+') as p:
			json.dump(profile, p, sort_keys=True, indent=4)			


if __name__ == "__main__":
	main()
