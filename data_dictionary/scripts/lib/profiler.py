from utilities import PrintException, removeNS, addPrefixes
from config import namespaces, profileWelcome, profileDefinitions, sparql
import json
import sys
import os
from SPARQLWrapper import JSON


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
							print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s  )  " % (removeNS(key), self.ptype, addPrefixes(key).replace(':', '').lower()))
						elif (annotation in value) and (('indexAs' in annotation) and (value[annotation] != '')):
							print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s) indexes as [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s  )  " % (removeNS(key), self.ptype, addPrefixes(key).replace(':', '').lower(), removeNS(value[annotation]), addPrefixes(value[annotation]).replace(':', '').lower()))
						elif (annotation in value) and (('backwardCompatibleWith' in annotation) and (value[annotation] != '')):
							print("  * [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_%s.md#%s) is compatible with %s  " % (removeNS(key), self.ptype, addPrefixes(key).replace(':', '').lower(), value[annotation]))
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
		except:
			PrintException()