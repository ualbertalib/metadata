from elasticsearch import helpers, Elasticsearch
from SPARQLWrapper import SPARQLWrapper, JSON
from dateutil import parser as parser
import math

predicates = {
	"resourceType": ("<http://purl.org/dc/terms/type>", "NR"),
	"doi": ("<http://purl.org/dc/terms/identifier>", "NR"),
	"title": ("<http://purl.org/dc/terms/title>", "NR"),
	"contributor": ("<http://purl.org/dc/terms/contributor>", "R"),
	"creator": ("<http://purl.org/dc/terms/creator>", "R"),
	"spatial": ("<http://purl.org/dc/terms/spatial>", "R"),
	"temporal": ("<http://purl.org/dc/terms/temporal>", "R"),
	"subject": ("<http://purl.org/dc/terms/subject>", "R"),
	"dateCreated": ("<http://purl.org/dc/terms/created>", "NR"),
	"dissertant": ("<http://id.loc.gov/vocabulary/relators/dis>", "NR"),
	"dateAccepted": ("<http://purl.org/dc/terms/dateAccepted>", "NR"),
	"department": ("<http://vivoweb.org/ontology/core#AcademicDepartment>", "R"),
	"degree": ("<http://purl.org/ontology/bibo/ThesisDegree>", "NR"),
	"specialization": ("<http://terms.library.ualberta.ca/thesis/specialization>", "NR"),
	"level": ("<http://terms.library.ualberta.ca/thesis/thesislevel>", "NR"),
	"supervisor": ("<http://id.loc.gov/vocabulary/relators/ths>", "NR"),
	"committee": ("<http://terms.library.ualberta.ca/role/thesiscommitteemember>", "R"),
	"collection": ("<http://terms.library.ualberta.ca/identifiers/hasCollection>", "R"),
	"abstract": ("<http://purl.org/dc/terms/abstract>", "NR"),
	"description": ("<http://purl.org/dc/terms/description>" "NR"),
}

indexSettings = {
	"settings": {
		"number_of_shards": 1,
		"number_of_replicas": 0
	},
	"mappings": {
		"resource": {
			"properties": {
				"subject": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"resourceType": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"doi": {
					"type": "text",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"title": {
					"type": "text",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"contributor": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"creator": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"spatial": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"temporal": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "date"
						}
					}
				},
				"dateCreated": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "date",
							"format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss+SS:SS||yyyy-MM-dd'T'HH:mm:ss'Z'"
						}
					}
				},
				"description": {
					"type": "text",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"abstract": {
					"type": "text",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"dissertant": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"dateAccepted": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "date",
							"format": "yyyy-MM-dd'T'HH:mm:ss||yyyy-MM-dd'T'HH:mm:ss+SS:SS||yyyy-MM-dd'T'HH:mm:ss'Z'"
						}
					}
				},
				"department": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"degree": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"specialization": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"level": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"supervisor": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"committee": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				},
				"collection": {
					"type": "keyword",
					"fields": {
						"label": {
							"type": "text"
						}
					}
				}
			}
		}
	}
}

sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/ERA/sparql")
query = """SELECT DISTINCT (count(?a) AS ?count) WHERE { ?a ?b ?c }"""
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
for result in sparql.query().convert()['results']['bindings']:
	n = int(result['count']['value'])


def main():
	query = """prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT * WHERE {OPTIONAL {?resource <http://purl.org/dc/terms/type> ?resourceType } . OPTIONAL {?resource <http://purl.org/dc/terms/abstract> ?abstract } . OPTIONAL {?resource <http://purl.org/dc/terms/description> ?description } . OPTIONAL {?resource <http://purl.org/dc/terms/identifier> ?doi } . OPTIONAL {?resource <http://purl.org/dc/terms/title> ?title } . OPTIONAL {?resource <http://purl.org/dc/terms/contributor> ?contributor } . OPTIONAL {?resource <http://purl.org/dc/terms/creator> ?creator } . OPTIONAL {?resource <http://purl.org/dc/terms/spatial> ?spatial } . OPTIONAL {?resource <http://purl.org/dc/terms/temporal> ?temporal } . OPTIONAL {?resource <http://purl.org/dc/terms/subject> ?subject } . OPTIONAL {?resource <http://purl.org/dc/terms/created> ?dateCreated } . OPTIONAL {?resource <http://id.loc.gov/vocabulary/relators/dis> ?dissertant } . OPTIONAL {?resource <http://purl.org/dc/terms/dateAccepted> ?dateAccepted } . OPTIONAL {?resource <http://vivoweb.org/ontology/core#AcademicDepartment> ?department } . OPTIONAL {?resource <http://purl.org/ontology/bibo/ThesisDegree> ?degree } . OPTIONAL {?resource <http://terms.library.ualberta.ca/thesis/specialization> ?specialization } . OPTIONAL {?resource <http://terms.library.ualberta.ca/thesis/thesislevel> ?level } . OPTIONAL {?resource <http://id.loc.gov/vocabulary/relators/ths> ?supervisor } . OPTIONAL {?resource <http://terms.library.ualberta.ca/role/thesiscommitteemember> ?committee} . OPTIONAL {?resource <http://terms.library.ualberta.ca/identifiers/hasCollection> ?collection} . }"""
	print('querying triple store')
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	es = Elasticsearch([{'host': '206.167.181.123', 'port': 9200}])
	print('deleting existing index')
	es.indices.delete(index="era", ignore=[400, 404])
	print('creating new index')
	es.indices.create(index="era", body=indexSettings)
	print('commencing indexing')
	arrange(results, es)
	

def collate(result, key, resource, datum):
	if predicates[key][1] == 'NR':
		if key == 'dateAccepted' or key == 'dateCreated':
			try:
				datum[resource][key] = parser.parse(result[key]['value']).isoformat('T')
			except Exception:
				pass
		else:
			datum[resource][key] = result[key]['value']
	elif predicates[key][1] == 'R':
		if key not in datum[resource]:
			datum[resource][key] = []
		if key == 'temporal':
			try:
				datum[resource][key].append(parser.parse(result[key]['value']).isoformat('T'))
			except Exception:
				pass
		else:
			datum[resource][key].append(result[key]['value'])
	return datum


def arrange(results, es):
	datum = {}
	i = 1
	for result in results["results"]["bindings"]:
		resource = result['resource']['value']
		for key in predicates.keys():
			if key in result.keys() and result[key]['value'] is not '':
				if resource in datum:
					datum = collate(result, key, resource, datum)
				else:
					datum[resource] = {}
					datum = collate(result, key, resource, datum)
		for data in datum:
			for key in datum[data].keys():
				if isinstance(datum[data][key], list):
					datum[data][key] = list(set(datum[data][key]))
		if len(datum) == 500:
			print('committing batch', i, 'of', str(math.ceil(n / 500)))
			elastic(datum, es)
			datum = {}
			i = i + 1
	print('committing batch', i, 'of', str(math.ceil(n / 500)))
	elastic(datum, es)




def elastic(datum, es):
	actions = []
	for resource in datum.keys():
		entry = datum[resource]
		entry['resource'] = [resource]
		action = {
			"_index": "era",
			'_op_type': 'index',
			"_type": 'resource',
			"_id": resource[0],
			"_source": entry
		}
		actions.append(action)
	helpers.bulk(es, actions)


if __name__ == "__main__":
	main()