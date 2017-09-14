import json
from config import namespaces, profileWelcome, profileDefinitions, path
import os


class owlDocument(object):
	""" separates terms, properties, and instances, along with annotations, returning a dict object containing each data set"""
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
					self.output = __add('Values')


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


class Profiler(object):
	def __init__(self, ptype):
		self.ptype = ptype
		self.__createProfile()

	def __createProfile(self):
		filename = "%s/profiles/%s/profile.json" % (path, self.ptype)
		with open(filename, 'r+') as profileData:
			dataOriginal = json.load(profileData)
			data = sorted(dataOriginal.items())
			print('# Jupiter %s Application Profile' % (self.ptype.title()))
			print('')
			print("%s" % profileWelcome)
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
					print('### %s  ' % (removeNS(annotation)))
					display = False
				for key, value in data:
					if (annotation in value) and ('true' in value[annotation]):
						print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_generic.md#%s  )  " % (removeNS(key), addPrefixes(key).replace(':', '').lower()))
					elif (annotation in value) and (('indexAs' in annotation) and (value[annotation] != '')):
						print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_generic.md#%s) indexes as [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s  )  " % (removeNS(key), addPrefixes(key).replace(':', '').lower(), removeNS(value[annotation]), addPrefixes(value[annotation]).replace(':', '').lower()))
					elif (annotation in value) and (('backwardCompatibleWith' in annotation) and (value[annotation] != '')):
						print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_generic.md#%s) is compatible with %s  " % (removeNS(key), addPrefixes(key).replace(':', '').lower(), value[annotation]))
			print('')
			print('# Profile by property')
			print('')
			for keys, values in data:
				print('### %s  ' % (addPrefixes(keys)))
				for key, value in sorted(values.items()):
					if key == 'acceptedValues':
						print("values displayed on form:  ")
						for j in value:
							if j['onForm'] == 'true':
								print('  * **%s** (%s)  ' % (removeNS(j['label']), j['uri']))
						print('')
					elif (key != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") and (value != ''):
						print("%s: **%s**  " % (removeNS(key), value))


def addPrefixes(v):
	for line in namespaces:
		if line['uri'] in v:
			v = v.replace(line['uri'], line['prefix'] + ':')
	return v

def removeNS(v):
	for line in namespaces:
		if line['uri'] in v:
			v = v.replace(line['uri'], '')
	return v
