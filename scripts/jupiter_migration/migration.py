from config import sparqlTerms, mig_ns, sparql_mig_test, sparql_mig_simple, sparql_mig_dev
from transformation import TransformationFactory
from SPARQLWrapper import JSON
from utilities import removeNS, PrintException
import concurrent.futures
import requests

def main():
	for ptype in ["collection", "community", "generic", "thesis"]:
		mig = QueryFactory.getMigrationQuery(ptype)
		for q in mig.queries:
			DTO = DataFactory.getData(q, mig)
			DTO.transformData()

class Query(object):
	""" Query objects are dynamically generated, and contain SPARQL CONSTRUCT queries with input from the jupiter application profile """
	def __init__(self, ptype, sparqlTerms=sparqlTerms, sparqlData=sparql_mig_test):
		self.mapping = []
		self.sparqlTerms = sparqlTerms  # doesn't need to change (the terms store doesn't change)
		self.sparqlData = sparqlData  # sets the triple store from which to get data (simple, test, or dev)
		self.queries = []
		self.prefixes = ""
		self.filename = ""
		for ns in mig_ns:
			self.prefixes = self.prefixes + " PREFIX %s: <%s> " % (ns['prefix'], ns['uri'])
		self.getMappings()
		self.generateQueries()


	def getMappings(self):
		query = "prefix ual: <http://terms.library.ualberta.ca/>SELECT * WHERE {GRAPH ual:%s {?newProperty ual:backwardCompatibleWith ?oldProperty} }" % (self.ptype)
		self.sparqlTerms.setReturnFormat(JSON)
		self.sparqlTerms.setQuery(query)
		results = self.sparqlTerms.query().convert()
		for result in results['results']['bindings']:
			self.mapping.append((result['newProperty']['value'], result['oldProperty']['value']))

	def generateQueries(self):
		pass


class Collection(Query):
	def __init__(self):
		self.ptype = 'collection'
		self.construct = "CONSTRUCT { ?resource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Collection"
		self.where = ["WHERE { ?resource info:hasModel 'Collection'^^xsd:string . OPTIONAL { ?resource ualids:is_community 'false'^^xsd:boolean } . OPTIONAL { ?resource ualid:is_community 'false'^^xsd:boolean } . OPTIONAL { ?resource ual:is_community 'false'^^xsd:boolean }"]
		self.select = None
		super().__init__(self.ptype)

	def generateQueries(self):
		for where in self.where:
			construct = self.construct
			for pair in self.mapping:
				construct = "%s ; <%s> ?%s" % (construct, pair[0], removeNS(pair[0]))
				where = " %s . OPTIONAL { ?resource <%s> ?%s }" % (where, pair[1], removeNS(pair[0]))
			self.queries.append( ("%s %s } %s }" % (self.prefixes, construct, where), "" ) )


class Community(Query):
	def __init__(self):
		self.ptype = 'community'
		self.construct = "CONSTRUCT { ?resource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Object; rdf:type ual:Community"
		self.where = ["WHERE { ?resource info:hasModel 'Collection'^^xsd:string ; OPTIONAL { ?resource ualids:is_community 'true'^^xsd:boolean } . OPTIONAL { ?resource ualid:is_community 'true'^^xsd:boolean } . OPTIONAL { ?resource ual:is_community 'true'^^xsd:boolean }"]
		self.select = None
		super().__init__(self.ptype)

	def generateQueries(self):
		for where in self.where:
			construct = self.construct
			for pair in self.mapping:
				construct = "%s ; <%s> ?%s" % (construct, pair[0], removeNS(pair[0]))
				where = " %s . OPTIONAL { ?resource <%s> ?%s }" % (where, pair[1], removeNS(pair[0]))
			self.queries.append( ( "%s %s } %s }" % (self.prefixes, construct, where), "" ) )


class Generic(Query):
	def __init__(self):
		self.ptype = 'generic'
		self.construct = "CONSTRUCT { ?resource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Object; rdf:type works:work"
		self.where = []
		self.select = "SELECT distinct ?collection WHERE { ?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type ?type . filter(?type != 'Thesis'^^xsd:string) . ?resource ualids:hasCollectionId ?collection }"
		super().__init__(self.ptype)

	def generateQueries(self):
		query = "%s %s" % (self.prefixes, self.select)
		self.sparqlData.setReturnFormat(JSON)
		self.sparqlData.setQuery(query)
		results = self.sparqlData.query().convert()
		for result in results['results']['bindings']:
			where = "WHERE {  ?resource ualids:hasCollectionId '%s'^^xsd:string ; info:hasModel 'GenericFile'^^xsd:string ; dcterm:type ?type . filter(?type != 'Thesis'^^xsd:string)" % (result['collection']['value'])
			construct = self.construct
			for pair in self.mapping:
				construct = "%s ; <%s> ?%s" % (construct, pair[0], removeNS(pair[0]))
				where = " %s . OPTIONAL { ?resource <%s> ?%s }" % (where, pair[1], removeNS(pair[0]))
			self.queries.append( ( "%s %s } %s }" % (self.prefixes, construct, where), result['collection']['value'] ) )

