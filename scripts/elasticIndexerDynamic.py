from elasticsearch import helpers, Elasticsearch
from SPARQLWrapper import SPARQLWrapper, JSON
from dateutil import parser as parser
import json
indexSettings = {
	"settings": {
		"number_of_shards": 1,
		"number_of_replicas": 0
	},
	"mappings": {
		"resource": {
			"properties": {}
		}
	}
}


def main():
	n = getResources()
	sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/jupiter-test/sparql")
	es = Elasticsearch([{'host': '206.167.181.123', 'port': 9200}])
	print('deleting existing index')
	es.indices.delete(index="era2", ignore=[400, 404])
	es.indices.delete(index="jupiter-test", ignore=[400, 404])
	print('creating new index')
	predicates = {'GenericFile': getPredicates('GenericFile'), 'Collection': getPredicates('Collection')}
	buildIndex(predicates)
	es.indices.create(index="jupiter-test", body=indexSettings)



	for model in predicates.keys():
		query = "prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT * WHERE {?resource <info:fedora/fedora-system:def/model#hasModel> \"%s\" . ?resource ?predicate ?object }" % (model)
		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		arrange(results, es, n, predicates[model])


def getResources():
	sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/jupiter-test/sparql")
	query = """SELECT (count(DISTINCT ?a) as ?n) WHERE { ?a ?b ?c }"""
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	resources = []
	for result in sparql.query().convert()['results']['bindings']:
		n = (result['n']['value'])
	print(n, 'items to index')
	return n


def buildIndex(predicates):
	for model in predicates.keys():
		for predicate in predicates[model]:
			if 'date' in predicate:
				indexSettings['mappings']['resource']['properties'][predicate[1]] = {"type": "keyword", "fields": {"label": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss+SS:SS||yyyy-MM-dd'T'HH:mm:ss'Z'"}}}
			else:
				indexSettings['mappings']['resource']['properties'][predicate[1]] = {"type": "keyword", "fields": {"label": {"type": "text"}}}
	
	# print(json.dumps(indexSettings, sort_keys=True, indent=4, separators=(',', ': ')))

def getPredicates(model):
	sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/jupiter-test/sparql")
	predicates = []
	query = "prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?predicate WHERE { ?resource <info:fedora/fedora-system:def/model#hasModel> '%s' . ?resource ?predicate ?object}" % (model)
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	for result in results["results"]["bindings"]:
		label = result['predicate']['value'].split('/')[-1].replace('#', '').replace('-', '')
		predicates.append((result['predicate']['value'], label))
	return predicates


def commit(predicates):
	sparql = SPARQLWrapper("http://sheff.library.ualberta.ca:9999/blazegraph/namespace/fcrepo/sparql")
	for key in predicates.keys():
		for predicate in predicates[key]:
			query = "prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT* WHERE {?resource <info:fedora/fedora-system:def/model#hasModel> \"%s\"^^xsd:string" % (key)
			query = query + " . ?resource <%s> ?%s }" % (predicate[0], predicate[1])
			sparql.setQuery(query)
			sparql.setReturnFormat(JSON)
			results = sparql.query().convert()
			g = Graph()
			for result in results["results"]["bindings"]:
				if predicate[1] in result.keys() and result[predicate[1]]['value'] is not '':
					g.add((URIRef(result['resource']['value']), URIRef(predicate[0]), Literal(str(result[predicate[1]]['value']))))
			g.serialize(destination='/home/zschoenb/Documents/nt/' + key + predicate[1] + '.nt', format='nt', indent=4)


def collate(result, predicate, resource, datum):
	# check if this particular predicate has been added before (i.e. is it a repeated predicate?)
	if predicate[1] not in datum[resource]:
		# it is new, so create a list
		datum[resource][predicate[1]] = []
		# check if this is a date predicate
		if predicate[1] == 'dateAccepted' or predicate[1] == 'dateCreated':
			# not all dates can be parsed easily, so we build in an exception handler
			try:
				datum[resource][predicate[1]] = parser.parse(result['object']['value']).isoformat('T')
			except Exception:
				pass
		# if not a date, simply append the value to the document under the field labelled by the predicate to which it belongs
		else:
			if len(result['object']['value']) > 32766:
				value = result['object']['value'][0:32766]
			else:
				value = result['object']['value']
			datum[resource][predicate[1]].append(value)
	# this is a repeating value, so we've already created a list
	else:
		# check if this is a date predicate
		if predicate[1] == 'dateAccepted' or predicate[1] == 'dateCreated':
			# not all dates can be parsed easily, so we build in an exception handler
			try:
				datum[resource][predicate[1]] = parser.parse(result['object']['value']).isoformat('T')
			except Exception:
				pass
		# if not a date, simply append the value to the document under the field labelled by the predicate to which it belongs
		else:
			if len(result['object']['value']) > 32766:
				value = result['object']['value'][0:32766]
			else:
				value = result['object']['value']
			datum[resource][predicate[1]].append(value)
	# return this field mapping
	return datum


def arrange(results, es, n, predicates):
	total = 0
	datum = {}
	# iterate over the data retrieved for this model (either collection or genericfile)
	for result in results["results"]["bindings"]:
		# set the resource (this is the document id)
		resource = result['resource']['value']
		# iterate over every predicate
		for predicate in predicates:
			# check if the predicate label is attached to this resource and its value is not blank
			if predicate[0] in result['predicate']['value'] and result['object']['value'] is not '':
				# check if we have created a document yet for this resource
				if resource in datum:
					# yes, a document exists, so go ahead and attach the data to the document
					datum = collate(result, predicate, resource, datum)
				else:
					# no document exists (this is the first time seeing the resource), create the resource
					datum[resource] = {}
					# attach the data to the document
					datum = collate(result, predicate, resource, datum)
		for predicate in datum[resource].keys():
			datum[resource][predicate] = list(set(datum[resource][predicate]))
		if len(datum) == 500:
			elastic(datum, es)
			datum = {}
			total = total + 500
			print('indexed', total)
	total = total + len(datum)
	elastic(datum, es)
	print(total, 'of', n, 'resources indexed')


def elastic(datum, es):
	actions = []
	for resource in datum.keys():
		entry = datum[resource]
		entry['resource'] = [resource]
		action = {
			"_index": "jupiter-test",
			'_op_type': 'index',
			"_type": 'resource',
			"_id": resource,
			"_source": entry
		}
		actions.append(action)
	helpers.bulk(es, actions)


if __name__ == "__main__":
	main()
