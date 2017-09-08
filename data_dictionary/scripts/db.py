import json
from SPARQLWrapper import SPARQLWrapper, json


def main():
	sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
	sparql.method = 'POST'
	for graph in ['collection', 'generic', 'thesis']:
		query = "PREFIX ual: <http://terms.library.ualberta.ca/> CREATE GRAPH ual:%s" % (graph)
		sparql.setQuery(query)
		sparql.query
	with open('../profiles/generic/profile.json', 'r') as data:
		data = json.load(data)
		for item in data:
			for graph in ['collection', 'generic', 'thesis']:
				for instance in item['config']['acceptedValues']:
					instances = "PREFIX ual: <http://terms.library.ualberta.ca/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> INSERT DATA {GRAPH ual:%s {<%s> rdfs:label '%s' } } " % (graph, instance['uri'], instance['label'])
					instanceMap = "PREFIX ual: <http://terms.library.ualberta.ca/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> INSERT DATA {GRAPH ual:%s {<%s> ual:acceptedValues <%s>} } " % (graph, item['uri'], instance['uri'])
					print(instances)
					print(instanceMap)
					sparql.setQuery(instances)
					sparql.query()
					sparql.setQuery(instanceMap)
					sparql.query()


if __name__ == '__main__':
	main()
