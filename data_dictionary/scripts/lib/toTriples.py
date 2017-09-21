import json
from config import sparql, path
import os


def main():
	sparql.setMethod("POST")
	for ptype in ["collection", "community", "generic", "thesis", "instances"]:
		sparql.setQuery('DROP GRAPH <http://terms.library.ualberta.ca/%s>' % (ptype))
		sparql.query()
	for ptype in ["collection", "generic", "thesis"]:
		directory = "%s/profiles/%s/" % (path, ptype)
		if not os.path.exists(directory):
			os.makedirs(directory)
		filename = os.path.join(directory, 'profile.json')
		with open(filename) as data:
			data = json.load(data)
			for item in data:
				query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA { GRAPH ual:%s { <%s> rdf:type rdf:Property" % (ptype, item)
				for key in data[item].keys():
					if 'acceptedValues' in key:
						for triple in data[item][key]:
							addValue = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA { GRAPH ual:instances { <%s> rdfs:label \"%s\" ; ual:onForm \"%s\" } } " % (triple['uri'], triple['label'], "true")
							sparql.setQuery(addValue)
							sparql.query()
							query = query + "; ual:acceptedValue <%s>" % (triple['uri'])
					elif isinstance(data[item][key], str) and ("http" in data[item][key]):
						query = query + "; <%s> <%s> " % (key, data[item][key])
					elif data[item][key] == "none":
						query = query + "; <%s> \"%s\"" % (key, "")
					else:
						query = query + "; <%s> \"%s\"" % (key, str(data[item][key]).lower())
				query = query + "} }"
				sparql.setQuery(query)
				sparql.query()


if __name__ == "__main__":
	main()