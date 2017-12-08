import random
from rdflib import URIRef, RDF, Literal


class URI_Generator(object):

	def __init__(self):
		self.proxyHash = {}
		self.fileSetTracker = []

	def generatefileSetId(self):
		fileSetId = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
		if fileSetId not in self.fileSetTracker:
			self.fileSetTracker.append(fileSetId)
			return fileSetId
		else:
			self.generatefileSetId()

	def generateProxyId(self, resource):
			proxyId = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
			if proxyId not in self.proxyHash:
				self.proxyHash[resource] = proxyId
				return proxyId
			else:
				self.generateProxyId(resource)

	def _addProxy(self, resource, fileSet):
		first = URIRef("http://www.iana.org/assignments/relation/first")
		last = URIRef("http://www.iana.org/assignments/relation/last")
		n = URIRef("http://www.iana.org/assignments/relation/next")
		p = URIRef("http://www.iana.org/assignments/relation/prev")
		if resource in self.proxyHash:
			otherProxy = "{}/proxy{}".format(resource, self.proxyHash[resource])
			proxyId = self.generateProxyId(resource)
			proxy = "{}/proxy{}".format(resource, proxyId)
			self._createProxy(resource, fileSet, proxy)
			self.graph.add((URIRef(resource), URIRef(first), URIRef(proxy)))
			self.graph.add((URIRef(resource), URIRef(last), URIRef(otherProxy)))
			self.graph.add((URIRef(proxy), URIRef(n), URIRef(otherProxy)))
			self.graph.add((URIRef(otherProxy), URIRef(p), URIRef(proxy)))
		else:
			proxyId = self.generateProxyId(resource)
			proxy = "{}/proxy{}".format(resource, proxyId)
			self._createProxy(resource, fileSet, proxy)

	def _createProxy(self, resource, fileSet, proxy):
		self.graph.add((URIRef(proxy), URIRef("http://www.openarchives.org/ore/terms/proxyIn"), URIRef(resource)))
		self.graph.add((URIRef(proxy), URIRef("http://www.openarchives.org/ore/terms/proxyFor"), URIRef(fileSet)))
		self.graph.add((URIRef(proxy), RDF.type, URIRef("http://fedora.info/definitions/v4/repository#Container")))
		self.graph.add((URIRef(proxy), RDF.type, URIRef("http://fedora.info/definitions/v4/repository#Resource")))
		self.graph.add((URIRef(proxy), RDF.type, URIRef("http://www.openarchives.org/ore/terms/Proxy")))
		self.graph.add((URIRef(proxy), RDF.type, URIRef("http://www.w3.org/ns/ldp#Container")))
		self.graph.add((URIRef(proxy), RDF.type, URIRef("http://www.w3.org/ns/ldp#RDFSource")))
		self.graph.add((URIRef(proxy), URIRef("info:fedora/fedora-system:def/model#hasModel"), Literal("ActiveFedora::Aggregation::Proxy")))
