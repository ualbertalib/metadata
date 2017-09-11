import json
import csv
from config import namespaces as ns
from config import definitions as defs
from config import ddWelcome, profileWelcome, profileDefinitions
from SPARQLWrapper import SPARQLWrapper, JSON


def main():
	#output = processOwlDocument()
	#processProfileData(output)
	#shipProfileToTriples()
	#fetchFromTriples()
	profileDisplay("generic")
	#dataDictionaryDisplay(output)

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


def profileDisplay(ptype):
	filename = "../profiles/%s/profile.json" % (ptype)
	with open(filename) as profileData:
		dataOriginal = json.load(profileData)
		data = sorted(dataOriginal.items())
		print('# Jupiter %s Application Profile' % (ptype.title()))
		print('')
		print("%s" % profileWelcome)
		print('')
		print('# Namespaces  ')
		for n in ns:
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
			if display == True:
				print('### %s  ' % (removeNS(annotation)))
				display = False
			for key, value in data:
				if (annotation in value) and ('true' in value[annotation]):
					print(" [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s) *" % (removeNS(key), addPrefixes(key).replace(':', '').lower()))
				elif (annotation in value) and ( ('indexAs' in annotation) and (value[annotation] !='')):
					print(" [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s) indexes as [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s)  " % (removeNS(key), addPrefixes(key).replace(':', '').lower(), removeNS(value[annotation]), addPrefixes(value[annotation]).replace(':', '').lower()))
				elif (annotation in value) and ( ('backwardCompatibleWith' in annotation) and (value[annotation] !='')):
					print(" [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s) is compatible with [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s)  " % (removeNS(key), addPrefixes(key).replace(':', '').lower(), removeNS(value[annotation]), addPrefixes(value[annotation]).replace(':', '').lower()))
		print('')
		print('# Profile by property')
		print('')
		for key, values in data:
			print('### %s  ' % (addPrefixes(key)))
			for i in values:
				if i == 'acceptedValues':
					print("values displayed on form:  ")
					for j in values[i]:
						if j['onForm'] == 'true':
							print('  * **%s** (%s)  ' % (removeNS(j['label']), j['uri']))
					print('')
				elif (i != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type") and (values[i] != ''):
					print("%s: **%s**  " % (removeNS(i), values[i]))



def dataDictionaryDisplay(output):
	print('# Jupiter Data Dictionary')
	print('')
	print("%s" % ddWelcome)
	# declares namespaces (set in config.py)
	print('# Namespaces')
	print('')
	for n in ns:
		print('   **%s:** %s  ' % (n['prefix'], n['uri']))
	print('')
	# defines annotations (set in config.py)
	print('# Definitions')
	print('')
	for d in defs:
		print('   **%s** %s  ' % (d['term'], d['def']))
	print('')
	print('# Table of Contents')
	for t, resources in sorted(output.items()):
		print("### %s " % (t))
		for s, resource in sorted(resources.items()):
			print(" [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s) *" % (addPrefixes(s), addPrefixes(s).replace(':', '').lower()))
		print('')
	print('')
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
					print('')
					# prints the name of the annotation
					print('   **%s**   ' % (addPrefixes(annotationName)))
					# prints annotation values line by line
					for value in annotationValues:
						print('  %s  ' % (value))
			# print("- [ ] Mark for editing")
			print('')
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


def fetchFromTriples():
	sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
	for ptype in ["collection", "generic", "thesis"]:
		profile = {}
		query = "PREFIX ual: <http://terms.library.ualberta.ca/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT * WHERE {GRAPH ual:%s {?property ?annotation ?value} }" % (ptype)
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

		filename = '../profiles/%s/profile.json' % ptype
		with open(filename, 'w+') as p:
			json.dump(profile, p, sort_keys=True, indent=4)
	print("profile data has been shipped from triplestore to json")


def processProfileData(output):

	"""processed the orignal data dictionary spreadsheet from google sheets""" 

	for ptype in ["collection", "generic", "thesis"]:
		profiles = []
		filename = "../profiles/original_profile_data/%s.csv" % (ptype)
		with open(filename, newline='') as data:
			reader = csv.DictReader(data)
			for row in reader:
				profile = {
					"uri": row['uri'],  # string
					"conf": {
						"required": row['required'],  # enumerated string: "optional", "required"
						"repeat": row['repeat'],  # boolean
						"facet": row['facet'],  # boolean
						"tokenize": "",  # boolean
						"display": row['display'],  # boolean
						"sort": row['sort'],  # boolean
						"onForm": row['onForm'],  # boolean
						"propertyName": "",  # string
						"displayLabel": row['displayLabel'],  # string
						"acceptedValues": [],
						"dataType": row['dataType'],  # enumerated string: "string", "enumeratedString", "enumeratedURI", "dateTime"
						"comments": row["comments"].replace("\"", "'"),  # string
						"backwardCompatibleWith": row["backwardCompatibleWith"],  # string
						"indexAs": row['indexAs'],  # string
						"definedBy": row['definedBy']  # string
					}
				}
				profile['conf']["propertyName"] = output["Properties"][row['uri']]['http://www.w3.org/2000/01/rdf-schema#label'][0]
				if "http://www.w3.org/2000/01/rdf-schema#range" in output["Properties"][row['uri']]:
						for valueKey, vals in output['Values'].items():
							if not set(output["Properties"][row['uri']]["http://www.w3.org/2000/01/rdf-schema#range"]).isdisjoint(vals['@type']):
								profile['conf']['acceptedValues'].append({"uri": valueKey, "label": vals["http://www.w3.org/2000/01/rdf-schema#label"][0], "onForm": "True"})
				profiles.append(profile)
			filename = '../profiles/%s/profile.json' % ptype
			with open(filename, 'w+') as p:
				json.dump(profiles, p, sort_keys=True, indent=4)
	print('profile data has been shipped from csv to json')


def shipProfileToTriples():
	sparql = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/terms/sparql")
	sparql.setMethod("POST")
	for ptype in ["collection", "generic", "thesis"]:
		filename = "../profiles/%s/profile.json" % (ptype)
		with open(filename) as data:
			for item in json.load(data):
				query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA { GRAPH ual:%s { <%s> rdf:type rdf:Property" % (ptype, item['uri'])
				for key in item['conf']:
					if key == 'acceptedValues':
						for triple in item['conf'][key]:
							addValue = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX ual: <http://terms.library.ualberta.ca/> INSERT DATA { GRAPH ual:instances { <%s> rdfs:label \"%s\" ; ual:onForm \"%s\" } } " % (triple['uri'], triple['label'], "true")
							print(addValue)
							print(' ')
							sparql.setQuery(addValue)
							sparql.query()
							query = query + "; ual:acceptedValue <%s>" % (triple['uri'])
					elif isinstance(item['conf'][key], str) and ("http" in item['conf'][key]):
						query = query + "; ual:%s <%s> " % (key, item['conf'][key])
					elif item['conf'][key] == "none":
						query = query + "; ual:%s \"%s\"" % (key, "")
					else:
						query = query + "; ual:%s \"%s\"" % (key, str(item['conf'][key]).lower())
				query = query + "} }"
				sparql.setQuery(query)
				sparql.query()
				print(query)
				print('')
	print("profile data has been shipped from json data to triplestore")

if __name__ == "__main__":
	main()
