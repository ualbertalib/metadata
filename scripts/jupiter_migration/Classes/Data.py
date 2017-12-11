from Classes import Transformation
from utilities import PrintException
import os
from SPARQLWrapper import JSON
from rdflib import URIRef, Literal, Graph
from rdflib.namespace import RDF
import requests


class Data(object):
    def __init__(self, group, queryObject):
        self.query = queryObject.queries[group]
        self.prefixes = queryObject.prefixes
        self.group = group
        self.sparqlData = queryObject.sparqlData
        self.sparqlTerms = queryObject.sparqlTerms
        self.results = {}
        self.graph = Graph()
        self.objectType = queryObject.objectType
        self.directory = "results/{0}/".format(self.objectType)
        self.filename = "results/{0}/{1}.nt".format(self.objectType, group)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def transformData(self):
        self.sparqlData.setReturnFormat(JSON)
        for q in self.query:
            self.sparqlData.setQuery("{} {} {}".format(q['prefix'], q['construct'], q['where']))
            # queries a batch of resources from this particular "group"
            results = self.sparqlData.query().convert()['results']['bindings']
            # iterates over each resource and performs transformations
            for result in results:
                result = Transformation.TransformationFactory().getTransformation(result, self.objectType)
                if isinstance(result, list):
                    for triple in result:
                        p = URIRef(triple['predicate']['value'])
                        try:
                            if triple['object']['type'] == 'uri':
                                if "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/" in triple['object']['value']:
                                    triple['object']['value'] = triple['object']['value'].replace('http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')
                                if 'NOID' in triple['object']['value']:
                                    triple['object']['value'] = triple['object']['value'].replace('NOID', triple['object']['value'].split('/')[10])
                                o = URIRef(triple['object']['value'])
                            else:
                                o = Literal(triple['object']['value'])
                            if triple['subject']['type'] == 'uri':
                                if "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/" in triple['subject']['value']:
                                    triple['subject']['value'] = triple['subject']['value'].replace('http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')
                                if 'NOID' in triple['object']['value']:
                                    triple['subject']['value'] = triple['subject']['value'].replace('NOID', triple['subject']['value'].split('/')[10])
                                s = URIRef(triple['subject']['value'])
                            else:
                                o = Literal(triple['subject']['value'])
                            self.graph.add((s, p, o))
                        except:
                            PrintException()

        # ensures that "draft" is not superceded by a more liberal permission, but allows for coexistence of liberal permissions.
        if ('generic' in self.objectType) or ('thesis' in self.objectType):
            s_o = {}
            for s, o in self.graph.subject_objects(URIRef("http://purl.org/dc/terms/accessRights")):
                if s not in s_o:
                    s_o[s] = []
                    s_o[s].append(o)
                else:
                    s_o[s].append(o)
            for so in s_o:
                if URIRef('http://terms.library.ualberta.ca/embargo') in s_o[so]:
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/public')))
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/authenticated')))
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/draft')))
                elif URIRef('http://terms.library.ualberta.ca/draft') in s_o[so]:
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/public')))
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/authenticated')))
                elif URIRef('http://terms.library.ualberta.ca/authenticated') in s_o[so]:
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/public')))
        # checks to see if this particular query yielded any results
        if len(self.graph) > 0:
            for s, o in self.graph.subject_objects(URIRef("info:fedora/fedora-system:def/model#hasModel")):
                if s.split('/')[10] not in self.results:
                    self.results[s.split('/')[10]] = Graph()
            for r in self.results:
                for s, p, o in self.graph.triples((None, None, None)):
                    if r in s:
                        self.results[r].add((s, p, o))
                self.filename = "results/{0}/{1}.nt".format(self.objectType, r)
                self.results[r].serialize(destination=self.filename, format='nt')
        else:
            print('query failed to generate results')
