class TripleStore(object):
	def __init__(self, sparqlData, sparqlTerms, sparqlResults):
		self.sparqlData = sparqlData
		self.sparqlTerms = sparqlTerms
		self.sparqlResults = sparqlResults