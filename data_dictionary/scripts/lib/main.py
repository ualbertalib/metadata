import json
from SPARQLWrapper import SPARQLWrapper, JSON
from config import namespaces, profileWelcome, profileDefinitions, sparql, definitions, ddWelcome
import os
import sys
import linecache


def main():
	old_stdout = sys.stdout
	with open('data_dictionary/jupiter_ontology.md', "w+") as ontology:
		sys.stdout = ontology
		owlDocument().generate()
	sys.stdout = old_stdout
	for ptype in ["collection", "community", "generic", "thesis"]:
		Profiler(ptype)
		# QueryFactory.getMigrationQuery(ptype)


class Profiler(object):

	def __init__(self, ptype):
		self.ptype = ptype
		self.__createJSON()
		filename = "data_dictionary/profile_%s.md" % (self.ptype)  # assumed we are in the root metadata folder
		old_stdout = sys.stdout
		with open(filename, "w+") as profile_output:
			sys.stdout = profile_output
			self.__createProfile()
			sys.stdout = old_stdout

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
				else:
					profile[result['property']['value']][result['annotation']['value']] = result['value']['value']

			directory = "data_dictionary/profiles/%s/" % (self.ptype)
			if not os.path.exists(directory):
				os.makedirs(directory)
			filename = directory + 'profile.json'
			with open(filename, 'w+') as p:
				json.dump(profile, p, sort_keys=True, indent=4)
		except:
			Utilities.PrintException()

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
					for key, value in data:
						if (annotation in value) and (('true' in value[annotation]) or ('indexAs' in annotation) or ('backwardCompatibleWith' in annotation)):
							display = True
					if display is True:
						print('### %s  ' % (Utilities.removeNS(annotation)))
						display = False
					for key, value in data:
						if (annotation in value) and ('true' in value[annotation]):
							print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s  )  " % (Utilities.removeNS(key), self.ptype, Utilities.addPrefixes(key).replace(':', '').lower()))
						elif (annotation in value) and (('indexAs' in annotation) and (value[annotation] != '')):
							print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s) indexes as [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s  )  " % (Utilities.removeNS(key), self.ptype, Utilities.addPrefixes(key).replace(':', '').lower(), Utilities.removeNS(value[annotation]), Utilities.addPrefixes(value[annotation]).replace(':', '').lower()))
						elif (annotation in value) and (('backwardCompatibleWith' in annotation) and (value[annotation] != '')):
							print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s) is compatible with %s  " % (Utilities.removeNS(key), self.ptype, Utilities.addPrefixes(key).replace(':', '').lower(), value[annotation]))
				print('')
				print('# Profile by property')
				print('')
				for keys, values in data:
					print('### %s  ' % (Utilities.addPrefixes(keys)))
					for key, value in sorted(values.items()):
						if key == 'acceptedValues':
							print("values displayed on form:  ")
							for j in value:
								if j['onForm'] == 'true':
									print('  * **%s** (%s)  ' % (Utilities.removeNS(j['label']), j['uri']))
							print('')
						elif (key != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") and (value != ''):
							print("%s: **%s**  " % (Utilities.removeNS(key), value))
		except:
			Utilities.PrintException()


class owlDocument(object):
	"""takes ontology.json as input; separates terms, properties, and instances, along with annotations, returning a dict object containing each data set"""
	def __init__(self):
		self.output = {'Terms': {}, 'Properties': {}, 'Values': {}}
		filename = 'data_dictionary/ontologies/Jupiter.json'
		with open(filename, 'r') as terms:
			owlDoc = json.load(terms)
			# the owl json consists of an self.index for each term, property, or instance
			for self.index in owlDoc:
				# check for type declaration (some individual instances do not contain a declaration, for reasons unknown)
				if '@type' in self.index:
					if "http://www.w3.org/2002/07/owl#Class" in self.index["@type"]:
						self.output = self.__add('Terms')
					elif ("http://www.w3.org/2002/07/owl#DatatypeProperty" in self.index["@type"]) or ("http://www.w3.org/2002/07/owl#ObjectProperty" in self.index["@type"]):
						self.output = self.__add('Properties')
					elif "http://www.w3.org/2002/07/owl#NamedIndividual" in self.index["@type"]:
						self.output = self.__add('Values')
				else:
					self.output = self.__add('Values')

	def __add(self, type):
		"""takes the type of self.index to be processes (resource, property, or instance (value); parses data and returns the processed data"""
		subject = self.index['@id']
		self.output[type][subject] = {}
		for predicate in self.index:
			self.output[type][subject][predicate] = []
			if predicate != '@id':
				for val in self.index[predicate]:
					if isinstance(val, dict):
						if '@value' in val:
							self.output[type][subject][predicate].append(val['@value'].replace('\n', ''))
						elif "@id" in val:
							if "http://www.w3.org/2001/XMLSchema#" not in val["@id"]:
								self.output[type][subject][predicate].append(val['@id'])
					else:
						if (type == "Values") and (val != "http://www.w3.org/2002/07/owl#NamedIndividual"):
							self.output[type][subject][predicate].append(val)
						else:
							pass
		return self.output

	def generate(self):
		print('# Jupiter Data Dictionary')
		print('')
		print("%s" % ddWelcome)
		# declares namespaces (set in config.py)
		print('# Namespaces')
		print('')
		for n in namespaces:
			print('   **%s:** %s  ' % (n['prefix'], n['uri']))
		print('')
		# defines annotations (set in config.py)
		print('# Definitions')
		print('')
		for d in definitions:
			print('   **%s** %s  ' % (d['term'], d['def']))
		print('')
		print('# Table of Contents')
		for t, resources in sorted(self.output.items()):
			print("### %s " % (t))
			for s, resource in sorted(resources.items()):
				print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s)  " % (Utilities.addPrefixes(s), Utilities.addPrefixes(s).replace(':', '').lower()))
			print('')
		print('')
		# sorts owlDoc alphabetically (so the display is always the same order)
		for t, resources in sorted(self.output.items()):
			# prints the key (Property, Term, or Value)
			print("# %s  " % (t))
			# iterates over each dictionary (resources)
			for s, resource in sorted(resources.items()):
				# prints the resource name, replacing the URI with a prefix (defined in config.py)
				print('### %s' % (Utilities.addPrefixes(s)))
				# iterates over the dictionary for this particular resource
				for annotationName, annotationValues in sorted(resource.items()):
					# checks to see if this is an empty list
					if len(annotationValues) > 0:
						print('')
						# prints the name of the annotation
						print('   **%s**   ' % (Utilities.addPrefixes(annotationName)))
						# prints annotation values line by line
						for value in annotationValues:
							print('  %s  ' % (value))
				# print("- [ ] Mark for editing")
				print('')
				print('***')


