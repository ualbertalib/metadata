from config import types, dates, sparqlTerms, sparqlData, sparqlResults, mig_ns, vocabs
from utilities import PrintException, cleanOutputs
import concurrent.futures
import time
from datetime import datetime, date
import os
from SPARQLWrapper import JSON, SPARQLWrapper
from rdflib import URIRef, Literal, Graph, Namespace
from rdflib.namespace import RDF
import re
import json
import requests
import random
import nltk
#nltk.download('punkt')
from nltk import word_tokenize
proxyHash = {}
fileSetTracker = []

def main():
    """ main controller: iterates over each object type (generic item metadata, thesis item metadata, and binary-level metadata), 
    creates a set of subqueries for each of these types, then cues threads to run each of these subqueries as a job. The migration outout is saved to
    the results folder and to a triplestore. The subqueries are cached in the cache folder. Custom settings can be modified in config.py."""
    ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print('cleaning the cache')
    cleanOutputs(sparqlResults)
    # Iterate over every type of object that needs to be migrated.
    # This is the first splitting of the data for migration.
    # a queryObject has been split into multiple groups
    # only one group exists for community, and one for collection objects
    # approximately a thousand queries each are minted for thesis and for generic objects
    # these queries are based on the first folder in the fedora pair tree
    # a queryObject knows its type
    # a cache of queries is recorded, results are sent to a "results" triplestore, and results are stored as n-triples
    for objectType in types:
        queryObject = QueryFactory.getMigrationQuery(objectType, sparqlData)
        queryObject.generateQueries()
        print('{0} queries generated'.format(objectType))
        print('{0} queries of {1} objects to be transformed'.format(len(queryObject.queries), objectType))
        i = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_result = {executor.submit(parellelTransform, queryObject, group): group for group in queryObject.queries.keys()}
            for future in concurrent.futures.as_completed(future_to_result):
                future_to_result[future]
                try:
                    i = i + 1
                    future.result()
                    print("{0} of {1} {2} queries transformed".format(i, len(queryObject.queries), objectType))
                except Exception:
                    PrintException()
        print("{0} objects transformation completed".format(objectType))
        del queryObject
    tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))


def parellelTransform(queryObject, group):
    DTO = Data(queryObject.queries[group], group, queryObject.sparqlData, sparqlTerms, queryObject)  # query, group, object
    DTO.transformData()
    # DTO.resultsToTriplestore()

def generatefileSetId():
    fileSetId = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
    if fileSetId not in fileSetTracker:
        fileSetTracker.append(fileSetId)
        return fileSetId
    else:
        generatefileSetId()

def generateProxyId(resource):
        proxyId = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
        if proxyId not in proxyHash:
            proxyHash[resource] = proxyId
            return proxyId
        else:
            generateProxyId(resource)

class TransformationFactory():
    @staticmethod
    def getTransformation(triple, objectType):
        function = re.sub(r'[0-9]+', '', triple['predicate']['value'].split('/')[-1].replace('#', '').replace('-', ''))
        for subjects in dates:
            if (subjects['subject'] in triple['subject']['value']) and (function == "created"):
                return Transformation().createdDate(subjects, triple, objectType)
            if (subjects['subject'] in triple['subject']['value']) and (function == "graduationdate"):
                return Transformation().gradDate(subjects, triple, objectType)
        if function == "created":
            return Transformation().sortYear(triple, objectType)
        if function == "graduationdate":
            return Transformation().sortYear(triple, objectType)
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
        elif function == "subject":
            return Transformation().subject(triple, objectType)
        elif function == "license":
            return Transformation().license(triple, objectType)
        elif function == "ontologyinstitution":
            return Transformation().institution(triple, objectType)
        elif function == "available":
            return Transformation().available(triple, objectType)
        elif function == "aclvisibilityAfterEmbargo":
            return Transformation().aclvisibilityAfterEmbargo(triple, objectType)
        elif function == "owner":
            return Transformation().owner(triple, objectType)            
        else:
            return [triple]


class QueryFactory():
    @staticmethod
    def getMigrationQuery(objectType, sparqlData):
        """ returns a specified query object depending on the type passed in"""
        if objectType == "collection":
            return Collection(sparqlData)
        elif objectType == "community":
            return Community(sparqlData)
        elif objectType == "thesis":
            return Thesis(sparqlData)
        elif objectType == "generic":
            return Generic(sparqlData)
        elif objectType == "technical":
            return Technical(sparqlData)
        elif objectType == "relatedObject":
            return Related_Object(sparqlData)
        else:
            return None


class Data(object):
    def __init__(self, query, group, sparqlData, sparqlTerms, queryObject):
        self.query = query
        self.prefixes = queryObject.prefixes
        self.group = group
        self.sparqlData = sparqlData
        self.sparqlTerms = sparqlTerms
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
                result = TransformationFactory().getTransformation(result, self.objectType)
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

        # ensures that "private" is not superceded by a more liberal permission, but allows for coexistence of liberal permissions.
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
                    print(URIRef(so), 'should be embargo')
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/public')))
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/authenticated')))
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/draft')))
                elif URIRef('http://terms.library.ualberta.ca/draft') in s_o[so]:
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/public')))
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/authenticated')))
                elif URIRef('http://terms.library.ualberta.ca/authenticated') in s_o[so]:
                    self.graph.remove((URIRef(so), URIRef("http://purl.org/dc/terms/accessRights"), URIRef('http://terms.library.ualberta.ca/public')))
        #checks to see if this particular query yielded any results
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


    def _addProxy(self, resource, fileSet):
        first = URIRef("http://www.iana.org/assignments/relation/first")
        last = URIRef("http://www.iana.org/assignments/relation/last")
        n = URIRef("http://www.iana.org/assignments/relation/next")
        p = URIRef("http://www.iana.org/assignments/relation/prev")
        if resource in proxyHash:
            otherProxy = "{}/proxy{}".format(resource, proxyHash[resource])
            proxyId = generateProxyId(resource)
            proxy = "{}/proxy{}".format(resource, proxyId)
            self._createProxy(resource, fileSet, proxy)
            self.graph.add((URIRef(resource), URIRef(first), URIRef(proxy)))
            self.graph.add((URIRef(resource), URIRef(last), URIRef(otherProxy)))
            self.graph.add((URIRef(proxy), URIRef(n), URIRef(otherProxy)))
            self.graph.add((URIRef(otherProxy), URIRef(p), URIRef(proxy)))
        else:
            proxyId = generateProxyId(resource)
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

    def resultsToTriplestore(self):
        headers = {'Content-Type': 'text/turtle'}
        requests.post(sparqlResults, data=self.graph.serialize(format='nt'), headers=headers)


