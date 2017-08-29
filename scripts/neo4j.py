import os
import requests
from py2neo import authenticate, Graph, Node, Relationship
from elasticsearch import helpers, Elasticsearch

predicateList = {
	"node": {
		"dis": {
			"label": "PERSON",
			"type": "dissertent"
		},
		"ths": {
			"label": "PERSON",
			"type": "supervisor"
		},
		"subject": {
			"label": "SUBJECT",
			"type": "topical"
		},
		"creator": {
			"label": "PERSON",
			"type": "creator"
		},
		"spatial": {
			"label": "SUBJECT",
			"type": "spatial"
		},
		"repositoryhasParent": {
			"label": "PROD"
		},
		"contributor": {
			"label": "PERSON",
			"type": "contributor"
		},
		"thesiscommitteemember": {
			"label": "PERSON",
			"type": "committeeMember"
		},
		"temporal": {
			"label": "SUBJECT",
			"type": "temporal"
		},
		"dpt": {
			"label": "ORGANIZATION",
			"type": "department",
			"attribute": 'specialization'
		},
		"coreAcademicDepartment": {
			"label": "ORGANIZATION",
			"type": "department",
			"attribute": 'specialization'
		}
	},
	"property": [
		"belongsToCommunity",
		"description",
		"graduationdate",
		"publisher",
		"rights",
		"identifier",
		"license",
		"abstract",
		"relationsexternalhasCollectionMember",
		"repositoryuuid",
		"modelcreatedDate",
		"thesislevel",
		"ThesisDegree",
		"hasCollectionId",
		"year_created",
		"type",
		"dateAccepted",
		"created",
		"is_community",
		"modeldownloadFilename",
		"language",
		"dateSubmitted",
		"modified",
		"title",
		"date_uploaded"
	]
}


# Connect to graph and add constraints.
authenticate("206.167.181.123:7474", "neo4j", "4metadata")
graph = Graph("http://206.167.181.123:7474/db/data/")
es = Elasticsearch([{'host': '206.167.181.123', 'port': 9200}])
scroll = helpers.scan(es, query={"query": {"match_all" : {} }}, index="jupiter-test", doc_type="Resource")
for s in scroll:
	print(s)
graph.run("CREATE CONSTRAINT ON (n:PROD) ASSERT n.value IS UNIQUE")
graph.run("CREATE CONSTRAINT ON (n:SUBJECT) ASSERT n.value IS UNIQUE")
graph.run("CREATE CONSTRAINT ON (n:PERSON) ASSERT n.value IS UNIQUE")
graph.run("CREATE CONSTRAINT ON (n:ORGANIZATION) ASSERT n.value IS UNIQUE")
graph.run("CREATE CONSTRAINT ON (n:COLLECTION) ASSERT n.value IS UNIQUE")
graph.run("CREATE CONSTRAINT ON (n:RESOURCE) ASSERT n.value IS UNIQUE")

try:
	graph.run("CREATE (r:PROD {value: \"http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/\"}) ")
except Exception as e:
	print(e)
	pass
try:
	graph.run("CREATE (r:ORGANIZATION {value: \"University of Alberta\"})")
except Exception as e:
	print(e)
	pass

for json in scroll:
	print(json)
	for record in json["hits"]["hits"]:
		print('attempt')
		source = record['_source']['resource'][0]
		if record['_source']["modelhasModel"] == 'Collection':
			for predicate in predicateList['node']:
				if predicate in record['_source']:
					if ('attribute' in predicateList['node'][predicate]) and predicateList['node'][predicate]['attribute'] in record['_source']:
						for value in record['_source'][predicate]:
							try:
								graph.run("CREATE (s:%s {value: \"%s\"}) CREATE (t:%s {value: \"%s\"}) CREATE (s)-[:%s {'type': %s}]->(t)" % ('COLLECTION', source, predicateList['node'][predicate]['label'], value, predicateList['node'][predicate]['type']), record['_source'][predicateList['node'][predicate]['attribute']])
							except Exception as e:
								graph.run("MATCH (s:%s {value: \"%s\"}) MATCH (t:%s {value: \"%s\"}) CREATE (s)-[:%s {'type': %s}]->(t)" % ('COLLECTION', source, predicateList['node'][predicate]['label'], value, predicateList['node'][predicate]['type']), record['_source'][predicateList['node'][predicate]['attribute']])
						for attribute in predicateList['property']:
							if attribute in record['_source']:
								graph.run("MATCH (s:%s {uri: \"%s\"}) set s.%s = \"%s\"" % ('COLLECTION', source, attribute, record['_source'][attribute][0]))

					else:
						for value in record['_source'][predicate]:
							try:
								graph.run("CREATE (s:%s {value: \"%s\"}) CREATE (t:%s {value: \"%s\"}) CREATE (s)-[:%s]->(t)" % ('COLLECTION', source, predicateList['node'][predicate]['label'], value, predicateList['node'][predicate]['type']))
							except Exception as e:
								graph.run("MATCH (s:%s {value: \"%s\"}) MATCH (t:%s {value: \"%s\"}) CREATE (s)-[:%s]->(t)" % ('COLLECTION', source, predicateList['node'][predicate]['label'], value, predicateList['node'][predicate]['type']))
						for attribute in predicateList['property']:
							if attribute in record['_source']:
								graph.run("MATCH (s:%s {uri: \"%s\"}) set s.%s = \"%s\"" % ('COLLECTION', source, attribute, record['_source'][attribute][0]))
		elif record['_source']['modelhasModel'] == 'GenericFile':
			for predicate in predicateList['node']:
				if predicate in record['_source']:
					if ('attribute' in predicateList['node'][predicate]) and predicateList['node'][predicate]['attribute'] in record['_source']:
						for value in record['_source'][predicate]:
							try:
								graph.run("CREATE (s:%s {value: \"%s\"}) CREATE (t:%s {value: \"%s\"}) CREATE (s)-[:%s {'type': %s}]->(t)" % ('RESOURCE', source, predicateList['node'][predicate]['label'], value, predicateList['node'][predicate]['type']), record['_source'][predicateList['node'][predicate]['attribute']])
							except Exception as e:
								graph.run("MATCH (s:%s {value: \"%s\"}) MATCH (t:%s {value: \"%s\"}) CREATE (s)-[:%s {'type': %s}]->(t)" % ('RESOURCE', source, predicateList['node'][predicate]['label'], value, predicateList['node'][predicate]['type']), record['_source'][predicateList['node'][predicate]['attribute']])
						for attribute in predicateList['property']:
							if attribute in record['_source']:
								graph.run("MATCH (s:%s {uri: \"%s\"}) set s.%s = \"%s\"" % ('RESOURCE', source, attribute, record['_source'][attribute][0]))

					else:
						for value in record['_source'][predicate]:
							try:
								graph.run("CREATE (s:%s {value: \"%s\"}) CREATE (t:%s {value: \"%s\"}) CREATE (s)-[:%s]->(t)" % ('RESOURCE', source, predicateList['node'][predicate]['label'], value, predicateList['node'][predicate]['type']))
							except Exception as e:
								graph.run("MATCH (s:%s {value: \"%s\"}) MATCH (t:%s {value: \"%s\"}) CREATE (s)-[:%s]->(t)" % ('RESOURCE', source, predicateList['node'][predicate]['label'], value, predicateList['node'][predicate]['type']))
						for attribute in predicateList['property']:
							if attribute in record['_source']:
								graph.run("MATCH (s:%s {uri: \"%s\"}) set s.%s = \"%s\"" % ('RESOURCE', source, attribute, record['_source'][attribute][0]))
