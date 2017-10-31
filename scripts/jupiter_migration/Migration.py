from config import types, sparqlTerms, sparqlData, sparqlResults, mig_ns, vocabs
from utilities import PrintException, cleanOutputs
import concurrent.futures
import time
from datetime import datetime
import os
from SPARQLWrapper import JSON, SPARQLWrapper
from rdflib import URIRef, Literal, Graph
import re
import json
import requests


def main():
    """ main controller: iterates over each object type (generic item metadata, thesis item metadata, and binary-level metadata), 
    creates a set of subqueries for each of these types, then cues threads to run each of these subqueries as a job. The migration outout is saved to
    the results folder and to a triplestore. The subqueries are cached in the cache folder. Custom settings can be modified in config.py."""
    ts = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print('cleaning the cache')
    cleanOutputs(types, sparqlResults)
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
    return None


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
        elif objectType == "file":
            return File(sparqlData)
        elif objectType == "relatedObject":
            return Related_Object(sparqlData)
        else:
            return None


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
        self.graph.serialize(destination=self.filename, format='nt')

    def resultsToTriplestore(self):
        headers = {'Content-Type': 'text/turtle'}
        requests.post(sparqlResults, data=self.graph.serialize(format='nt'), headers=headers)


"""Pulls current mappings from triplestore, dynamically builds queries in managable sizes"""


class Query(object):
    """ Query objects are dynamically generated, and contain SPARQL CONSTRUCT queries with input from the jupiter application profile """
    def __init__(self, objectType, sparqlData, sparqlTerms=sparqlTerms):
        self.mapping = []
        self.sparqlTerms = SPARQLWrapper(sparqlTerms)  # doesn't need to change (the terms store doesn't change)
        self.sparqlData = SPARQLWrapper(sparqlData)  # sets the triple store from which to get data (simple, test, or dev)
        self.sparqlResults = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/results/sparql")
        self.sparqlTerms.setMethod("POST")
        self.sparqlData.setMethod("POST")
        self.sparqlResults.setMethod("POST")
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
        query = "prefix fedora: <http://fedora.info/definitions/v4/repository#> prefix ldp: <http://www.w3.org/ns/ldp#> prefix dcterm: <http://purl.org/dc/terms/> prefix info: <info:fedora/fedora-system:def/model#> prefix ual: <http://terms.library.ualberta.ca/> {0}".format(self.select).replace('\n', '')
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
        for query in self.queries:
            self.queries[query]['construct'] = ' '.join(self.queries[query]['construct'].replace('\n', ' ').split())
            self.queries[query]['where'] = ' '.join(self.queries[query]['where'].replace('\n', ' ').split())
        filename = "cache/{0}.json".format(self.objectType)
        with open(filename, 'w+') as f:
            json.dump([self.queries], f, sort_keys=True, indent=4, separators=(',', ': '))