class DateFinder:
    def __init__(self, tokens):
        self.word = tokens
        self.out = []
        self.output = [""]
        
    def getyear(self):
        # find all years with a 4 digit format (between 1900 and 2018)
        self.year = [i for i, w in enumerate(self.word) if re.search('^\d{4}$', w)]
        #print (self.year)
        for n,year in enumerate(self.year):
            self.out.append({'year': '', "grams": {"1-gram": "", "-1-gram": "", "2-gram": "", "-2-gram": "", "3-gram": "", "-3-gram": "", "4-gram": "", "-4-gram": "", "5-gram": "", "-5-gram": ""}})
            if int(self.word[year]) > 1900 and int(self.word[year]) < 2018:
                #index = self.word.index(year)
                self.out[n]["year"] = self.word[year]
                for j in range(1, 6):
                    # preceding grams
                    if j + year < len(self.word): 
                        self.out[n]["grams"][str(j) + "-gram"] = self.word[year + j] 
                    #succeeding grams 
                    if year - j > 0:
                        self.out[n]["grams"]["-" + str(j) + "-gram"] = self.word[year - j]
                self.output = self.out 
        if self.output[0] != '':
            return self.output
        else: 
            return None
    
    def getymonth(self):
        # find all dates with yyyy-./:mm format
        self.ymonth = [w for w in self.word if re.search('^\d{4}?[-/.//://\/]\d{2}$', w)]
        for i in self.ymonth:
            for j in ["-", ":", "/", "."]:
                if j in i:
                    self.year = ""
                    self.month = ""
                    self.year = i.split(str(j))[0]
                    self.month = i.split(str(j))[1]
                if self.year in range (1900, 2019) and self.month in range (1, 13):
                    self.output[0] = self.month + "/" + self.year
        if self.output[0] != '':
            return self.output
        else:
            return None
    
    def getyday(self):
        self.yday = [w for w in self.word if re.search('^\d{4}?[-/.//://\/]\d{2}?[/.//:/-/\/]\d{2}$', w)]
        for i in self.yday:
            for j in ["-", ":", "/", "."]:
                if j in i:
                    self.year = ""
                    self.month = ""
                    self.day = ""
                    self.year = i.split(str(j))[0]
                    self.month = i.split(str(j))[1]
                    self.day = i.split(str(j))[2]
                if self.year in range (1900, 2019) and self.month in range (1, 13) and slef.day in range (1, 32):
                    self.output[0] = self.day + "/" + self.month + "/" + self.year
        if self.output[0] != '':
            return self.output
        else:
            return None  

class Query(object):
    """ Query objects are dynamically generated, and contain SPARQL CONSTRUCT queries with input from the jupiter application profile """
    def __init__(self, objectType, sparqlData, sparqlTerms=sparqlTerms):
        self.mapping = []
        self.sparqlTerms = SPARQLWrapper(sparqlTerms)  # doesn't need to change (the terms store doesn't change)
        self.sparqlData = SPARQLWrapper(sparqlData)  # sets the triple store from which to get data (simple, test, or dev)
        self.sparqlTerms.setMethod("POST")
        self.sparqlData.setMethod("POST")
        self.queries = {}
        self.splitBy = {}
        self.prefixes = ""
        self.filename = ""
        for ns in mig_ns:
            self.prefixes = self.prefixes + " PREFIX {0}: <{1}> ".format(ns['prefix'], ns['uri'])
        self.getMappings()

    def generateQueries(self):
        pass

    def getMappings(self):
        if (self.objectType == 'collection') or (self.objectType == 'community') or (self.objectType == 'generic') or (self.objectType == 'thesis'):
            query = """prefix ual: <http://terms.library.ualberta.ca/> SELECT * WHERE {{ GRAPH ual:{0} {{?newProperty ual:backwardCompatibleWith ?oldProperty}} }}""".format(self.objectType)
            self.sparqlTerms.setReturnFormat(JSON)
            self.sparqlTerms.setQuery(query)
            results = self.sparqlTerms.query().convert()
            for result in results['results']['bindings']:
                self.mapping.append((result['newProperty']['value'], result['oldProperty']['value']))
        else:
            pass

    def getSplitBy(self):
        # base query only needs 3 prefixes appended to the "select" statement defined by the object
        query = "prefix ualids: <http://terms.library.ualberta.ca/identifiers/> prefix fedora: <http://fedora.info/definitions/v4/repository#> prefix ldp: <http://www.w3.org/ns/ldp#> prefix dcterm: <http://purl.org/dc/terms/> prefix info: <info:fedora/fedora-system:def/model#> prefix ual: <http://terms.library.ualberta.ca/> {0}".format(self.select).replace('\n', '')
        self.sparqlData.setReturnFormat(JSON)
        self.sparqlData.setQuery(query)
        results = self.sparqlData.query().convert()
        # iterate over query results
        for result in results['results']['bindings']:
            # the group is the two folders at the base of the pair tree, concatenated by an underscore
            group = result['resource']['value'].split('/')[6]
            # assign that parameter by which you want to search to that group
            self.splitBy[group] = "/".join(result['resource']['value'].split('/')[:7])  # the stem of the resource [0] and the group number by which to save [1] (this is the first digit in the pair tree)

    def postResults(self):
        directory = 'results/{0}'.format(self.objectType)
        for (dirpath, dirnames, filenames) in os.walk(directory):
            for filename in filenames:
                with open(os.path.join(dirpath, filename), 'rb') as f:
                    query = "INSERT DATA {{0}}".format(f.read())
                    self.sparqlResults.setReturnFormat(JSON)
                    self.sparqlResults.setQuery(query)
                    self.sparqlResults.query()

    def writeQueries(self):
        for group in self.queries:
            for num, query in enumerate(self.queries[group]):
                self.queries[group][num]['construct'] = ' '.join(self.queries[group][num]['construct'].replace('\n', ' ').split())
                self.queries[group][num]['where'] = ' '.join(self.queries[group][num]['where'].replace('\n', ' ').split())
        filename = "cache/{0}.json".format(self.objectType)
        with open(filename, 'w+') as f:
            json.dump([self.queries], f, sort_keys=True, indent=4, separators=(',', ': '))


