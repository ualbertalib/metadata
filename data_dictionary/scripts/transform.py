import json
from config import namespaces as ns
from config import definitions as defs
from config import welcome

def main():
	output = processOwlDocument()
	display(output)


### ADD TABLE OF CONTENTS


def processOwlDocument():
	""" separates terms, properties, and instances, along with annotations, returning a dict object containing each data set"""
	output = {'Terms': {}, 'Properties': {}, 'Values': {}}
	with open('../ontologies/Jupiter.json', 'r') as terms:
		owlDoc = json.load(terms)
		# the owl json consists of an index for each term, property, or instance
		for index in owlDoc:
			# check for type declaration (some individual instances do not contain a declaration, for reasons unknown)
			if '@type' in index:
				# iterate over the types
				for types in index['@type']:
					# if this index is a Class (i.e. a "term"), add it to the output as such

					if types == "http://www.w3.org/2002/07/owl#Class":
						output = add('Terms', index, output)
					elif (types == "http://www.w3.org/2002/07/owl#DatatypeProperty") or (types == "http://www.w3.org/2002/07/owl#ObjectProperty"):
						output = add('Properties', index, output)
					elif (types == "http://www.w3.org/2002/07/owl#NamedIndividual"):
						output = add('Values', index, output)
			# if there is no class, it is by default an instance (this needs to corrected in the owl document, but it could be a bug in protege)
			else:
				output = add('Values', index, output)
	return output


def add(type, resource, output):
	"""takes the type of index to be processes (resource, property, or instance (value); parses data and returns the processed data"""
	# the subject of the resource is found in the @id property
	subject = resource['@id']
	output[type][subject] = {}
	for predicate in resource:
		output[type][subject][predicate] = []
		# predicates store a list of dictionaries, we iterate over those
		for values in resource[predicate]:
			if '@type' in values:
					# store the value as a string
				output[type][subject][predicate].append(values['@type'])
			# @value contains the value expressed (i.e rdfs:label is predicate, @value is 'Creator')
			if '@value' in values:
					# store the value as a string
				output[type][subject][predicate].append(values['@value'].replace('\n', ''))
				# @id is used if the value is a URI (i.e. rdfs:isDefinedBy purl.org/dc/terms/)
			elif "@id" in values:
				output[type][subject][predicate].append(values['@id'])
	return(output)


def display(output):
	print('# Jupiter Data Dictionary')
	print('   ')
	print("%s" % welcome)

	# defines annotations (set in config.py)
	print('# Definitions')
	print('   ')
	for d in defs:
		print('   **%s** %s  ' % (d['term'], d['def']))
	print('   ')
	# declares namespaces (set in config.py)
	print('# Namespaces')
	print('   ')
	for n in ns:
		print('   **%s:** %s  ' % (n['prefix'], n['uri']))
	print('   ')
	print('# Table of Contents')
	for t, resources in sorted(output.items()):
		print("### %s " % (t))
		for s, resource in sorted(resources.items()):
			print(" [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s) *" % (addPrefixes(s), removeNS(s)))
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


if __name__ == "__main__":
	main()
