from Classes.Transformation import Transformation_Factory
from tools import PrintException
import os
from SPARQLWrapper import JSON
from rdflib import URIRef, Literal, Graph
import re


class Data(object):
    """the data object performs a query passed into it from the main controller; it passes the results of the query to any necessary transformation methods (transformation class); 
    it then commits the transformed data to a local graph (an RDFLib object); 
    when all the results of a query have been transformed and committed to the local graph, the graph then has some transformations performed on it; 
    the local graph is the committed to a file in the results folder"""
    def __init__(self, group, queryObject):
        self.query = queryObject.queries[group]  # the query for the group 
        self.prefixes = queryObject.prefixes  # the prefixes for this query
        self.group = group  # this group folder
        self.sparqlData = queryObject.sparqlData  # the migration origin
        self.sparqlTerms = queryObject.sparqlTerms  # the mapping origin
        self.results = {}  # 
        self.graph = Graph()  # local graph stores the transformed results. final transformations are performed directly on the graph when context is required (if this then that)
        self.objectType = queryObject.objectType 
        self.directory = "results/{0}/".format(self.objectType)
        self.filename = "results/{0}/{1}.nt".format(self.objectType, group)
        if not os.path.exists(self.directory):  # if the directory doesn't exist, create it
            os.makedirs(self.directory)

    def transformData(self, uri_generator):
        self.sparqlData.setReturnFormat(JSON)
        # for each query in the query object, perform query and transform results
        for q in self.query:
            self.sparqlData.setQuery("{} {} {}".format(q['prefix'], q['construct'], q['where'])) # set the query
            results = self.sparqlData.query().convert()['results']['bindings']
            # iterate over each resource and performs transformations
            for result in results:
                # for this set of results, perform a transformation
                result = Transformation_Factory.TransformationFactory().getTransformation(result, self.objectType, uri_generator)
                # test to see if the post-transformation result is actually a triple (just a QA test)
                if isinstance(result, list):
                    # a transformation can return more than one triple (status and dctype, for example)
                    for triple in result:
                        p = URIRef(triple['predicate']['value'])
                        try:
                            # adding triple to the local graph, depends on uri or literal
                            if triple['object']['type'] == 'uri':
                                # substitute NOID for an actual noid, fileSetId for an actual ID, and replace gillingham with UAT anywhere that we might have failed to do so in the query
                                if "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/" in triple['object']['value']:
                                    triple['object']['value'] = triple['object']['value'].replace('http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')
                                if 'NOID' in triple['object']['value']:
                                    triple['object']['value'] = triple['object']['value'].replace('NOID', triple['object']['value'].split('/')[10])
                                if "filesetID" in triple['object']['value']:
                                    triple['object']['value'] = re.sub('filesetID', uri_generator.generatefileSetId("{}{}".format(triple['object']['value'].split('/')[10], triple['object']['value'].split('/')[11])), triple['object']['value'])
                                o = URIRef(triple['object']['value'])
                            else:
                                o = Literal(triple['object']['value'])
                            if triple['subject']['type'] == 'uri':
                                if "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/" in triple['subject']['value']:
                                    triple['subject']['value'] = triple['subject']['value'].replace('http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')
                                if 'NOID' in triple['object']['value']:
                                    triple['subject']['value'] = triple['subject']['value'].replace('NOID', triple['subject']['value'].split('/')[10])
                                if "filesetID" in triple['subject']['value']:
                                    triple['subject']['value'] = re.sub('filesetID', uri_generator.generatefileSetId("{}{}".format(triple['subject']['value'].split('/')[10], triple['subject']['value'].split('/')[11])), triple['subject']['value'])
                                s = URIRef(triple['subject']['value'])
                            else:
                                o = Literal(triple['subject']['value'])
                            self.graph.add((s, p, o))
                        except:
                            PrintException()
            self.__editVisibility() # post-transformation transformation on visibility
            self.__editOwners() # post-transformation transformation on ownership
            self.__addEbucore() # checks for one or more date of ingest and converts to ebucore
            self.__writeGraphToFile() # commit the local graph to a file (aka: 'the end')

    def __editVisibility(self):
        # ensures that "draft" is not superceded by a more liberal permission, but allows for coexistence of liberal permissions.
        if ('generic' in self.objectType) or ('thesis' in self.objectType) or ('collection' in self.objectType) or ('community' in self.objectType):
            # temporarily stores all contents of the predicate in a dictionary, making it easier to know what is or is not in a graph
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
           #for s, p, o in self.graph.triples((None, URIRef("http://purl.org/dc/terms/accessRights"), None)):
            #   print(s, p, o)

    def __editOwners(self):
        s_o = {}
        for s, o in self.graph.subject_objects(URIRef("http://purl.org/ontology/bibo/owner")):
            if s not in s_o:
                s_o[s] = []
                s_o[s].append(o)
            else:
                s_o[s].append(o)
        for so in s_o:
            if (len(s_o[so]) == 2) and URIRef("eraadmi@ualberta.ca") in s_o[so]:
                self.graph.remove((URIRef(so), URIRef("http://purl.org/ontology/bibo/owner"), URIRef("eraadmi@ualberta.ca")))
            if (len(s_o[so]) > 2) and URIRef("eraadmi@ualberta.ca") in s_o[so]:
                self.graph.remove((URIRef(so), URIRef("http://purl.org/ontology/bibo/owner"), URIRef("eraadmi@ualberta.ca")))
            if (len(s_o[so]) > 1) and URIRef("eraadmi@ualberta.ca") not in s_o[so]:
                pass
                # do someting else to remaining owners

    def __addEbucore(self):
        if (None, URIRef("info:fedora/fedora-system:def/model#createdDate"), None) in self.graph:
            for s, o in self.graph.subject_objects(URIRef("info:fedora/fedora-system:def/model#createdDate")):
                self.graph.add((s, URIRef("http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#dateIngested"), o))
                self.graph.remove((s, URIRef("info:fedora/fedora-system:def/model#createdDate"), o))
                if (s, URIRef("http://fedora.info/definitions/v4/repository#created"), None) in self.graph:
                    self.graph.remove((s, URIRef("http://fedora.info/definitions/v4/repository#created"), None))
        elif (None, URIRef("http://fedora.info/definitions/v4/repository#created"), None) in self.graph:
            for s, o in self.graph.subject_objects(URIRef("http://fedora.info/definitions/v4/repository#created")):
                self.graph.add((s, URIRef("http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#dateIngested"), o))
                self.graph.remove((s, URIRef("http://fedora.info/definitions/v4/repository#created"), o))

    def __writeGraphToFile(self):
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