class Collection(Query):
    def __init__(self, sparqlData):
        self.objectType = 'collection'
        self.construct = """CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            rdf:type pcdm:Collection ; ual:hydraNoid ?noid; dcterm:accessRights ?visibility"""
        self.where = ["""WHERE {
            ?resource info:hasModel 'Collection'^^xsd:string .
            OPTIONAL {
                ?resource ualids:is_community 'false'^^xsd:boolean
            } .
            OPTIONAL {
                ?resource ualid:is_community 'false'^^xsd:boolean
            } .
            OPTIONAL {
                ?resource ual:is_community 'false'^^xsd:boolean
            }"""]
        self.select = None
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.queries['collection'] = []
        self.queries['collection'].append({})
        for where in self.where:
            construct = self.construct
            for pair in self.mapping:
                construct = "{0} ; <{1}> ?{2} ".format(construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " {0} . OPTIONAL {{ ?resource <{1}> ?{2} . FILTER (str(?{3})!='') }}".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries['collection'][0]['prefix'] = self.prefixes
            self.queries['collection'][0]['construct'] = construct + "}"
            self.queries['collection'][0]['where'] = """{} . OPTIONAL {{ ?permission webacl:accessTo ?resource ; webacl:mode webacl:Read ; webacl:agent ?visibility }} . BIND(STR(replace(replace(STR(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', '',''), '^.+/', '')) AS ?noid) . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)}}""".format(where)
        self.writeQueries()


class Community(Query):
    def __init__(self, sparqlData):
        self.objectType = 'community'
        self.construct = """CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            rdf:type pcdm:Object; rdf:type ual:Community; ual:hydraNoid ?noid; dcterm:accessRights ?visibility"""
        self.where = ["""WHERE { ?resource info:hasModel 'Collection'^^xsd:string ;
            OPTIONAL { ?resource ualids:is_community 'true'^^xsd:boolean } .
            OPTIONAL { ?resource ualid:is_community 'true'^^xsd:boolean } .
            OPTIONAL { ?resource ual:is_community 'true'^^xsd:boolean }"""]
        self.select = None
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.queries['community'] = []
        self.queries['community'].append({})
        for where in self.where:
            construct = self.construct
            for pair in self.mapping:
                construct = "{0} ; <{1}> ?{2} ".format(construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " {0} . OPTIONAL {{ ?resource <{1}> ?{2} . FILTER (str(?{3})!='') }}".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries['community'][0]['prefix'] = self.prefixes
            self.queries['community'][0]['construct'] = construct + "}"
            self.queries['community'][0]['where'] = """{} . OPTIONAL {{ ?permission webacl:accessTo ?resource ; webacl:mode webacl:Read ; webacl:agent ?visibility }} . BIND(STR(replace(replace(STR(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', '',''), '^.+/', '')) AS ?noid) . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource) . }}""".format(where)
        self.writeQueries()


class Generic(Query):
    def __init__(self, sparqlData):
        self.objectType = 'generic'
        # custom construct clause to capture unmapped triples
        self.construct = """CONSTRUCT {
            ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            dcterm:available ?available ;
            dcterm:accessRights ?visibility ;
            rdf:type works:Work;
            rdf:type pcdm:Object ;
            bibo:owner ?owner ;
            acl:embargoHistory ?history ;
            acl:visibilityAfterEmbargo ?visAfter ;
            ual:hydraNoid ?noid"""
        self.where = []
        self.select = """SELECT distinct ?resource WHERE {
            ?resource info:hasModel 'GenericFile'^^xsd:string ;
            dcterm:type ?type . FILTER(str(?type) != 'Thesis'^^xsd:string) .
            FILTER (NOT EXISTS {{?resource ualids:remote_resource 'dataverse'^^xsd:string}})
        }"""
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = []
            self.queries[group].append({})
            # synthesize a query that fetches a subgroup of resources and constructs a transformed graph from this subgroup
            where = """WHERE {{
                ?resource info:hasModel 'GenericFile'^^xsd:string ;
                dcterm:type ?type . filter(str(?type) != 'Thesis'^^xsd:string) .
                FILTER (contains(str(?resource), '{}')) .
                FILTER (NOT EXISTS {{?resource ualids:remote_resource 'Dataverse'^^xsd:string}})""".format(self.splitBy[group])
            construct = self.construct
            for pair in self.mapping:
                construct = "{0} ; <{1}> ?{2} ".format(construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                if ("http://purl.org/dc/terms/created" in pair[1]) or ("http://terms.library.ualberta.ca/date/graduationdate" in pair[1]):
                    where = """ {0} .
                                OPTIONAL {{
                                    ?resource <{1}> ?{2} .
                                }}""".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                else:
                    where = """ {0} .
                                OPTIONAL {{
                                    ?resource <{1}> ?{2} .
                                    FILTER (str(?{3})!='')
                                }}""".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))                
            # customize the where clause to include triples that aren't in the mappings
            self.queries[group][0]['prefix'] = self.prefixes
            self.queries[group][0]['construct'] = construct + " }"
            self.queries[group][0]['where'] = """{} .
                OPTIONAL {{ ?ownership webacl:accessTo ?resource ;
                    webacl:mode webacl:Write ;
                    webacl:agent ?owner }} .
                OPTIONAL {{ ?permission webacl:accessTo ?resource ;
                    webacl:mode webacl:Read ;
                    webacl:agent ?visibility }} .
                OPTIONAL {{ ?resource acl:hasEmbargo ?embargo .
                    OPTIONAL {{ ?embargo acl:embargoReleaseDate ?available }} .
                    OPTIONAL {{ ?embargo acl:embargoHistory ?history }} .
                    OPTIONAL {{ ?embargo acl:visibilityAfterEmbargo ?visAfter }}
                }} .
                BIND(STR(replace(replace(STR(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', '',''), '^.+/', '')) AS ?noid) .
                BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)
            }}""".format(where)
        self.writeQueries()


class Thesis(Query):
    def __init__(self, sparqlData):
        self.objectType = 'thesis'
        self.construct = """CONSTRUCT {
            ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            dcterm:available ?available ;
            dcterm:accessRights ?accessRights;
            rdf:type works:Work ;
            rdf:type pcdm:Object ;
            rdf:type bibo:Thesis; bibo:owner ?owner ;
            acl:embargoHistory ?history ;
            acl:visibilityAfterEmbargo ?visAfter ;
            ual:hydraNoid ?noid"""
        self.where = []
        self.select = """SELECT distinct ?resource WHERE {
            ?resource info:hasModel 'GenericFile'^^xsd:string ;
            dcterm:type 'Thesis'^^xsd:string
        }"""
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = []
            self.queries[group].append({})
            where = """WHERE {{ ?resource info:hasModel 'GenericFile'^^xsd:string ;
                dcterm:type 'Thesis'^^xsd:string .
                FILTER (contains(str(?resource), '{0}'))""".format(self.splitBy[group])
            construct = self.construct
            for pair in self.mapping:
                construct = "{0} ; <{1}> ?{2}".format(construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                if ("http://purl.org/dc/terms/created" in pair[1]) or ("http://terms.library.ualberta.ca/date/graduationdate" in pair[1]):
                    where = " {0} . OPTIONAL {{ ?resource <{1}> ?{2} }} ".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                else:
                    where = " {0} . OPTIONAL {{ ?resource <{1}> ?{2} . FILTER (str(?{3})!='') }} ".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries[group][0]['prefix'] = self.prefixes
            self.queries[group][0]['construct'] = construct + " }"
            self.queries[group][0]['where'] = """{} .
                OPTIONAL {{
                    ?ownership webacl:accessTo ?resource ;
                    webacl:mode webacl:Write ;
                    webacl:agent ?owner .
                }} .
                OPTIONAL {{
                    ?permission webacl:accessTo ?resource ;
                    webacl:mode webacl:Read ;
                    webacl:agent ?accessRights .
                }} .
                OPTIONAL {{
                    ?resource acl:hasEmbargo ?embargo .
                    OPTIONAL {{ ?embargo acl:embargoReleaseDate ?available }} .
                    OPTIONAL {{ ?embargo acl:embargoHistory ?history }} .
                    OPTIONAL {{ ?embargo acl:visibilityAfterEmbargo ?visAfter }} .
                    OPTIONAL {{ ?embargo acl:visibilityDuringEmbargo ?accessRights }} .
                }} .
                BIND(STR(replace(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', '',''), '^.+/', '')) AS ?noid) .
                BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource) .
            }}""".format(where)
        self.writeQueries()


class Technical(Query):
    """ direct members: content and characterization"""
    def __init__(self, sparqlData):
        self.objectType = 'technical'
        # custom construct clause to capture unmapped triples
        self.construct = """CONSTRUCT {
            ?jupiterResource pcdm:hasMember ?jupiterDirectFileset .
            ?jupiterDirectFileset info:hasModel 'IRFileSet' ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:Object ;
            rdf:type works:FileSet ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            pcdm:hasFile ?jupiterDirectFile ;
            pcdm:memberOf ?jupiterResource ;
            fedora:hasParent ?jupiterResource ;
            ldp:contains ?jupiterDirectFiles ;
            ldp:membershipResource ?jupiterDirectFiles .
            ?jupiterDirectFiles info:hasModel 'ActiveFedora::DirectContainer' ;
            fedora:hasParent ?jupiterDirectFileset ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type ldp:DirectContainer ;
            rdf:type ldp:RDFSource ;
            fedora:created ?fedoraCreated ;
            fedora:lastModified ?fedoraLastModified ;
            fedora:createdBy ?fedoraCreatedBy ;
            fedora:lastModifiedBy ?fedoraLastModifiedBy ;
            fedora:writable ?directFedoraWritable ;
            ldp:hasMemberRelation pcdm:hasFile ;
            ldp:contains ?jupiterDirectFile .
            ?jupiterDirectFile info:hasModel 'File' ;
            rdf:type ldp:NonRDFSource ;
            rdf:type fedora:Binary ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:File ;
            rdf:type use:OriginalFile ;
            rdf:type pcdm:File ;
            pcdm:fileOf ?jupiterDirectFileset ;
            iana:describedby ?jupiterDirectFileFCR ;
            fedora:hasParent ?jupiterDirectFiles ;
            fedora:hasFixityService ?directFileFixity ;
            ebucore:filename ?directOriginalName ;
            ebucore:hasMimeType ?directMimeType ;
            premis:hasMessageDigest ?directFedoraDigest ;
            premis:hasSize ?directSize ;
            fedora:created ?fedoraCreated ;
            fedora:lastModified ?fedoraLastModified ;
            fedora:createdBy ?fedoraCreatedBy ;
            fedora:lastModifiedBy ?fedoraLastModifiedBy ;
            fedora:writable ?directFedoraWritable ;
            rdf:type ?directRdfType ;
            fedora:mixinTypes ?directFileMixins .
            ?jupiterDirectFileFCR iana:describes ?jupiterDirectFile ;
            fedora:hasVersions ?directFileVersions ;
            fedora:uuid ?directFileFCRUUID ;
            fedora:mixinTypes ?directFileFCRMixins ;
            fedora:primaryType ?directFileFCRPrimaryType ;
            fedora:created ?directFedoraCreated ;
            fedora:lastModified ?directFedoraLastModified ;
            fedora:createdBy ?directFedoraCreatedBy ;
            fedora:lastModifiedBy ?directFedoraLastModifiedBy ;
            fedora:writable ?directFedoraWritable .
            ?proxy ore:proxyIn ?jupiterResource ;
            ore:proxyFor ?jupiterDirectFileset ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type ore:Proxy ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            info:hasModel 'ActiveFedora::Aggregation::Proxy' ;
            iana:next ?proxy;
            iana:prev ?proxy .
            ?jupiterResource iana:first ?proxy ;
            iana:last ?proxy ."""
        self.select = """SELECT distinct ?resource WHERE {
            ?resource rdf:type fedora:Binary .
        }"""
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = []
            filesetId = generatefileSetId()
            proxyId = generateProxyId(random.choice('0123456789ABCDEF') for i in range(16))
            for fileType in ['content', 'characterization']:
                self.queries[group].append({})
                # synthesize a query that fetches a subgroup of resources and constructs a transformed graph from this subgroup
                where = """WHERE {{
                    ?directMember rdf:type fedora:Binary .
                    FILTER (STRSTARTS(str(?directMember), '{}')) .
                    FILTER (STRENDS(str(?directMember), '{}'))""".format(self.splitBy[group], fileType)
                # customize the where clause to include triples that aren't in the mappings
                self.queries[group][-1]['prefix'] = self.prefixes
                self.queries[group][-1]['construct'] = self.construct + " }"
                self.queries[group][-1]['where'] = """{} .
                        OPTIONAL {{ ?directMember fedora:created ?directFedoraCreated . FILTER (str(?directFedoraCreated) != '') }} .
                        OPTIONAL {{ ?directMember fedora:createdBy ?directFedoraCreatedBy . FILTER (str(?irectFedoraCreatedBy) != '')}} .
                        OPTIONAL {{ ?directMember fedora:lastModified ?directFedoraLastModified . FILTER (str(?directFedoraModified) != '')}} .
                        OPTIONAL {{ ?directMember fedora:lastModifiedBy ?directFedoraLastModifiedBy . FILTER (str(?directFedoraModifiedBy) != '')}} .
                        OPTIONAL {{ ?directMember fedora:writable ?directFedoraWritable . FILTER (str(?directFedoraWritable) != '')}} .
                        OPTIONAL {{ ?directMember fedora:uuid ?directFedoraUUID . FILTER (str(?directFedoraUUID) != '')}} .
                        OPTIONAL {{ ?directMember fedora:digest ?directFedoraDigest . FILTER (str(?directFedoraDigest) != '')}} .
                        OPTIONAL {{ ?directMember rdf:type ?directRdfType . FILTER (str(?directRdfType) != '')}} .
                        OPTIONAL {{ ?directMember premis:hasSize ?directSize . FILTER (str(?directSize) != '')}} .
                        OPTIONAL {{ ?directMember premis:hasOriginalName ?directOriginalName . FILTER (str(?directOriginalName) != '')}} .
                        OPTIONAL {{ ?directMember fedora:mimeType ?directMimeType . FILTER (str(?directMimeType) != '')}} .
                        OPTIONAL {{ ?directMember fedora:mixinTypes ?directFileMixins . FILTER (str(?directFileMixins) != '')}} .
                        BIND(STR(replace(replace(replace(str(?directMember), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', ''),'/{}',''), '^.+/', '')) AS ?noid) .
                        BIND(URI(replace(replace(str(?directMember), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/'), '{}', '{}')) AS ?jupiterDirectFileset)
                        BIND(URI(CONCAT(STR(?jupiterDirectFileset), '/files')) AS ?jupiterDirectFiles) .
                        BIND(URI(CONCAT(STR(?jupiterDirectFiles), CONCAT('/', ?noid))) AS ?jupiterDirectFile) .
                        BIND(URI(CONCAT(STR(?directMember), '/fcr:metadata')) AS ?directFileFCR) .
                        BIND(URI(CONCAT(STR(?jupiterDirectFile), '/fcr:metadata')) AS ?jupiterDirectFileFCR) .
                        BIND(URI(CONCAT(STR(?directFile), '/fcr:fixity')) AS ?directFileFixity) .
                        BIND(URI(CONCAT(STR(?directFile), '/fcr:versions')) AS ?directFileVersions) .
                        OPTIONAL {{ ?directFileFCR rdf:type ?directFileFCRRDFType . FILTER (str(?directFileFCRRDFType) != '')}} .
                        OPTIONAL {{ ?directFileFCR fedora:uuid ?directFileFCRUUID . FILTER (str(?directFileFCRUUID) != '')}} .
                        OPTIONAL {{ ?directFileFCR fedora:mixinTypes ?directFileFCRMixins . FILTER (str(?directFileFCRMixins) != '')}} .
                        OPTIONAL {{ ?directFileFCR fedora:primaryType ?directFileFCRPrimaryType . FILTER (str(?directFileFCRPrimaryType) != '')}} .
                        BIND(URI(replace(str(?jupiterDirectFileset), '/{}', '')) AS ?jupiterResource) .
                        BIND(URI(CONCAT(str(?jupiterResource), '/proxy{}')) AS ?proxy) .
                    }}""".format(where, fileType, fileType, filesetId, filesetId, proxyId)
            self.writeQueries()


class Related_Object(Query):
    """ related members: content and characterization"""
    def __init__(self, sparqlData):
        self.objectType = 'relatedObject'
        # custom construct clause to capture unmapped triples
        self.construct = """CONSTRUCT {
            ?jupiterResource pcdm:hasRelatedObject ?jupiterRelatedObject .
            ?jupiterRelatedObject info:hasModel 'IRItem' ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:Object ;
            rdf:type works:Work ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            fedora:created ?relatedFedoraCreated ;
            fedora:lastModified ?relatedFedoraLastModified ;
            fedora:createdBy ?relatedFedoraCreatedBy ;
            fedora:lastModifiedBy ?relatedFedoraLastModifiedBy ;
            fedora:writable ?relatedFedoraWritable ;
            pcdm:hasMember ?relatedFileset ;
            pcdm:relatedObjectOf ?jupiterResource ;
            fedora:hasParent ?jupiterResource ;
            ldp:contains ?files ;
            ldp:membershipResource ?files .
            ?relatedFileset info:hasModel 'IRFileSet' ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:Object ;
            rdf:type works:FileSet ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            pcdm:hasFile ?relatedFile ;
            pcdm:memberOf ?jupiterRelatedObject ;
            fedora:hasParent ?jupiterRelatedObject ;
            ldp:contains ?relatedFiles ;
            ldp:membershipResource ?relatedFiles .
            ?relatedFiles info:hasModel 'ActiveFedora::DirectContainer' ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type ldp:DirectContainer ;
            rdf:type ldp:RDFSource ;
            ldp:hasMemberRelation pcdm:hasFile ;
            ldp:contains ?relatedFile ;
            fedora:hasParent ?relatedFileset .
            ?relatedFile info:hasModel 'File' ;
            rdf:type ldp:NonRDFSource ;
            rdf:type fedora:Binary ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:File ;
            rdf:type use:OriginalFile ;
            rdf:type pcdm:File ;
            pcdm:fileOf ?relatedFileset ;
            iana:describedby ?relatedFileFCR ;
            fedora:hasParent ?relatedFiles ;
            fedora:hasFixityService ?relatedFileFixity ;
            ebucore:filename ?relatedOriginalName ;
            ebucore:hasMimeType ?relatedMimeType ;
            premis:hasMessageDigest ?relatedFedoraDigest ;
            premis:hasSize ?relatedSize ;
            rdf:type ?relatedRdfType ;
            fedora:mixinTypes ?relatedFileMixins .
            ?relatedFileFCR rdf:type ?relatedFileFCRRDFType ;
            iana:describes ?relatedFile ;
            fedora:hasVersions ?relatedFileVersions ;
            fedora:uuid ?relatedFileFCRUUID ;
            fedora:mixinTypes ?relatedFileFCRMixins ;
            fedora:primaryType ?relatedFileFCRPrimaryType ;
            fedora:created ?relatedFedoraCreated ;
            fedora:lastModified ?relatedFedoraLastModified ;
            fedora:createdBy ?relatedFedoraCreatedBy ;
            fedora:lastModifiedBy ?relatedFedoraLastModifiedBy ;
            fedora:writable ?relatedFedoraWritable .
            ?proxy ore:proxyIn ?jupiterRelatedObject ;
            ore:proxyFor ?relatedFileset ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type ore:Proxy ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            info:hasModel 'ActiveFedora::Aggregation::Proxy' ;
            iana:next ?proxy;
            iana:prev ?proxy .
            ?jupiterRelatedObject iana:first ?proxy ;
            iana:last ?proxy ."""
        self.select = """SELECT distinct ?resource WHERE {
            ?resource rdf:type fedora:Binary .
        }"""
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = []
            for fileType in ['fedora3foxml', 'era1stats']:
                filesetId = generatefileSetId()
                self.queries[group].append({})
                # synthesize a query that fetches a subgroup of resources and constructs a transformed graph from this subgroup
                where = """WHERE {{
                    ?relatedObject rdf:type fedora:Binary .
                    FILTER (STRSTARTS(str(?relatedObject), '{}')) .
                    FILTER (STRENDS(str(?relatedObject), '{}')) """.format(self.splitBy[group], fileType)
                # customize the where clause to include triples that aren't in the mappings
                self.queries[group][-1]['prefix'] = self.prefixes
                self.queries[group][-1]['construct'] = self.construct + " }"
                self.queries[group][-1]['where'] = """{} .
                    OPTIONAL {{ ?relatedObject fedora:created ?relatedFedoraCreated . FILTER (str(?relatedFedoraCreated) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:createdBy ?relatedFedoraCreatedBy . FILTER (str(?relatedFedoraCreatedBy) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:lastModified ?relatedFedoraLastModified . FILTER (str(?relatedFedoraLastModified) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:lastModifiedBy ?relatedFedoraLastModifiedBy . FILTER (str(?relatedFedoraLastModifiedBy) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:writable ?relatedFedoraWritable . FILTER (str(?relatedFedoraWritable) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:uuid ?relatedFedoraUUID . FILTER (str(?relatedFedoraUUID) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:digest ?relatedFedoraDigest . FILTER (str(?relatedFedoraDigest) != '') }} .
                    OPTIONAL {{ ?relatedObject rdf:type ?relatedRdfType . FILTER (str(?relatedRdfType) != '') }} .
                    OPTIONAL {{ ?relatedObject premis:hasSize ?relatedSize . FILTER (str(?relatedSize) != '') }} .
                    OPTIONAL {{ ?relatedObject premis:hasOriginalName ?relatedOriginalName . FILTER (str(?relatedOriginalName) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:mimeType ?relatedMimeType . FILTER (str(?relatedMimeType) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:mixinTypes ?relatedFileMixins . FILTER (str(?relatedFileMixins) != '') }} .
                    OPTIONAL {{ ?relatedObject fedora:hasParent ?relatedParent }} .
                    BIND(URI(replace(str(?relatedObject), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterRelatedObject)
                    BIND(URI(CONCAT(STR(?relatedObject), '/files')) AS ?relatedFiles) .
                    BIND(STR(replace(replace(replace(str(?relatedObject), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', ''),'/{}',''), '^.+/', '')) AS ?noid) .
                    BIND(URI(CONCAT(STR(?relatedFiles), CONCAT('/', ?noid))) AS ?relatedFile) .
                    BIND(URI(CONCAT(STR(?relatedFile), '/fcr:metadata')) AS ?relatedFileFCR) .
                    BIND(URI(CONCAT(STR(?relatedFile), '/fcr:fixity')) AS ?relatedFileFixity) .
                    BIND(URI(CONCAT(STR(?relatedFile), '/fcr:versions')) AS ?relatedFileVersions) .
                    OPTIONAL {{ ?relatedFileFCR rdf:type ?relatedFileFCRRDFType . FILTER (str(?relatedFileFCRRDFType) != '') }} .
                    OPTIONAL {{ ?relatedFileFCR fedora:uuid ?relatedFileFCRUUID . FILTER (str(?relatedFileFCRUUID) != '') }} .
                    OPTIONAL {{ ?relatedFileFCR fedora:mixinTypes ?relatedFileFCRMixins . FILTER (str(?relatedFileFCRMixins) != '') }} .
                    OPTIONAL {{ ?relatedFileFCR fedora:primaryType ?relatedFileFCRPrimaryType . FILTER (str(?relatedFileFCRPrimaryType) != '') }} .
                    BIND(URI(replace(str(?jupiterRelatedObject), '/{}', '')) AS ?jupiterResource) .
                    BIND(URI(CONCAT(STR(?jupiterRelatedObject), '/{}')) AS ?relatedFileset) .
                    BIND(URI(CONCAT(str(?jupiterRelatedObject), '/proxy{}')) AS ?proxy) .
                    }}""".format(where, fileType, fileType, filesetId, generateProxyId(random.choice('0123456789ABCDEF') for i in range(16)))
            self.writeQueries()


"""TRANSFORMATION functions for handling data passed over by the data object. Takes a triple, detects what kind of action needs to be taken based on the predicate, sends it to the appropriate function for transformations, then returns it back to the data handler to be saved."""

class Transformation():

    def __init__(self):
        self.output = []

    def subject(self, triple, objectType):
        """strip whitespaces/periods off front and back & capitalize first letter"""
        triple['object']['value'] = triple['object']['value'].strip().strip('.')
        triple['object']['value'] = triple['object']['value'][0].upper() + triple['object']['value'][1:]
        self.output.append(triple)
        return self.output

    def language(self, triple, objectType):
        # normalize values and convert to URI (consult the "vocabs" variable from the config file (this folder))
        for vocab in vocabs["language"]:
            # mint a new triple with the mapped type
            if triple['object']['value'] in vocab["mapping"]:
                self.output.append(
                    {
                        'subject': {
                            'value': triple['subject']['value'],
                            'type': 'uri'
                        },
                        'predicate': {
                            'value': triple['predicate']['value'],
                            'type': 'uri'
                        },
                        'object': {
                            'value': vocab["uri"],
                            'type': 'uri'
                        }
                    }
                )

            # "other" labels can be changed to specific languages manually.

        return self.output

    def rights(self, triple, objectType):
        # several different license values need to be coerced into one common value, this needs to be confirmed with leah before it is written
        self.output.append(triple)
        return self.output

    def aclvisibilityAfterEmbargo(self, triple, objectType):
        if ("open" in triple['object']['value']) or ("open access" in triple['object']['value']):
            triple['object']['value'] = "http://terms.library.ualberta.ca/public"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output
        elif "university_of_alberta" in triple['object']['value']:
            triple['object']['value'] = "http://terms.library.ualberta.ca/authenticated"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output

    def institution(self, triple, objectType):
        self.output.append(
            {
                'subject': {
                    'value': triple['subject']['value'],
                    'type': 'uri'
                },
                'predicate': {
                    'value': triple['predicate']['value'],
                    'type': 'uri'
                },
                'object': {
                    'value': 'http://id.loc.gov/authorities/names/n79058482',
                    'type': 'uri'
                }
            }
        )
        return self.output

    def license(self, triple, objectType):
        # convert licenses from text to URI (use vocabs variable, some coersion will be necessary)
        if "I am required to use/link to a publisher's license" in triple['object']['value']:
            return None
        else:
            for vocab in vocabs["license"]:
                if triple['object']['value'] in vocab["mapping"]:
                    self.output.append(
                        {
                            'subject': {
                                'value': triple['subject']['value'],
                                'type': 'uri'
                            },
                            'predicate': {
                                'value': triple['predicate']['value'],
                                'type': 'uri'
                            },
                            'object': {
                                'value': vocab["uri"],
                                'type': 'uri'
                            }
                        }
                    )
            if len(self.output) > 0:
                return self.output
            else:
                self.output.append(
                    {
                        'subject': {
                            'value': triple['subject']['value'],
                            'type': 'uri'
                        },
                        'predicate': {
                            'value': "http://purl.org/dc/elements/1.1/rights",
                            'type': 'uri'
                        },
                        'object': {
                            'value': triple['object']['value'],
                            'type': 'literal'
                        }
                    }
                )
                return self.output

    def type(self, triple, objectType):
        if objectType == 'generic':
            for vocab in vocabs["type"]:
                # mint a new triple with the mapped type
                if triple['object']['value'] in vocab["mapping"]:
                    self.output.append(
                        {
                            'subject': {
                                'value': triple['subject']['value'],
                                'type': 'uri'
                            },
                            'predicate': {
                                'value': triple['predicate']['value'],
                                'type': 'uri'
                            },
                            'object': {
                                'value': vocab["uri"],
                                'type': 'uri'
                            }
                        }
                    )
            else:
                pass
        elif (objectType == 'community') or (objectType == 'collection'):
            self.output.append(triple)
        return self.output

    def modelsmemberOf(self, triple, objectType):
        if "http" not in triple['object']['value']:
            value = triple['object']['value']
            triple['object']['value'] = "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/{}/{}/{}/{}/{}".format(value[0:2], value[2:4], value[4:6], value[6:8], value)
            triple['object']['type'] = 'uri'
        self.output.append(triple)
        return self.output

    def modelshasMember(self, triple, objectType):
        if "http" not in triple['object']['value']:
            value = triple['object']['value']
            triple['object']['value'] = "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/{}/{}/{}/{}/{}".format(value[0:2], value[2:4], value[4:6], value[6:8], value)
            triple['object']['type'] = 'uri'
        self.output.append(triple)
        return self.output

    def accessRights(self, triple, objectType):
        if "http://projecthydra.org/ns/auth/group#public" in triple['object']['value']:
            triple['object']['value'] = "http://terms.library.ualberta.ca/public"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output
        elif ("http://projecthydra.org/ns/auth/group#university_of_alberta" in triple['object']['value']) or ("http://projecthydra.org/ns/auth/group#registered" in triple['object']['value']):
            triple['object']['value'] = "http://terms.library.ualberta.ca/authenticated"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output
        else:
            triple['object']['value'] = "http://terms.library.ualberta.ca/draft"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output

    def available(self, triple, objectType):
        if datetime.strptime(re.sub(r"[T].+$", "", triple['object']['value']), "%Y-%m-%d").date() > date.today():
            print(triple['subject']['value'])
            self.output.append(
            {
                'subject': {
                    'value': triple['subject']['value'],
                    'type': 'uri'
                },
                'predicate': {
                    'value': "http://purl.org/dc/terms/accessRights",
                    'type': 'uri'
                },
                'object': {
                    'value': "http://terms.library.ualberta.ca/embargo",
                    'type': 'uri'
                }
            }
            )
        self.output.append(triple)
        return self.output
        
    def createdDate(self, subjects, triple, objectType):
        tempTriple = {
            'subject': {
                'value': triple['subject']['value'],
                'type': 'uri'
            },
            'predicate': {
                'value': triple['predicate']['value'],
                'type': 'uri'
            },
            'object': {
                'value': subjects["object"][0],
                'type': 'date'
            }
        }
        self.output.append(tempTriple)
        Transformation.sortYear(self, tempTriple, objectType)
        return self.output

    def gradDate(self, subjects, triple, objectType):
        tempTriple = {
            'subject': {
                'value': triple['subject']['value'],
                'type': 'uri'
            },
            'predicate': {
                'value': triple['predicate']['value'],
                'type': 'uri'
            },
            'object': {
                'value': subjects["object"][0],
                'type': 'date'
            }
        }
        self.output.append(tempTriple)
        Transformation.sortYear(self, tempTriple, objectType)
        return self.output

    def sortYear(self, triple, objectType):
        self.output.append(
            {
                'subject': {
                    'value': triple['subject']['value'],
                    'type': 'uri'
                },
                'predicate': {
                    'value': triple['predicate']['value'],
                    'type': 'uri'
                },
                'object': {
                    'value': triple['object']['value'],
                    'type': 'date'
                }
            }
        )
        if isinstance(triple['object']['value'], list):
            text = triple['object']['value'][0].replace(';', ' ').replace(':', ' ').replace('_', ' ').replace('-', ' ').replace('/', ' ').replace('.', ' ').replace(',', ' ')
        else:
            text = triple['object']['value'].replace(';', ' ').replace(':', ' ').replace('_', ' ').replace('-', ' ').replace('/', ' ').replace('.', ' ').replace(',', ' ')
        tokens = word_tokenize(text)
        for n,i in enumerate(tokens):
            if i == "," :
                del tokens[n]
            if i == ")" :
                del tokens[n]
            if i == "(" :
                del tokens[n]
        years = DateFinder(tokens)
        trans = years.getyear()
        if trans != None:
            for i in trans:
                self.output.append(
                    {
                        'subject': {
                            'value': triple['subject']['value'],
                            'type': 'uri'
                        },
                        'predicate': {
                            'value': 'http://terms.library.ualberta.ca/date/sort_year',
                            'type': 'uri'
                        },
                        'object': {
                            'value': i["year"],
                            'type': 'date'
                        }
                    }
                )
            return self.output

    def owner(self, triple, objectType):
        triple['object']['value'] = triple['subject']['value'].strip("http://projecthydra.org/ns/auth/person#")
        triple['object']['value'] = triple['subject']['value'].strip("http://projecthydra.org/ns/auth/group#")
        self.output.append(triple)
        return self.output


if __name__ == "__main__":
    main()
