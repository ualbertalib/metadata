from utilities import PrintException, removeNS, addPrefixes
from config import namespaces, profileWelcome, profileDefinitions, sparql, ignore
import json
import sys
import os
from SPARQLWrapper import JSON, SPARQLWrapper
from datetime import datetime, timedelta
from rdflib import Graph, URIRef, Literal


class Profiler(object):

	def __init__(self, ptype):
		self.ptype = ptype
		self.__backupTriples()
		self.__createJSON()
		filename = "data_dictionary/profile_%s.md" % (self.ptype)  # assumed we are in the root metadata folder
		old_stdout = sys.stdout
		with open(filename, "w+") as profile_output:
			sys.stdout = profile_output
			self.__createProfile()
			sys.stdout = old_stdout
		self.__createGithubMessage()


	def __backupTriples(self):
		filename = "data_dictionary/profiles/backup.nquads"
		sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
		sparql.setReturnFormat(JSON)
		query = "construct {graph ?g {?s ?p ?o }} where { graph ?g {?s ?p ?o}}"
		sparql.setQuery(query)
		results = sparql.query()
		graph = Graph()
		for result in results['results']['bindings']:
			if result['o']['type'] == 'literal':
				print('literal')
				graph.addN((URIRef(result['s']['value']), URIRef(result['p']['value']), Literal(result['o']['value'])), URIRef(result['g']['value']))
			elif result['o']['type'] == 'uri':
				print('uri')
				graph.addN((URIRef(result['s']['value']), URIRef(result['p']['value']), URIRef(result['o']['value'])), URIRef(result['g']['value']))
		graph.serialize(destination=filename, format='nquads')

	def __createJSON(self):
		try:
			profile = {}
			query = "PREFIX ual: <http://terms.library.ualberta.ca/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT * WHERE {GRAPH ual:%s {?property ?annotation ?value} }" % (self.ptype)
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
				elif result['annotation']['value'] in profile[result['property']['value']]:
					profile[result['property']['value']][result['annotation']['value']].append(result['value']['value'])
				else:
					profile[result['property']['value']][result['annotation']['value']] = []
					profile[result['property']['value']][result['annotation']['value']].append(result['value']['value'])

			directory = "data_dictionary/profiles/%s/" % (self.ptype)
			if not os.path.exists(directory):
				os.makedirs(directory)
			filename = directory + 'profile.json'
			with open(filename, 'w+') as p:
				json.dump(profile, p, sort_keys=True, indent=4)
		except:
			PrintException()

	def __createProfile(self):
		try:
			filename = "data_dictionary/profiles/%s/profile.json" % (self.ptype)
			with open(filename, 'r+') as profileData:
				dataOriginal = json.load(profileData)
				data = sorted(dataOriginal.items())
				print('# Jupiter %s Application Profile' % (self.ptype.title()))
				print('')
				print("%s" % (profileWelcome))
				print('')
				print('# Namespaces  ')
				for n in namespaces:
					if n['uri'] not in ignore:
						print('**%s:** %s  ' % (n['prefix'], n['uri']))
				print('')
				print('# Definitions')
				print('')
				for d in profileDefinitions:
					print('   **%s** %s  ' % (d['term'], d['def']))
				print('')
				print('# Profile by annotation')
				annotations = []
				display = False
				for key, value in data:
					for key in value.keys():
						annotations.append(key)
				annotations = sorted(list(set(annotations)))
				for annotation in annotations:
					for propertyName, PropertyData in data:
						if ((annotation in PropertyData) and ('true' in PropertyData[annotation]) and not (any(i in propertyName for i in ignore))) or (('indexAs' in annotation) or ('backwardCompatibleWith' in annotation)):
							display = True
					if display is True:
						print('### %s  ' % (removeNS(annotation)))
						display = False
					for propertyName, PropertyData in data:
						if (annotation in PropertyData) and ('true' in PropertyData[annotation]) and not (any(i in propertyName for i in ignore)):
							print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s  )  " % (removeNS(propertyName), self.ptype, addPrefixes(propertyName).replace(':', '').lower()))
						elif ((annotation in PropertyData) and ('indexAs' in annotation) and not (any(i in propertyName for i in ignore))) and (PropertyData[annotation][0] != ''):
							print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s) indexes as:  " % (removeNS(propertyName), self.ptype, addPrefixes(propertyName).replace(':', '').lower()))
							for anno in PropertyData[annotation]:
								print("    * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/jupiter_ontology.md#%s  )  " % (removeNS(anno), addPrefixes(anno).replace(':', '').lower()))
						elif ((annotation in PropertyData) and ('backwardCompatibleWith' in annotation) and not (any(i in propertyName for i in ignore))) and (PropertyData[annotation][0] != ''):
								print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s) is backward compatible with:  " % (removeNS(propertyName), self.ptype, addPrefixes(propertyName).replace(':', '').lower()))
								for anno in PropertyData[annotation]:
									print("    * %s  " % (anno))
				print('')
				print('# Profile by property')
				print('')
				for propertyName, propertyValue in data:
					if not any(i in propertyName for i in ignore):
						print('### %s  ' % (addPrefixes(propertyName)))
						for annotation, annotationValue in sorted(propertyValue.items()):
							if annotation == 'acceptedValues':
								print("  * values displayed on form:  ")
								for j in annotationValue:
									if j['onForm'] == 'true':
										print('    * **%s** (%s)  ' % (removeNS(j['label']), j['uri']))
							elif (annotation != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") and (annotationValue[0] != ''):		
								print("  * %s:  " % (removeNS(annotation)))
								for v in annotationValue:
									print("    * %s  " % (v))
		except:
			PrintException()

	def __createGithubMessage(self):
		lines = ["Daily changes made to metadata profiles:"]
		dateFilter = datetime.now() - timedelta(days=1)
		query = "prefix dcterms: <http://purl.org/dc/terms/> prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> prefix schema: <http://schema.org/> prefix ual: <http://terms.library.ualberta.ca/> select ?username ?date ?type ?graph ?property ?annotation ?insertion ?deletion where { graph ual:audit { ?event schema:agent ?user ; rdf:type ?type ;	schema:endTime ?date ; dcterms:isPartOf ?graph ; schema:targetCollection ?property ; schema:object ?annotation . OPTIONAL { ?event ual:deletion ?deletion} . OPTIONAL { ?event ual:insertion ?insertion } } } ORDER BY desc(?date)"
		sparql.setReturnFormat(JSON)
		sparql.setQuery(query)
		results = sparql.query().convert()
		for result in results['results']['bindings']:
			line = ""
			date = datetime.strptime(result['date']['value'], "%Y-%m-%d %H:%M:%S")
			if date > dateFilter:
				ptype = addPrefixes(result['graph']['value'])
				predicate = addPrefixes(result['property']['value'])
				annotation = addPrefixes(result['annotation']['value'])
				line = """
{}
  - change made to profile: '{}',
  - to the property: '{}',
  - to the annotation '{}',
  - the following changes:""".format(date, ptype, predicate, annotation)
				if ('insertion' in result) and (result['insertion']["value"] != ''):
					line = """{}
    - inserted: '{}'""".format(line, addPrefixes(result['insertion']['value']))
				if ('deletion' in result) and (result['deletion']["value"] != ''):
					line = """{}
    - deleted: '{}'""".format(line, addPrefixes(result['deletion']['value']))
				line = """{}

				""".format(line)
				lines.append(line)
		with open('data_dictionary/scripts/lib/message.md', 'w+') as f:
			f.writelines(lines)
