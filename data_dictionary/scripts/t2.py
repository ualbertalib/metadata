import json
from config import namespaces as ns
from config import definitions as defs
from config import welcome


def main():
	with open('../ontologies/Jupiter.json', 'r') as resources:
		Core(json.load(resources))


############################################################################
############################################################################


class Core:
	def __init__(self, resources):
		self.resources = resources
		self.collection = Collection()
		self.processResources()
		Renderer.renderIntroduction()
		Renderer.renderNamespaces()
		Renderer.renderDefinitions()

	def processResources(self):
		for resource in self.resources:
			# check for type declaration (some individual instances do not contain a declaration, for reasons unknown)
			if '@type' in resource:
				if "http://www.w3.org/2002/07/owl#Class" in resource["@type"]:
					term = Terms().setAnnotations(resource)
					self.collection.addResource(term)
				elif ("http://www.w3.org/2002/07/owl#DatatypeProperty" in resource["@type"]) or ("http://www.w3.org/2002/07/owl#ObjectProperty" in resource["@type"]):
					prop = Properties().setAnnotations(resource)
					self.collection.addResource(prop)
				elif "http://www.w3.org/2002/07/owl#NamedIndividual" in resource["@type"]:
					value = Values().setAnnotations(resource)
					self.collection.addResource(value)
			else:
				value = Values()
				value = value.setAnnotations(resource)
				self.collection.addResource(value)


############################################################################
############################################################################


class Collection:
	def __init__(self):
		self.terms = {}
		self.properties = {}
		self.values = {}

	def addResource(self, resource):
		if resource.resourceType == "Terms":
			self.terms[self.subject] = resource
		if resource.resourceType == "Properties":
			self.properties[self.subject] = resource
		if resource.resourceType == "Values":
			self.values[self.subject] = resource

	def getResources(self, resource):
		print(resource)
		if resource.resourceType == "Terms":
			return self.terms
		if resource.resourceType == "Properties":
			return self.properties
		if resource.resourceType == "Values":
			return self.values



############################################################################
############################################################################


class Resource(object):
	def __init__(self):
		self.annotations = {}

	def setAnnotations(self, resource):
		self.resource = resource
		self.subject = self.resource['@id']
		for annotation in self.resource:
			self.annotations[annotation] = []
			if annotation != '@id':
				for val in self.resource[annotation]:
					if isinstance(val, dict):
						if '@value' in val:
							self.annotations[annotation].append(val['@value'].replace('\n', ''))
						elif "@id" in val:
							if "http://www.w3.org/2001/XMLSchema#" not in val["@id"]:
								self.annotations[annotation].append(val['@id'])
					else:
						if (type == "Values") and (val != "http://www.w3.org/2002/07/owl#NamedIndividual"):
							self.annotations[annotation].append(val)
						else:
							pass

class Terms(Resource):
	def __init__(self):
		super(Terms, self).__init__()
		self.resourceType = "Terms"


class Properties(Resource):
	def __init__(self):
		super(Properties, self).__init__()
		self.resourceType = "Properties"


class Values(Resource):
	def __init__(self):
		super(Values, self).__init__()
		self.resourceType = "Values"

############################################################################
############################################################################


class Renderer:
	def __init__(self, collection):
		pass

	def renderIntroduction(self):
		print('# Jupiter Data Dictionary')
		print('   ')
		print("%s" % welcome)
		# declares namespaces (set in config.py)

	def renderNamespaces(self):
		print('# Namespaces')
		print('   ')
		for n in ns:
			print('   **%s:** %s  ' % (n['prefix'], n['uri']))
		print('   ')
		# defines annotations (set in config.py)

	def renderDefinitions(self):
		print('# Definitions')
		print('   ')
		for d in defs:
			print('   **%s** %s  ' % (d['term'], d['def']))
		print('   ')

	def renderTOC(self, collection):
		print('# Table of Contents')
		for key in ["Terms", "Properties", "Values"]:
			print("### %s " % (key))
			for resource in collection.getResources(key):
				print(" [%s](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#%s) *" % (self.renderPrefixes(resource.subject), self.renderPrefixes(resource.subject).replace(':', '').lower()))
			print('   ')
		print('   ')

	def renderBody(self, collection):
		# sorts output alphabetically (so the display is always the same order)
		for key in ["Terms", "Properties", "Values"]:
			# prints the key (Property, Term, or Value)
			print("# %s  " % (key))
			# iterates over each dictionary (resources)
			for resource in collection.getResources(key):
				# prints the resource name, replacing the URI with a prefix (defined in config.py)
				print('### %s' % (self.renderPrefixes(resource.subject)))
				# iterates over the dictionary for this particular resource
				for annotationName, annotationValues in sorted(resource.annotations):
					# checks to see if this is an empty list
					if len(annotationValues) > 0:
						print('   ')
						# prints the name of the annotation
						print('   **%s**   ' % (self.renderPrefixes(annotationName)))
						# prints annotation values line by line
						for value in annotationValues:
							print('  %s  ' % (value))
				# print("- [ ] Mark for editing")
				print('   ')
			print('***')

	def renderPrefixes(v):
		for line in ns:
			if line['uri'] in v:
				v = v.replace(line['uri'], line['prefix'] + ':')
		return v


if __name__ == "__main__":
	main()
