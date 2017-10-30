import os
from SPARQLWrapper import JSON
from rdflib import URIRef, Literal, Graph
import Transformation
import re

# ##  DATA TRANSPORT OBJECTS
# ##### Runs a query, sends data to get transformed, saves data to appropriate file



class TransformationFactory():
    @staticmethod
    def getTransformation(triple, objectType):
        function = re.sub(r'[0-9]+', '', triple['predicate']['value'].split('/')[-1].replace('#', '').replace('-', ''))
        if function == "accessRights":
            return Transformation().accessRights(triple, objectType)
        elif function == "modelsmemberOf":
            return Transformation().modelsmemberOf(triple, objectType)
        elif function == "modelshasMember":
            return Transformation().modelshasMember(triple, objectType)
        elif function == "language":
            return Transformation().language(triple, objectType)
        elif function == "type":
            return Transformation().type(triple, objectType)
        elif function == "rights":
            return Transformation().rights(triple, objectType)
        elif function == "license":
            return Transformation().license(triple, objectType)
        elif function == "ontologyinstitution":
            return Transformation().institution(triple, objectType)
        elif function == "available":
            return Transformation().available(triple, objectType)
        elif function == "aclvisibilityAfterEmbargo":
            return Transformation().aclvisibilityAfterEmbargo(triple, objectType)
        else:
            return [triple]


class Data(object):
    def __init__(self, query, group, sparqlData, sparqlTerms, queryObject):
        self.q = query
        self.prefixes = queryObject.prefixes
        self.group = group
        self.sparqlData = sparqlData
        self.sparqlTerms = sparqlTerms
        self.output = []
        self.graph = Graph()
        self.objectType = queryObject.objectType
        self.directory = "results/{0}/".format(self.objectType)
        self.filename = "results/{0}/{1}.nt".format(self.objectType, group)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def transformData(self):
        self.sparqlData.setReturnFormat(JSON)
        self.sparqlData.setQuery("{} {} {}".format(self.q['prefix'], self.q['construct'], self.q['where']))
        # queries a batch of resources from this particular "group"
        results = self.sparqlData.query().convert()['results']['bindings']
        # iterates over each resource and performs transformations
        for result in results:
            result = TransformationFactory().getTransformation(result, self.objectType)
            if isinstance(result, list):
                for triple in result:
                    s = URIRef(triple['subject']['value'])
                    p = URIRef(triple['predicate']['value'])
                    if triple['object']['type'] == 'uri':
                        if "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/" in triple['object']['type']:
                            triple['object']['type'] = triple['object']['type'].replace('http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')
                        o = URIRef(triple['object']['value'])
                    else:
                        o = Literal(triple['object']['value'])
                    self.graph.add((s, p, o))
        self.graph.serialize(destination=self.filename, format='nt')

    def resultsToTriplestore(self):
        headers = {'Content-Type': 'text/turtle'}
        requests.post(sparqlResults, data=self.graph.serialize(format='nt'), headers=headers)