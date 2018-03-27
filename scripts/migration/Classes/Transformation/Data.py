from Classes.Transformation import Transformation_Factory
from tools import PrintException
import os
from SPARQLWrapper import JSON
from rdflib import URIRef, Literal, Graph
import re
import concurrent.futures


class Data(object):
    """the data object performs a query passed into it from the main controller; it passes the results of the query to any necessary transformation methods (transformation class); 
    it then commits the transformed data to a local graph (an RDFLib object); 
    when all the results of a query have been transformed and committed to the local graph, the graph then has some transformations performed on it; 
    the local graph is the committed to a file in the results folder"""
    def __init__(self, group, queryObject, filesetIds, proxies, validator):
        self.proxies = proxies
        self.filesetIds = filesetIds
        self.query = queryObject.queries[group]  # the query for the group 
        self.prefixes = queryObject.prefixes  # the prefixes for this query
        self.group = group  # this group folder
        self.sparqlData = queryObject.sparqlData  # the migration origin
        self.sparqlTerms = queryObject.sparqlTerms  # the mapping origin
        self.results = {}  # 
        self.validator = validator #a list of all requried predicates for objectType
        self.graph = Graph()  # local graph stores the transformed results. final transformations are performed directly on the graph when context is required (if this then that)
        self.objectType = queryObject.objectType 
        self.directory = "results/{0}/".format(self.objectType)
        self.filename = "results/{0}/{1}.nt".format(self.objectType, group)
        if not os.path.exists(self.directory):  # if the directory doesn't exist, create it
            os.makedirs(self.directory)

    def transformData(self):
        self.sparqlData.setReturnFormat(JSON)
        # for each query in the query object, perform query and transform results
        # for binaries there are more than one query per group (2 x content/characterization, foxml/era1stats) so we loop over the self.query object
        for q in self.query:
            self.sparqlData.setQuery("{} {} {}".format(q['prefix'], q['construct'], q['where']))  # set the query
            try:
                results = self.sparqlData.query().convert()['results']['bindings']
            # iterate over each resource and performs transformations
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                    future_to_result = {executor.submit(parallelTransform, sparqlResult, self): sparqlResult for sparqlResult in results}
                    for future in concurrent.futures.as_completed(future_to_result):
                        future_to_result[future]
                        try:
                            future.result()
                        except Exception:
                            PrintException()
            except Exception:
                print (q)
                PrintException()
            self.__editVisibility()  # post-transformation transformation on visibility
            self.__editOwners()  # post-transformation transformation on ownership
            self.__addEbucore()  # checks for one or more date of ingest and converts to ebucore
            self.__writeGraphToFile()  # commit the local graph to a file (aka: 'the end')

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
        try:
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
        except Exception:
            print (s)
            PrintException()

    def __writeGraphToFile(self):
        if len(self.graph) > 0:
            with open('Audit/' + self.objectType + '_required_predicates_missing.txt', 'a') as file1, open('Audit/' + self.objectType + '_required_predicates_empty.txt', 'a') as file2:
                for s, o in self.graph.subject_objects(URIRef("info:fedora/fedora-system:def/model#hasModel")):
                    if s.split('/')[10] not in self.results:
                        self.results[s.split('/')[10]] = Graph()
                for r in self.results:
                    uri = 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/' + r[0:2] + "/" + r[2:4] + "/" + r[4:6] + "/" + r[6:8] + "/" + r
                    for s, p, o in self.graph.triples((None, None, None)):
                        if r in s:
                            self.results[r].add((s, p, o))
                    if self.objectType == "generic" and (None, URIRef("http://purl.org/dc/terms/created"), None) not in self.results[r]:
                        if (None, URIRef("http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#dateIngested"), None) in self.results[r]:
                            temp_date = self.results[r].value(URIRef(uri), URIRef("http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#dateIngested"))[0:4] 
                        elif (None, URIRef("http://fedora.info/definitions/v4/repository#created"), None) in self.results[r]:
                            temp_date = self.results[r].value(URIRef(uri), URIRef("http://fedora.info/definitions/v4/repository#created"))[0:4]
                        elif (None, URIRef("info:fedora/fedora-system:def/model#createdDate"), None) in self.results[r]:
                            temp_date = self.results[r].value(URIRef(uri), URIRef("info:fedora/fedora-system:def/model#createdDate"))[0:4]
                        print (uri, temp_date)
                        if temp_date:
                            self.results[r].add((URIRef(uri), URIRef("http://purl.org/dc/terms/created"), Literal(temp_date+ "-t")))
                            self.results[r].add((URIRef(uri), URIRef("http://terms.library.ualberta.ca/sortYear"), Literal(temp_date)))
                    elif self.objectType == "generic" and (None, URIRef("http://purl.org/dc/terms/created"), None) in self.results[r]:
                        if not self.results[r].value(URIRef(uri), URIRef("http://purl.org/dc/terms/created")):
                            self.results[r].remove((URIRef(uri), URIRef("http://purl.org/dc/terms/created"), None))
                            if (None, URIRef("http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#dateIngested"), None) in self.results[r]:
                                tmp_date = self.results[r].value(URIRef(uri), URIRef("http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#dateIngested"))[0:4]
                            elif (None, URIRef("http://fedora.info/definitions/v4/repository#created"), None) in self.results[r]:
                                tmp_date = self.results[r].value(URIRef(uri), URIRef("http://fedora.info/definitions/v4/repository#created"))[0:4]
                            elif (None, URIRef("info:fedora/fedora-system:def/model#createdDate"), None) in self.results[r]:
                                temp_date = self.results[r].value(URIRef(uri), URIRef("info:fedora/fedora-system:def/model#createdDate"))[0:4]
                            print (uri, tmp_date)
                            if tmp_date:
                                self.results[r].add((URIRef(uri), URIRef("http://purl.org/dc/terms/created"), Literal(tmp_date+ "-d")))
                                self.results[r].add((URIRef(uri), URIRef("http://terms.library.ualberta.ca/sortYear"), Literal(tmp_date)))                            
                    for v in self.validator: 
                    #self.validator have the results of all required predicates for the objectType
                        if (None, URIRef(v), None) in self.results[r]:
                            if not self.results[r].value(URIRef(uri), URIRef(v)):
                                file2.write("Predicate with no Value: " + "\t" + uri + "\t" + " | " + v + "\n")
                        else:
                            access = str(self.results[r].value(URIRef(uri), URIRef("http://purl.org/dc/terms/accessRights")))
                            file1.write ("Predicate is not in graph: " + "\t" + uri + "\t" + " | " + v + "\t" + access + "\n")
                            #file.write("Predicate is not in the object graph: " + "\t" + uri + "\t" + " | " + v + "\n")
                    self.filename = "results/{0}/{1}.nt".format(self.objectType, r)
                    self.results[r].serialize(destination=self.filename, format='nt')