class Collection(Query):
    def __init__(self, sparqlData):
        self.objectType = 'collection'
        self.construct = """CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            rdf:type pcdm:Collection"""
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
        self.queries['collection'] = {}
        for where in self.where:
            construct = self.construct
            for pair in self.mapping:
                construct = "{0} ; <{1}> ?{2} ".format(construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " {0} . OPTIONAL {{ ?resource <{1}> ?{2} . FILTER (str(?{3})!='') }}".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries['collection']['prefix'] = self.prefixes
            self.queries['collection']['construct'] = construct + "}"
            self.queries['collection']['where'] = """{} . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)}}""".format(where)
        self.writeQueries()


class Community(Query):
    def __init__(self, sparqlData):
        self.objectType = 'community'
        self.construct = """CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            rdf:type pcdm:Object; rdf:type ual:Community"""
        self.where = ["""WHERE { ?resource info:hasModel 'Collection'^^xsd:string ;
            OPTIONAL { ?resource ualids:is_community 'true'^^xsd:boolean } .
            OPTIONAL { ?resource ualid:is_community 'true'^^xsd:boolean } .
            OPTIONAL { ?resource ual:is_community 'true'^^xsd:boolean }"""]
        self.select = None
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.queries['community'] = {}
        for where in self.where:
            construct = self.construct
            for pair in self.mapping:
                construct = "{0} ; <{1}> ?{2} ".format(construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " {0} . OPTIONAL {{ ?resource <{1}> ?{2} . FILTER (str(?{3})!='') }}".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries['community']['prefix'] = self.prefixes
            self.queries['community']['construct'] = construct + "}"
            self.queries['community']['where'] = """{} . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)}}""".format(where)
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
            acl:visibilityAfterEmbargo ?visAfter"""
        self.where = []
        self.select = """SELECT distinct ?resource WHERE {
            ?resource info:hasModel 'GenericFile'^^xsd:string ;
            dcterm:type ?type . filter(str(?type) != 'Thesis'^^xsd:string)
        }"""
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = {}
            # synthesize a query that fetches a subgroup of resources and constructs a transformed graph from this subgroup
            where = """WHERE {{
                ?resource info:hasModel 'GenericFile'^^xsd:string ;
                dcterm:type ?type . filter(str(?type) != 'Thesis'^^xsd:string) .
                FILTER (contains(str(?resource), '{}'))""".format(self.splitBy[group])
            construct = self.construct
            for pair in self.mapping:
                construct = "{0} ; <{1}> ?{2} ".format(construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = """ {0} .
                            OPTIONAL {{
                                ?resource <{1}> ?{2} .
                                FILTER (str(?{3})!='')
                            }}""".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            # customize the where clause to include triples that aren't in the mappings
            self.queries[group]['prefix'] = self.prefixes
            self.queries[group]['construct'] = construct + " }"
            self.queries[group]['where'] = """{} .
                OPTIONAL {{ ?permission webacl:accessTo ?resource ;
                    webacl:mode webacl:Write ;
                webacl:agent ?owner }} .
                OPTIONAL {{ ?resource acl:hasEmbargo ?embargo .
                    OPTIONAL {{ ?embargo acl:embargoReleaseDate ?available }} .
                    OPTIONAL {{ ?embargo acl:embargoHistory ?history }} .
                    OPTIONAL {{ ?embargo acl:visibilityAfterEmbargo ?visAfter }}
                }}
                BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)
            }}""".format(where)
        self.writeQueries()


class Thesis(Query):
    def __init__(self, sparqlData):
        self.objectType = 'thesis'
        self.construct = """CONSTRUCT {
            ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            dcterm:available ?available ;
            dcterm:accessRights ?visibility; rdf:type works:Work ;
            rdf:type pcdm:Object ;
            rdf:type bibo:Thesis; bibo:owner ?owner ;
            acl:embargoHistory ?history ;
            acl:visibilityAfterEmbargo ?visAfter"""
        self.where = []
        self.select = """SELECT distinct ?resource WHERE {
            ?resource info:hasModel 'GenericFile'^^xsd:string ;
            dcterm:type 'Thesis'^^xsd:string
        }"""
        super().__init__(self.objectType, sparqlData)


    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = {}
            where = """WHERE {{ ?resource info:hasModel 'GenericFile'^^xsd:string ;
                dcterm:type 'Thesis'^^xsd:string .
                FILTER (contains(str(?resource), '{0}'))""".format(self.splitBy[group])
            construct = self.construct
            for pair in self.mapping:
                construct = "{0} ; <{1}> ?{2}".format(construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " {0} . OPTIONAL {{ ?resource <{1}> ?{2} . FILTER (str(?{3})!='') }} ".format(where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries[group]['prefix'] = self.prefixes
            self.queries[group]['construct'] = construct + " }"
            self.queries[group]['where'] = """{} .
                OPTIONAL {{
                    ?permission webacl:accessTo ?resource ;
                    webacl:mode webacl:Read ;
                    webacl:agent ?visibility
                }} .
                OPTIONAL {{
                    ?permission webacl:accessTo ?resource ;
                    webacl:mode webacl:Write ;
                    webacl:agent ?owner
                }} .
                OPTIONAL {{
                    ?resource acl:hasEmbargo ?embargo .
                    OPTIONAL {{ ?embargo acl:embargoReleaseDate ?available }} .
                    OPTIONAL {{ ?embargo acl:embargoHistory ?history }} .
                    OPTIONAL {{ ?embargo acl:visibilityAfterEmbargo ?visAfter }}
                }} .
                BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)
            }}""".format(where)
        self.writeQueries()


class File(Query):
    """ direct members: content and characterization"""
    def __init__(self, sparqlData):
        self.objectType = 'file'
        # custom construct clause to capture unmapped triples
        self.construct = """CONSTRUCT {
            ?jupiterResource pcdm:hasMember ?directFileset ;
            iana:first ?proxy .
            ?proxy ore:proxyIn ?jupiterResource ;
            ore:proxyFor ?directFileset ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type ore:Proxy ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            info:hasModel 'ActiveFedora::Aggregation::Proxy' .
            ?directFileset info:hasModel 'IRFileSet' ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:Object ;
            rdf:type works:FileSet ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            pcdm:hasFile ?directFile ;
            pcdm:isMemberOf ?jupiterResource ;
            fedora:hasParent ?jupiterResource ;
            ldp:contains ?directFiles ;
            ldp:membershipResource ?directFiles .
            ?directFiles info:hasModel 'ActiveFedora::DirectContainer' ;
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
            ldp:contains ?directFile .
            ?directFile info:hasModel 'File' ;
            rdf:type ldp:NonRDFSource ;
            rdf:type fedora:Binary ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:File ;
            rdf:type use:OriginalFile ;
            rdf:type pcdm:File ;
            pcdm:fileOf ?directFileset ;
            iana:describedby ?directFileFCR ;
            pcdm:isMemberOf ?directFileset ;
            fedora:hasParent ?directFiles ;
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
            ?directFileFCR rdf:type ?directFCRRrdf ;
            iana:describes ?directFile ;
            fedora:hasVersions ?directFileVersions ;
            fedora:uuid ?directFileUUID ;
            fedora:mixinTypes ?directFileFCRMixins ;
            fedora:primaryType ?primaryType ;
            rdf:type ?directFCRRDFType ;
            fedora:created ?fedoraCreated ;
            fedora:lastModified ?fedoraLastModified ;
            fedora:createdBy ?fedoraCreatedBy ;
            fedora:lastModifiedBy ?fedoraLastModifiedBy ;
            fedora:writable ?directFedoraWritable ."""
        self.select = """SELECT distinct ?resource WHERE {
            ?resource info:hasModel 'GenericFile'^^xsd:string
        }"""
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        order = {1: 'first', 2: 'last'}
        proxyNum = 1
        for fileType in ['content', 'characterization']:
            print('building queries from {} objects'.format(fileType))
            for group in self.splitBy.keys():
                self.queries[group] = {}
                # synthesize a query that fetches a subgroup of resources and constructs a transformed graph from this subgroup
                where = """WHERE {{
                    ?directMember rdf:type fedora:Binary .
                    FILTER (STRSTARTS(str(?directMember), '{}')) .
                    FILTER (STRENDS(str(?directMember), '{}'))""".format(self.splitBy[group], fileType)
                # customize the where clause to include triples that aren't in the mappings
                self.queries[group]['prefix'] = self.prefixes
                self.queries[group]['construct'] = self.construct + "?jupiterResource iana:%s ?proxy }" % (order[proxyNum])
                self.queries[group]['where'] = """{} .
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
                        BIND(URI(replace(str(?directMember), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterDirectMember)
                        BIND(URI(CONCAT(STR(?directMember), '/fileset')) AS ?directFileset) .
                        BIND(URI(CONCAT(STR(?directMember), '/files')) AS ?directFiles) .
                        BIND(URI(CONCAT(STR(?directMember), '/member_of_collections')) AS ?directMemberOfCollections) .
                        BIND(URI(CONCAT(STR(?directFiles), CONCAT('/', 'NOID'))) AS ?directFile) .
                        BIND(URI(CONCAT(STR(?directFiles), '/NOID/fcr:metadata', '')) AS ?directFileFCR) .
                        BIND(URI(CONCAT(STR(?directFiles), '/NOID/fcr:fixity', '')) AS ?directFileFixity) .
                        BIND(URI(CONCAT(STR(?directFiles), '/NOID/fcr:versions', '')) AS ?directFileVersions) .
                        OPTIONAL {{ ?directFileFCR rdf:type ?directFCRRDFType . FILTER (str(?directFCRRDFType) != '')}} .
                        OPTIONAL {{ ?directFileFCR fedora:uuid ?directFileUUID . FILTER (str(?directFileUUID) != '')}} .
                        OPTIONAL {{ ?directFileFCR fedora:mixinTypes ?directFileFCRMixins . FILTER (str(?directFileFCRMixins) != '')}} .
                        OPTIONAL {{ ?directFileFCR fedora:primaryType ?directPrimaryType . FILTER (str(?directPrimaryType) != '')}} .
                        BIND(URI(CONCAT(str(?directMember), '/proxy{}')) AS ?proxy)
                        BIND(URI(replace(str(?directMember), '{}/', '')) AS ?resource)
                        BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)
                    }}""".format(where, fileType, proxyNum)
            self.writeQueries()
            proxyNum = proxyNum + 1


class Related_Object(Query):
    """ related members: content and characterization"""
    def __init__(self, sparqlData):
        self.objectType = 'relatedObject'
        # custom construct clause to capture unmapped triples
        self.construct = """CONSTRUCT {
            ?jupiterResource pcdm:hasRelatedObject ?jupiterRelatedObject ;
            ldp:contains ?jupiterRelatedObject ;
            pcdm:hasMember ?jupiterRelatedObject .
            ?jupiterRelatedObject info:hasModel 'IRItem' ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:Object ;
            rdf:type works:Work ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            fedora:created ?fedoraCreated ;
            fedora:lastModified ?fedoraLastModified ;
            fedora:createdBy ?fedoraCreatedBy ;
            fedora:lastModifiedBy ?fedoraLastModifiedBy ;
            fedora:writable ?relatedFedoraWritable ;
            pcdm:hasMember ?relatedFileset ;
            fedora:hasParent ?jupiterResource ;
            ldp:contains ?files ;
            ldp:membershipResource ?files .
            ?proxy ore:proxyIn ?jupiterRelatedObject ;
            ore:proxyFor ?relatedFileset ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type ore:Proxy ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            info:hasModel 'ActiveFedora::Aggregation::Proxy' .
            ?relatedFileset info:hasModel 'IRFileSet' ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:Object ;
            rdf:type works:FileSet ;
            rdf:type ldp:Container ;
            rdf:type ldp:RDFSource ;
            pcdm:hasFile ?relatedFile ;
            pcdm:isMemberOf ?jupiterRelatedObject ;
            fedora:hasParent ?jupiterRelatedObject ;
            pcdm:relatedObjectOf ?jupiterResource ;
            ldp:contains ?relatedFiles ;
            ldp:membershipResource ?relatedFiles .
            ?relatedFiles info:hasModel 'ActiveFedora::DirectContainer' ;
            rdf:type fedora:Container ;
            rdf:type fedora:Resource ;
            rdf:type ldp:DirectContainer ;
            rdf:type ldp:RDFSource ;
            fedora:created ?fedoraCreated ;
            fedora:lastModified ?fedoraLastModified ;
            fedora:createdBy ?fedoraCreatedBy ;
            fedora:lastModifiedBy ?fedoraLastModifiedBy ;
            fedora:writable ?relatedFedoraWritable ;
            ldp:hasMemberRelation pcdm:hasFile ;
            ldp:contains ?relatedFile .
            ?relatedFile info:hasModel 'File' ;
            rdf:type ldp:NonRDFSource ;
            rdf:type fedora:Binary ;
            rdf:type fedora:Resource ;
            rdf:type pcdm:File ;
            rdf:type use:OriginalFile ;
            rdf:type pcdm:File ;
            pcdm:fileOf ?relatedFileset ;
            iana:describedby ?relatedFileFCR ;
            pcdm:isMemberOf ?relatedFileset ;
            fedora:hasParent ?relatedFiles ;
            fedora:hasFixityService ?relatedFileFixity ;
            ebucore:filename ?relatedOriginalName ;
            ebucore:hasMimeType ?relatedMimeType ;
            premis:hasMessageDigest ?relatedFedoraDigest ;
            premis:hasSize ?relatedSize ;
            fedora:created ?fedoraCreated ;
            fedora:lastModified ?fedoraLastModified ;
            fedora:createdBy ?fedoraCreatedBy ;
            fedora:lastModifiedBy ?fedoraLastModifiedBy ;
            fedora:writable ?relatedFedoraWritable ;
            rdf:type ?relatedRdfType ;
            fedora:mixinTypes ?relatedFileMixins .
            ?relatedFileFCR rdf:type ?relatedFCRRrdf ;
            iana:describes ?relatedFile ;
            fedora:hasVersions ?relatedFileVersions ;
            fedora:uuid ?relatedFileUUID ;
            fedora:mixinTypes ?relatedFileFCRMixins ;
            fedora:primaryType ?primaryType ;
            rdf:type ?relatedFCRRDFType ;
            fedora:created ?fedoraCreated ;
            fedora:lastModified ?fedoraLastModified ;
            fedora:createdBy ?fedoraCreatedBy ;
            fedora:lastModifiedBy ?fedoraLastModifiedBy ;
            fedora:writable ?relatedFedoraWritable . """
        self.select = """SELECT distinct ?resource WHERE {
            ?resource info:hasModel 'GenericFile'^^xsd:string
        }"""
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        order = {1: 'first', 2: 'last'}
        proxyNum = 1
        for fileType in ['fedora3foxml', 'era1stats']:
            print('building queries from {} objects'.format(fileType))
            for group in self.splitBy.keys():
                self.queries[group] = {}
                # synthesize a query that fetches a subgroup of resources and constructs a transformed graph from this subgroup
                where = """WHERE {{
                    ?relatedObject rdf:type fedora:Binary .
                    FILTER (STRSTARTS(str(?relatedObject), '{}')) .
                    FILTER (STRENDS(str(?relatedObject), '{}'))""".format(self.splitBy[group], fileType)
                # customize the where clause to include triples that aren't in the mappings
                self.queries[group]['prefix'] = self.prefixes
                self.queries[group]['construct'] = self.construct + "?jupiterResource iana:%s ?proxy }" % (order[proxyNum])
                self.queries[group]['where'] = """{} .
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
                    BIND(URI(replace(str(?relatedObject), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterRelatedObject)
                    BIND(URI(CONCAT(STR(?relatedObject), '/files')) AS ?relatedFiles) .
                    BIND(URI(CONCAT(STR(?relatedObject), '/member_of_collections')) AS ?relatedMemberOfCollections) .
                    BIND(URI(CONCAT(STR(?relatedObject), '/fileset')) AS ?relatedFileset) .
                    BIND(URI(CONCAT(STR(?relatedFiles), CONCAT('/', 'NOID'))) AS ?relatedFile) .
                    BIND(URI(CONCAT(STR(?relatedFiles), '/NOID/fcr:metadata', '')) AS ?relatedFileFCR) .
                    BIND(URI(CONCAT(STR(?relatedFiles), '/NOID/fcr:fixity', '')) AS ?relatedFileFixity) .
                    BIND(URI(CONCAT(STR(?relatedFiles), '/NOID/fcr:versions', '')) AS ?relatedFileVersions) .
                    OPTIONAL {{ ?relatedFileFCR rdf:type ?relatedFCRRDFType . FILTER (str(?relatedFCRRDFType) != '') }} .
                    OPTIONAL {{ ?relatedFileFCR fedora:uuid ?relatedFileUUID . FILTER (str(?relatedFileUUID) != '') }} .
                    OPTIONAL {{ ?relatedFileFCR fedora:mixinTypes ?relatedFileFCRMixins . FILTER (str(?relatedFileFCRMixins) != '') }} .
                    OPTIONAL {{ ?relatedFileFCR fedora:primaryType ?primaryType . FILTER (str(?primaryType) != '') }} .
                    BIND(URI(CONCAT(str(?relatedObject), '/proxy{}')) AS ?proxy)
                    BIND(URI(replace(str(?relatedObject), '{}/', '')) AS ?resource)
                    BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)
                    }}""".format(where, fileType, proxyNum)
            self.writeQueries()
            proxyNum = proxyNum + 1


"""TRANSFORMATION functions for handling data passed over by the data object. Takes a triple, detects what kind of action needs to be taken based on the predicate, sends it to the appropriate function for transformations, then returns it back to the data handler to be saved."""

class Transformation():

    def __init__(self):
        self.output = []

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
            triple['object']['value'] = "http://terms.library.ualberta.ca/private"
            triple['object']['type'] = 'uri'
            self.output.append(triple)
            return self.output

    def available(self, triple, objectType):
        self.output.append(triple)
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
                    'value': "http://terms.library.ualberta.ca/public",
                    'type': 'uri'
                }
            }
        )
        return self.output



if __name__ == "__main__":
    main()
