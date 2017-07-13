from SPARQLWrapper import SPARQLWrapper, JSON
import json
import os

"""This script compares each of those profiles with the contents of ERA to determine an approximate
match based on a complete family name match and a first initial given name match."""

# There are 2479 ORCID profiles containing the term "Univeristy of Alberta"
# Conservative rules: 
#	189 profiles correlate with 204 ERA resources at 99% reliability
# Liberal rules: 
#	867 profiles correlate with 2273 ERA resources
#	524 of these profiles correlate with only one resource and have approximately 80% reliability
# 	remaining 343 profiles which correlate to 1749 resources have reliability well below 50%




def main():
	orcs = orcids()
	results = getERAData()
	getMatches(results, orcs)


def orcids():

	"""generate a list of all orcid profiles"""

	# stores all orcid profiles
	orcids = []
	# access a json file containing all university of alberta affiliated ORCID profiles
	for filename in os.listdir(os.getcwd()):
		with open(filename, 'r+') as f:
			if filename.endswith('.json'):
				j = json.load(f)
				# stores an individual orcid profile
				person = {}
				# as long as an orcid profile has a name, add it to the orcid profile
				if 'name' in j and j['name'] is not None:
					if 'given-names' in j['name'] and j['name']['given-names'] is not None:
						person['given'] = j['name']['given-names']['value']
					if 'family-name' in j['name'] and j['name']['family-name'] is not None:
						person['family'] = j['name']['family-name']['value']
					if 'path' in j['name'] and j['name']['path'] is not None:
						person['id'] = j['name']['path']
				# append the profile to the list of profiles
				orcids.append(person)
	return orcids


def getERAData():
	
	"""Query triplestore for all ERA resources, creators, and dissertants"""

	query = """prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix dcterm: <http://purl.org/dc/terms/> select * WHERE {	?resource <info:fedora/fedora-system:def/model#hasModel> 'GenericFile'^^xsd:string . OPTIONAL { ?resource <http://id.loc.gov/vocabulary/relators/dis> ?dis} FILTER (strlen(?dis)>1 ) OPTIONAL { ?resource dcterm:creator ?creator } }"""
	sparql = SPARQLWrapper("http://sheff.library.ualberta.ca:9999/blazegraph/namespace/fcrepo/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	return results


def getMatches(results, orcs):
	print("{ \"results\": [")
	"""Iterate over ORCID profiles, querying ERA data for matching names, returning a list of matches"""

	for person in orcs:
		# a result contains one or more matches for a given orcid profile
		creator = None
		# a family name must exist in the orcid profile
		if 'family' in person and 'family' != '':
			familyName = person['family']
			# triplestore results are a list, therefore we iterate over each result set to find a match
			for result in results["results"]["bindings"]:
				if 'creator' in result or 'dis' in result:
					# check for a family name match against creator or dissertent and assign
					if ('creator' in result) and ("," in result['creator']['value']) and (familyName == result['creator']['value'].split(",")[0]):
						creator = result['creator']['value']
					elif ('creator' in result) and (familyName == result['creator']['value']):
						creator = result['creator']['value']
					elif ('dis' in result) and ("," in result['dis']['value']) and (familyName == result['dis']['value'].split(",")[0]):
						creator = result['dis']['value']
					elif ('dis' in result) and (familyName == result['dis']['value']):
						creator = result['dis']['value']
					# check for a given name in the orcid profile and check for a first initial match against the ERA first initial
					if creator is not None:
						if ('given' in person) and ("," in creator):
							ORCinit = person['given'].strip()[0:1]
							ERAinit = creator.split(",")[1].strip()[0:1]
							# below is a more liberal implementation based on first initial first name recognition. below requires entire first name recognition
							# if person['given'].strip() == creator.split(",")[1].strip():
							if ORCinit == ERAinit:
								# add the match to the result
								print("{\"era\": {\"resource\": \"" + result['resource']['value'] + "\", \"creator\": \"" + str(creator) + "\"}, \"orcid\": " + "{ \"id\": \"" + person['id'] + "\", \"family\": \"" + person['family'] + "\", \"given\": \"" + person['given'] +  "\" } },")
						# if there is no given name, we need to take the match based on last name alone
						else:
							# add the partial match to the output
							print("{\"era\": {\"resource\": \"" + result['resource']['value'] + "\", \"creator\": \"" + str(creator) + "\"}, \"orcid\": " + "{ \"id\": \"" + person['id'] + "\", \"family\": \"" + person['family'] + "\", \"given\": \"" + person['given'] +  "\"} },")
						creator = None
	print("]}")

if __name__ == "__main__":
	main()
