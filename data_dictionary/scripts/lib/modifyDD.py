from utilities import PrintException, removeNS, addPrefixes
from config import namespaces, profileWelcome, profileDefinitions, sparql, ignore
import json
import sys
import os
from SPARQLWrapper import JSON, SPARQLWrapper
from datetime import datetime, timedelta
import re

sparqlData = "http://206.167.181.124:7200/repositories/era-dd"
sparqlData = SPARQLWrapper(sparqlData)
sparqlData.setReturnFormat(JSON)
with open ('modifyDD.txt' , 'w+') as out:
	for subgraph in ['community', 'collection', 'generic', 'thesis', 'oai_pmh', 'oai_etdms', 'instances']:
		out.write("PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> prefix ual: <http://terms.library.ualberta.ca/> prefix ualid: <http://terms.library.ualberta.ca/id>" + "\n")
		sparqlData.setQuery("prefix ual: <http://terms.library.ualberta.ca/> select  * where {graph ual:%s  {?s ?p ?o} }" %(subgraph))
		r = sparqlData.query().convert()['results']['bindings']
		for triple in r:
			subject = triple['s']['value'].lower()
			predicate = triple['p']['value']
			objectt = triple['o']['value']
			sparql = "http://206.167.181.124:7200/repositories/testdd"
			sparql = SPARQLWrapper(sparql)
			sparql.setMethod('POST')
			if triple['o']['type'] == "uri":
				query = "INSERT DATA {GRAPH ual:%s {<%s> <%s> <%s>} } ; " % (subgraph, subject, predicate, objectt)
			if triple['o']['type'] == "literal":
				#print (subject, " is a literal")
				query = 'INSERT DATA {GRAPH ual:%s {<%s> <%s> "%s"} } ; ' % (subgraph, subject, predicate, objectt)
			out.write(query + "\n")
			query = "INSERT DATA {GRAPH ual:%s {<%s> <http://terms.library.ualberta.ca/dataDictionaryLabel> <%s>} } ; " % (subgraph, subject, triple['s']['value'])
			out.write(query + "\n")

