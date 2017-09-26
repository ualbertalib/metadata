from config import namespaces, sparql
import linecache
import os
import sys
from SPARQLWrapper import JSON
import json


def addPrefixes(v):
	""" replaces a namespace with a prefix """
	for line in namespaces:
		if line['uri'] in v:
			v = v.replace(line['uri'], line['prefix'] + ':')
	return v


def removeNS(v):
	""" removes the namespace from a predicate, leaving only the predicate term """
	for line in namespaces:
		if line['uri'] in v:
			v = v.replace(line['uri'], '')
	return v


def PrintException():
	""" for testing """
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))


def pushOntologyToTripleStore():
	""" only for the first implementation of the terms database (will destroy changes by issueing a fresh copy of properties from the ontology)"""
	sparql.setMethod("POST")
	for ptype in ["collection", "community", "generic", "thesis", "instances"]:
		sparql.setQuery('DROP GRAPH <http://terms.library.ualberta.ca/%s>' % (ptype))
		sparql.query()
	for ptype in ["collection", "generic", "thesis"]:
		directory = "data_dictionary/profiles/%s/" % (ptype)
		if not os.path.exists(directory):
			os.makedirs(directory)
		filename = directory + 'profile.json'
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
