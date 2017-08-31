import json
from config import namespaces as ns
from config import definitions as defs
from config import welcome

def main():
	#displayWelcome()
	output = processOwlDocument()
	#displayBody(output)
	resetProfiles(output)


def processOwlDocument():
	""" separates terms, properties, and instances, along with annotations, returning a dict object containing each data set"""
	output = {'Terms': {}, 'Properties': {}, 'Values': {}}
	with open('../ontologies/Jupiter.json', 'r') as terms:
		owlDoc = json.load(terms)
		# the owl json consists of an index for each term, property, or instance
		for index in owlDoc:
			# check for type declaration (some individual instances do not contain a declaration, for reasons unknown)
			if '@type' in index:
				if "http://www.w3.org/2002/07/owl#Class" in index["@type"]:
					output = add('Terms', index, output)
				elif ("http://www.w3.org/2002/07/owl#DatatypeProperty" in index["@type"]) or ("http://www.w3.org/2002/07/owl#ObjectProperty" in index["@type"]):
					output = add('Properties', index, output)
				elif "http://www.w3.org/2002/07/owl#NamedIndividual" in index["@type"]:
					output = add('Values', index, output)
			else:
				output = add('Values', index, output)
	return output


def add(type, resource, output):
	"""takes the type of index to be processes (resource, property, or instance (value); parses data and returns the processed data"""
	subject = resource['@id']
	output[type][subject] = {}
	for predicate in resource:
		output[type][subject][predicate] = []
		if predicate != '@id':
			for val in resource[predicate]:
				if isinstance(val, dict):
					if '@value' in val:
						output[type][subject][predicate].append(val['@value'].replace('\n', ''))
					elif "@id" in val:
						if "http://www.w3.org/2001/XMLSchema#" not in val["@id"]:
							output[type][subject][predicate].append(val['@id'])
				else:
					if (type == "Values") and (val != "http://www.w3.org/2002/07/owl#NamedIndividual"):
						output[type][subject][predicate].append(val)
					else:
						pass
	return(output)


def displayWelcome():
	print('# Jupiter Data Dictionary')
	print('   ')
	print("%s" % welcome)
	# declares namespaces (set in config.py)
	print('# Namespaces')
	print('   ')
	for n in ns:
		print('   **%s:** %s  ' % (n['prefix'], n['uri']))
	print('   ')
	# defines annotations (set in config.py)
	print('# Definitions')
	print('   ')
	for d in defs:
		print('   **%s** %s  ' % (d['term'], d['def']))
	print('   ')


def displayBody(output):
	print('# Table of Contents')
	for t, resources in sorted(output.items()):
		print("### %s " % (t))
		for s, resource in sorted(resources.items()):
			print(" [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s) *" % (addPrefixes(s), addPrefixes(s).replace(':', '').lower()))
		print('   ')
	print('   ')
	# sorts output alphabetically (so the display is always the same order)
	for t, resources in sorted(output.items()):
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
					print('   ')
					# prints the name of the annotation
					print('   **%s**   ' % (addPrefixes(annotationName)))
					# prints annotation values line by line
					for value in annotationValues:
						print('  %s  ' % (value))
			# print("- [ ] Mark for editing")
			print('   ')
			print('***')


def addPrefixes(v):
	for line in ns:
		if line['uri'] in v:
			v = v.replace(line['uri'], line['prefix'] + ':')
	return v


def removeNS(v):
	for line in ns:
		if line['uri'] in v:
			v = v.replace(line['uri'], '')
	return v


def resetProfiles(output):
	profiles = []
	for propertyKey, propertyValues in output['Properties'].items():
		profile = {
			"uri": propertyKey,  # string
			"implemented": None,  # boolean
			"config": {
				"obligation": None,  # enumerated string: "optional", "required"
				"repeat": None,  # boolean
				"facet": None,  # boolean
				"tokenize": None,  # boolean
				"display": None,  # boolean
				"sort": None,  # boolean
				"onForm": None,  # boolean
				"propertyName": None,  # string
				"displayLabel": None,  # string
				"acceptedValues": [],
				"dataType": None,  # enumerated string: "string", "enumeratedString", "enumeratedURI", "dateTime"
				"comments": None,  # string
				"backwardCompatibleWith": [],  # string
				"indexWith": [],  # string
				"definedBy": None  # string
			}
		}
		if 'http://www.w3.org/2000/01/rdf-schema#label' in propertyValues:
			profile['config']["propertyName"] = propertyValues['http://www.w3.org/2000/01/rdf-schema#label'][0]
		profile['config']['definedBy'] = "https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s" % addPrefixes(propertyKey).replace(":", "").lower()
		if "http://www.w3.org/2000/01/rdf-schema#range" in propertyValues:
			for valueKey, vals in output['Values'].items():
				if propertyValues["http://www.w3.org/2000/01/rdf-schema#range"] == vals['@type']:
					profile['config']['acceptedValues'].append({"uri": valueKey, "label": vals["http://www.w3.org/2000/01/rdf-schema#label"][0], "implemented": None})
		profiles.append(profile)
		for profileType in ["collection", "generic", "thesis"]:
			filename = '../profiles/%s/profile.json' % profileType
			with open(filename, 'w+') as p:
				json.dump(profiles, p)


# def updateProfiles(output):


# def editForm():





if __name__ == "__main__":
	main()