class Thesis(Query):
	def __init__(self):
		self.ptype = 'thesis'
		self.construct = "CONSTRUCT { ?resource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Object; rdf:type works:work ; rdf:type bibo:Thesis"
		self.where = []
		self.select = "SELECT distinct ?year_created WHERE { ?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type 'Thesis'^^xsd:string ; ualids:year_created ?year_created }"
		super().__init__(self.ptype)

	def generateQueries(self):
		query = "%s %s" % (self.prefixes, self.select)
		self.sparqlData.setReturnFormat(JSON)
		self.sparqlData.setQuery(query)
		results = self.sparqlData.query().convert()
		for result in results['results']['bindings']:
			where = "WHERE { ?resource ualid:year_created '%s'^^xsd:string ; info:hasModel 'GenericFile'^^xsd:string ; dcterm:type 'Thesis'^^xsd:string" % (result['year_created']['value'])
			construct = self.construct
			for pair in self.mapping:
				construct = "%s ; <%s> ?%s" % (construct, pair[0], removeNS(pair[0]))
				where = " %s . OPTIONAL { ?resource <%s> ?%s }" % (where, pair[1], removeNS(pair[0]))
			self.queries.append(( "%s %s } %s }" % (self.prefixes, construct, where), result['year_created']['value']))


class QueryFactory():

	@staticmethod
	def getMigrationQuery(ptype):
		""" returns a specified query object depending on the type passed in"""
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


class Data(object):
	def __init__(self, q, sparqlData, sparqlTerms):
		self.q = q
		self.query = q[0]
		self.sparqlData = sparqlData
		self.sparqlTerms = sparqlTerms
		self.filename = ""
		self.output = []

	def transformData(self):
		self.sparqlData.setMethod("GET")
		self.sparqlData.setReturnFormat(JSON)
		self.sparqlData.setQuery(self.query)
		results = self.sparqlData.query().convert()['results']['bindings']
		for result in results:
			result = TransformationFactory().getTransformation(result)
			for triple in result:
				s = "<%s>" % (str(triple['subject']['value']))
				p = "<%s>" % (str(triple['predicate']['value']))
				if triple['object']['type'] == 'uri':
					o = "<%s>" % (str(triple['object']['value']))
				else:
					o = "\"%s\"" % (str(triple['object']['value']))
				self.output.append("%s %s %s . \n" % (s, p, o))
		with open(self.filename, "w+") as f:
			f.writelines(self.output)

		#with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
		#	future_to_result = {executor.submit(self.processResults, results, query): result for result in results}
		#	for future in concurrent.futures.as_completed(future_to_result):
		#		result = future_to_result[future]
		#		try:
		#			future.result()
		#		except Exception:
		#			PrintException()





class CollectionData(Data):
	def __init__(self, q, sparqlData, sparqlTerms):
		super().__init__(q, sparqlData, sparqlTerms)
		self.filename = 'results/collection.nt'

class CommunityData(Data):
	def __init__(self, q, sparqlData, sparqlTerms):
		super().__init__(q, sparqlData, sparqlTerms)
		self.filename = 'results/community.nt'


class ThesisData(Data):
	def __init__(self, q, sparqlData, sparqlTerms):
		super().__init__(q, sparqlData, sparqlTerms)
		self.filename = "results/thesis/%s.nt" % (self.q[1])


class GenericData(Data):
	def __init__(self, q, sparqlData, sparqlTerms):
		super().__init__(q, sparqlData, sparqlTerms)
		self.filename = "results/generic/%s.nt" % (self.q[1])


class DataFactory():
	@staticmethod
	def getData(q, mig):
		""" returns a specified query object depending on the type passed in"""
		if (mig.ptype == "collection"):
			return CollectionData(q, mig.sparqlData, mig.sparqlTerms)
		elif (mig.ptype == "community"):
			return CommunityData(q, mig.sparqlData, mig.sparqlTerms)
		elif (mig.ptype == "thesis"):
			return ThesisData(q, mig.sparqlData, mig.sparqlTerms)
		elif (mig.ptype == "generic"):
			return GenericData(q, mig.sparqlData, mig.sparqlTerms)
		else:
			return None

if __name__ == "__main__":
	main()