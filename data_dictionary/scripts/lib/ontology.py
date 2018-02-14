from config import namespaces, definitions, ddWelcome
from utilities import addPrefixes
import json

class owlDocument(object):
	"""takes ontology.json as input; separates terms, properties, and instances, along with annotations, returning a dict object containing each data set"""
	def __init__(self):
		self.output = {'Terms': {}, 'Properties': {}, 'Values': {}}
		filename = '../../ontologies/Jupiter.json'
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
				print("  * [%s](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#%s)  " % (addPrefixes(s), addPrefixes(s).replace(':', '').lower()))
			print('')
		print('')
		# sorts owlDoc alphabetically (so the display is always the same order)
		for t, resources in sorted(self.output.items()):
			# prints the key (Property, Term, or Value)
			print("# %s  " % (t))
			# iterates over each dictionary (resources)
			for s, resource in sorted(resources.items()):
				# prints the resource name, replacing the URI with a prefix (defined in config.py)
				print('### %s' % (addPrefixes(s)))
				# iterates over the dictionary for this particular resource
				for annotationName, annotationValues in sorted(resource.items()):
					# checks to see if this is an empty list
					if len(annotationValues) > 0:
						print('')
						# prints the name of the annotation
						print('   **%s**   ' % (addPrefixes(annotationName)))
						# prints annotation values line by line
						for value in annotationValues:
							print('  %s  ' % (value))
				# print("- [ ] Mark for editing")
				print('')
				print('***')