class Query(object):

	def __init__(self):
		self.compatability = []

	def generate(self):
		raise NotImplementedError()

	def getCompatibility(self, ptype):
		query = ''
		for key in namespaces.keys():
			query = query + "%: % " % (namespaces[key]['PREFIX'], namespaces[key]['uri'])
			query = "SELECT * WHERE {GRAPH ual:%s {?newProperty ual:backwardCompatibleWith ?oldProperty} }" % (ptype)
		sparql.setReturnFormat(JSON)
		sparql.setQuery(query)
		results = sparql.query().convert()
		for result in results['results']['bindings']:
			self.compatability.append((result['newProperty']['value'], result['oldProperty']['value']))


class Collection(Query):

	def __init__(self):
		self.construct = "CONSTRUCT { ?resource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Collection"
		self.where = "WHERE { ?resource info:hasModel 'Collection'^^xsd:string ; OPTIONAL { ?s ualids:is_community 'false'^^xsd:boolean } . OPTIONAL { ?s ualid:is_community 'false'^^xsd:boolean } . OPTIONAL { ?s ual:is_community 'false'^^xsd:boolean } . ?s ?p ?o}"
		self.getCompatibility('collection')
		self.generate()

	def generate(self):
		for pair in self.compatability:
			self.construct = self.construct + " ; "


class Community(Query):

	def __init__(self):
		self.getCompatibility('collection')
		self.generate()

	def generate(self):
		self.construct = "CONSTRUCT { ?resource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Object; rdf:type ual:Community } "
		self.where = "WHERE { ?resource info:hasModel 'Community'^^xsd:string} { ?resource info:hasModel 'Collection'^^xsd:string ; OPTIONAL { ?s ualids:is_community 'true'^^xsd:boolean } . OPTIONAL { ?s ualid:is_community 'true'^^xsd:boolean } . OPTIONAL { ?s ual:is_community 'true'^^xsd:boolean } . ?s ?p ?o}"


class Generic(Query):

	def __init__(self):
		self.getCompatibility('collection')
		self.generate()

	def generate(self):
		self.construct = "CONSTRUCT { ?resource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Object; rdf:type works:work } "
		self.where = "WHERE { ?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type ?type . filter(?type != 'Thesis') . ?resource ?p ?o }"


class Thesis(Query):

	def __init__(self):
		self.getCompatibility('collection')
		self.generate()

	def generate(self):
		self.construct = "CONSTRUCT { ?resource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Object; rdf:type works:work ; rdf:type bibo:Thesis } "
		self.where = "WHERE { ?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type 'Thesis'^^xsd:string ; ?p ?o}"


class QueryFactory():

	@staticmethod
	def getMigrationQuery(ptype):
		if (ptype == "collection"):
			return Collection()
		elif (ptype == "community"):
			return Community()
		elif (ptype == "thesis"):
			return Thesis()
		elif (ptype == "generic"):
			return Generic()
		else:
			return None


class Utilities():

	@staticmethod
	def addPrefixes(v):
		for line in namespaces:
			if line['uri'] in v:
				v = v.replace(line['uri'], line['prefix'] + ':')
		return v

	@staticmethod
	def removeNS(v):
		for line in namespaces:
			if line['uri'] in v:
				v = v.replace(line['uri'], '')
		return v

	@staticmethod
	def PrintException():
		exc_type, exc_obj, tb = sys.exc_info()
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename
		linecache.checkcache(filename)
		line = linecache.getline(filename, lineno, f.f_globals)
		print("EXCEPTION IN (%s, LINE %s '%s'): %s" % (filename, lineno, line.strip(), exc_obj))

if __name__ == "__main__":
	main()