def parallelTransform(result, queryObject):
    # for this set of results, perform a transformation
    result = Transformation_Factory.TransformationFactory().getTransformation(result, queryObject.objectType, queryObject.proxies)
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
                        try:
                            triple['object']['value'] = re.sub('filesetID', str(queryObject.filesetIds[triple['object']['value'].split('/')[10]]), str(triple['object']['value']))
                        except:
                            PrintException()
                    o = URIRef(triple['object']['value'])
                else:
                    o = Literal(triple['object']['value'])
                if triple['subject']['type'] == 'uri':
                    if "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/" in triple['subject']['value']:
                        triple['subject']['value'] = triple['subject']['value'].replace('http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')
                    if 'NOID' in triple['object']['value']:
                        triple['subject']['value'] = triple['subject']['value'].replace('NOID', triple['subject']['value'].split('/')[10])
                    if "filesetID" in triple['subject']['value']:
                        try:
                            triple['subject']['value'] = re.sub('filesetID', str(queryObject.filesetIds[triple['subject']['value'].split('/')[10]]), str(triple['subject']['value']))
                        except:
                            PrintException()
                    s = URIRef(triple['subject']['value'])
                else:
                    o = Literal(triple['subject']['value'])
                queryObject.graph.add((s, p, o))
            except:
                PrintException()