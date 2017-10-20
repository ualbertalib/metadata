from config import sparqlTerms, mig_ns, vocabs, types, sparqlData, sparqlResults
try:
    from config import sparql_mig_test as sparqlData
except:
    pass
try:
    from config import sparql_mig_simple as sparqlData
except:
    pass
try:
    from config import sparql_mig_dev as sparqlData
except:
    pass
from config import sparqlResults as sparqlResults
from SPARQLWrapper import JSON, SPARQLWrapper
from utilities import PrintException, cleanOutputs
import re
import os
import concurrent.futures
import json
import requests
import time
from datetime import datetime
from rdflib import URIRef, Literal, Graph


def main():
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
        print('%s queries generated' % (objectType))
        print('%i queries of %s objects to be transformed' % (len(queryObject.queries), objectType))
        i = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_result = {executor.submit(parellelTransform, queryObject, group): group for group in queryObject.queries.keys()}
            for future in concurrent.futures.as_completed(future_to_result):
                future_to_result[future]
                try:
                    i = i + 1
                    future.result()
                    print("%i of %i %s queries transformed" % (i, len(queryObject.queries), objectType))
                except Exception:
                    PrintException()
        print("%s objects transformation completed" % (objectType))
        del queryObject
    tf = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    print("walltime:", datetime.strptime(tf, '%H:%M:%S') - datetime.strptime(ts, '%H:%M:%S'))


def parellelTransform(queryObject, group):
    DTO = Data(queryObject.queries[group], group, queryObject.sparqlData, sparqlTerms, queryObject)  # query, group, object
    DTO.transformData()
    DTO.resultsToTriplestore()


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
        elif objectType == "era1statsFile":
            return era1statsFile(sparqlData)
        elif objectType == "era1statsFileset":
            return era1statsFileset(sparqlData)
        elif objectType == "fedora3foxmlFile":
            return fedora3foxmlFile(sparqlData)
        elif objectType == "fedora3foxmlFileset":
            return fedora3foxmlFileset(sparqlData)
        elif objectType == "contentFile":
            return contentFile(sparqlData)
        elif objectType == "contentFileset":
            return contentFileset(sparqlData)
        elif objectType == "characterizationFile":
            return characterizationFile(sparqlData)
        elif objectType == "characterizationFileset":
            return characterizationFileset(sparqlData)
        else:
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


# ##  QUERY BUILDER
# ##### Pulls current mappings from triplestore, dynamically builds queries in managable sizes


class Query(object):
    """ Query objects are dynamically generated, and contain SPARQL CONSTRUCT queries with input from the jupiter application profile """
    def __init__(self, objectType, sparqlData, sparqlTerms=sparqlTerms):
        self.mapping = []
        self.sparqlTerms = SPARQLWrapper(sparqlTerms)  # doesn't need to change (the terms store doesn't change)
        self.sparqlData = SPARQLWrapper(sparqlData)  # sets the triple store from which to get data (simple, test, or dev)
        self.sparqlResults = SPARQLWrapper("http://206.167.181.123:9999/blazegraph/namespace/results2/sparql")
        self.sparqlTerms.setMethod("POST")
        self.sparqlData.setMethod("POST")
        self.sparqlResults.setMethod("POST")
        self.queries = {}
        self.splitBy = {}
        self.prefixes = ""
        self.filename = ""
        for ns in mig_ns:
            self.prefixes = self.prefixes + " PREFIX %s: <%s> " % (ns['prefix'], ns['uri'])
        self.getMappings()

    def generateQueries(self):
        pass

    def getMappings(self):
        if (self.objectType == 'collection') or (self.objectType == 'community') or (self.objectType == 'generic') or (self.objectType == 'thesis'):
            query = "prefix ual: <http://terms.library.ualberta.ca/> SELECT * WHERE {GRAPH ual:%s {?newProperty ual:backwardCompatibleWith ?oldProperty} }" % (self.objectType)
            self.sparqlTerms.setReturnFormat(JSON)
            self.sparqlTerms.setQuery(query)
            results = self.sparqlTerms.query().convert()
            for result in results['results']['bindings']:
                self.mapping.append((result['newProperty']['value'], result['oldProperty']['value']))
        else:
            pass

    def getSplitBy(self):
        # base query only needs 3 prefixes appended to the "select" statement defined by the object
        query = "prefix ldp: <http://www.w3.org/ns/ldp#> prefix dcterm: <http://purl.org/dc/terms/> prefix info: <info:fedora/fedora-system:def/model#> prefix fedora: <http://fedora.info/definitions/v4/repository#> prefix ual: <http://terms.library.ualberta.ca/> %s" % (self.select)
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
        directory = 'results/%s' % (self.objectType)
        for (dirpath, dirnames, filenames) in os.walk(directory):
            for filename in filenames:
                with open(os.path.join(dirpath, filename), 'rb') as f:
                    query = "INSERT DATA {%s}" % (f.read())
                    self.sparqlResults.setReturnFormat(JSON)
                    self.sparqlResults.setQuery(query)
                    self.sparqlResults.query()

    def writeQueries(self):
        filename = "cache/%s.json" % (self.objectType)
        with open(filename, 'w+') as f:
            json.dump([self.queries], f, sort_keys=True, indent=4, separators=(',', ': '))


class Collection(Query):
    def __init__(self, sparqlData):
        self.objectType = 'collection'
        self.construct = "CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Collection"
        self.where = ["WHERE { ?resource info:hasModel 'Collection'^^xsd:string . OPTIONAL { ?resource ualids:is_community 'false'^^xsd:boolean } . OPTIONAL { ?resource ualid:is_community 'false'^^xsd:boolean } . OPTIONAL { ?resource ual:is_community 'false'^^xsd:boolean }"]
        self.select = None
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        for where in self.where:
            construct = self.construct
            for pair in self.mapping:
                construct = "%s ; <%s> ?%s" % (construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " %s . OPTIONAL { ?resource <%s> ?%s . FILTER (str(?%s)!='') }" % (where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries['collection'] = "%s %s } %s . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)}" % (self.prefixes, construct, where)
        self.writeQueries


class Community(Query):
    def __init__(self, sparqlData):
        self.objectType = 'community'
        self.construct = "CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ; rdf:type pcdm:Object; rdf:type ual:Community"
        self.where = ["WHERE { ?resource info:hasModel 'Collection'^^xsd:string ; OPTIONAL { ?resource ualids:is_community 'true'^^xsd:boolean } . OPTIONAL { ?resource ualid:is_community 'true'^^xsd:boolean } . OPTIONAL { ?resource ual:is_community 'true'^^xsd:boolean }"]
        self.select = None
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        for where in self.where:
            construct = self.construct
            for pair in self.mapping:
                construct = "%s ; <%s> ?%s" % (construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " %s . OPTIONAL { ?resource <%s> ?%s . FILTER (str(?%s)!='') }" % (where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries['community'] = "%s %s } %s  . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)}" % (self.prefixes, construct, where)
        self.writeQueries()


class File(Query):
    def __init__(self, sparqlData, objectType, filterType):
        self.construct = "CONSTRUCT {?parent pcdm:hasRelatedObject ?relatedObject . ?fileset rdf:type fedora:Container ; rdf:type fedora:Resource ; rdf:type pcdm:Object ; rdf:type works:FileSet; rdf:type ldp:Container ; rdf:type ldp:RDFSource ; pcdm:hasFile ?file ; pcdm:isMemberOf ?relatedObject ; fedora:hasParent ?relatedObject ; ?predicate ?object . ?relatedObject pcdm:relatedObjectOf ?parent ; rdf:type ual:%s ; rdf:type fedora:Container ; rdf:type fedora:Resource ; rdf:type pcdm:Object ; rdf:type works:Work ; rdf:type ldp:Container ; rdf:type ldp:RDFSource ; pcdm:hasMember ?fileset ; fedora:hasParent ?parent . ?file rdf:type ldp:NonRDFSource; rdf:type pcdm:File; pcdm:fileOf ?fileset ; iana:describedby ?fixty ; iana:describedby ?fcr ; fedora:hasParent ?fileset ; ?predicate ?object }" % (self.filterType)
        self.where = "WHERE { ?resource rdf:type ldp:NonRDFSource . FILTER ( strEnds(str(?resource), '%s') && " % (self.filterType)
        self.select = "SELECT distinct ?resource WHERE  {?resource rdf:type ldp:NonRDFSource . FILTER ( strEnds(str(?resource), '%s') ) }" % (self.filterType)
        super().__init__(self.objectType, self.sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = "%s %s %s strStarts(str(?resource), '%s') ) . ?resource ?predicate ?object . FILTER ( !contains(str(?predicate), 'http://www.iana.org/assignments/relation/') && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasFixityService')  && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasParent')  && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasVersions') && str(?object)!='' )  . ?resourceFCR rdf:type fedora:NonRdfSourceDescription . ?resourceFCR ?predicate ?object . FILTER ( strEnds(str(?resourceFCR), '%s/fcr:metadata') && !contains(str(?predicate), 'http://www.iana.org/assignments/relation/') && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasFixityService')  && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasParent')  && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasVersions') && str(?object)!='' ) . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource) . BIND(URI(replace(str(?resourceFCR), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResourceFCR) . BIND(URI(CONCAT(str(?jupiterResource), '/file')) AS ?file)  . BIND(URI(CONCAT(str(?jupiterResourceFCR), '/fileset')) AS ?fileset) . BIND(URI(CONCAT(str(?jupiterResource), '/file/fcr:fixity')) AS ?fixity)  . BIND(URI(CONCAT(str(?jupiterResource), '/file/fcr:metadata')) AS ?fcr) . BIND(URI(REPLACE(STR(?jupiterResource), '/%s', '')) AS ?parent) . BIND(URI(CONCAT(STR(?jupiterResource), '/relatedObject')) AS ?relatedObject) }" % (self.prefixes, self.construct, self.where, self.splitBy[group], self.filterType, self.filterType)
        self.writeQueries()


class Fileset(Query):
    def __init__(self, sparqlData, objectType, filterType):
        self.pcdmType = "works:Fileset"
        self.construct = "CONSTRUCT { ?parent pcdm:hasRelatedObject ?relatedObject . ?fileset rdf:type fedora:Container ; rdf:type fedora:Resource ; rdf:type pcdm:Object ; rdf:type works:FileSet; rdf:type <http://www.w3.org/ns/ldp#Container> ; rdf:type <http://www.w3.org/ns/ldp#RDFSource> ; pcdm:hasFile ?file ; pcdm:isMemberOf ?relatedObject ; fedora:hasParent ?relatedObject . ?relatedObject pcdm:relatedObjectOf ?parent ; rdf:type ual:%s ; rdf:type fedora:Container ; rdf:type fedora:Resource ; rdf:type pcdm:Object ; rdf:type works:Work ; rdf:type <http://www.w3.org/ns/ldp#Container> ; rdf:type <http://www.w3.org/ns/ldp#RDFSource> ; pcdm:hasMember ?fileset ; fedora:hasParent ?parent ; ?predicate ?object } " % (self.filterType)
        self.where = "WHERE { ?resource rdf:type fedora:NonRdfSourceDescription . FILTER ( strEnds(str(?resource), '%s/fcr:metadata') && " % (self.filterType)
        self.select = "SELECT distinct ?resource WHERE {?resource rdf:type fedora:NonRdfSourceDescription . FILTER ( strEnds(str(?resource), '%s/fcr:metadata') ) }" % (self.filterType)
        super().__init__(self.objectType, self.sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = "%s %s %s strStarts(str(?resource), '%s')) . ?resource ?predicate ?object FILTER ( !contains(str(?predicate), 'http://www.iana.org/assignments/relation/') && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasFixityService') && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasParent') && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasVersions') && str(?object)!='' )  . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource) . BIND(URI(REPLACE(STR(?jupiterResource), '/%s/fcr:metadata', '/fileset')) AS ?fileset) . BIND(URI(REPLACE(STR(?jupiterResource), '/%s/fcr:metadata', '/file')) AS ?file)  . BIND(URI(REPLACE(STR(?jupiterResource), '/%s/fcr:metadata', '')) AS ?parent) . BIND(URI(REPLACE(STR(?jupiterResource), '/fcr:metadata', '/relatedObject')) AS ?relatedObject) }" % (self.prefixes, self.construct, self.where, self.splitBy[group], self.filterType, self.filterType, self.filterType)
        self.writeQueries()


class Generic(Query):
    def __init__(self, sparqlData):
        self.objectType = 'generic'
        self.construct = "CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ; dcterm:available ?available ; dcterm:accessRights ?visibility; rdf:type works:Work; rdf:type pcdm:Object ; bibo:owner ?owner ; acl:embargoHistory ?history ; acl:visibilityAfterEmbargo ?visAfter"
        self.where = []
        self.select = "SELECT distinct ?resource WHERE { ?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type ?type . filter(str(?type) != 'Thesis'^^xsd:string) }"
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            where = "WHERE { ?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type ?type . filter(str(?type) != 'Thesis'^^xsd:string) . FILTER (contains(str(?resource), '%s'))" % (self.splitBy[group])
            construct = self.construct
            for pair in self.mapping:
                construct = "%s ; <%s> ?%s" % (construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " %s . OPTIONAL { ?resource <%s> ?%s . FILTER (str(?%s)!='') }" % (where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries[group] = "%s %s } %s . OPTIONAL {?permission webacl:accessTo ?resource ; webacl:mode webacl:Read ; webacl:agent ?visibility } . OPTIONAL {?permission webacl:accessTo ?resource ; webacl:mode webacl:Write ; webacl:agent ?owner } . OPTIONAL {?resource acl:hasEmbargo ?embargo . OPTIONAL {?embargo acl:embargoReleaseDate ?available } . OPTIONAL {?embargo acl:embargoHistory ?history } . OPTIONAL {?embargo acl:visibilityAfterEmbargo ?visAfter } }  . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)}" % (self.prefixes, construct, where)
        self.writeQueries()


class era1statsFile(File):
    def __init__(self, sparqlData):
        self.sparqlData = sparqlData
        self.objectType = 'era1statsFile'
        self.filterType = "era1stats"
        super().__init__(self.sparqlData, self.objectType, self.filterType)


class era1statsFileset(Fileset):
    def __init__(self, sparqlData):
        self.sparqlData = sparqlData
        self.objectType = 'era1statsFileset'
        self.filterType = "era1stats"
        super().__init__(self.sparqlData, self.objectType, self.filterType)


class fedora3foxmlFile(File):
    def __init__(self, sparqlData):
        self.sparqlData = sparqlData
        self.objectType = 'fedora3foxmlFile'
        self.filterType = "fedora3foxml"
        super().__init__(self.sparqlData, self.objectType, self.filterType)


class fedora3foxmlFileset(Fileset):
    def __init__(self, sparqlData):
        self.sparqlData = sparqlData
        self.objectType = 'fedora3foxmlFileset'
        self.filterType = "fedora3foxml"
        super().__init__(self.sparqlData, self.objectType, self.filterType)


class characterizationFile(File):
    def __init__(self, sparqlData):
        self.sparqlData = sparqlData
        self.objectType = 'characterizationFile'
        self.filterType = "characterization"
        super().__init__(self.sparqlData, self.objectType, self.filterType)
        self.construct = "CONSTRUCT { ?file rdf:type ldp:NonRDFSource ; rdf:type fedora:Binary ; rdf:type fedora:Resource ; rdf:type pcdm:File; pcdm:fileOf ?fileset; iana:describedby ?fcr ; ?predicate ?object }"

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = "%s %s %s strStarts(str(?resource), '%s') ) . ?resource ?predicate ?object . FILTER ( !contains(str(?predicate), 'http://www.iana.org/assignments/relation/') && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasFixityService')  && !contains(str(?predicate), 'http://fedora.info/definitions/v4/repository#hasParent') && str(?object)!='' ) . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource) . BIND(URI(CONCAT(str(?jupiterResource), '/file')) AS ?file)  . BIND(URI(REPLACE(str(?jupiterResource), '/characterization', '/fileset')) AS ?fileset) . BIND(URI(CONCAT(str(?jupiterResource), '/file/fcr:fixity')) AS ?fixity)  . BIND(URI(CONCAT(str(?jupiterResource), '/file/fcr:metadata')) AS ?fcr)}" % (self.prefixes, self.construct, self.where, self.splitBy[group])
        self.writeQueries()


class contentFile(File):
    def __init__(self, sparqlData):
        self.sparqlData = sparqlData
        self.objectType = 'contentFile'
        self.filterType = "content"
        super().__init__(self.sparqlData, self.objectType, self.filterType)
        self.construct = "CONSTRUCT { ?fileset rdf:type fedora:Container ; rdf:type fedora:Resource ; rdf:type pcdm:Object ; rdf:type works:FileSet; rdf:type ldp:Container ; rdf:type ldp:RDFSource ; pcdm:hasFile ?file ; pcdm:memberOf ?parent . ?file rdf:type ldp:NonRDFSource ; rdf:type fedora:Binary ; rdf:type fedora:Resource ; rdf:type pcdm:File; pcdm:fileOf ?fileset; iana:describedby ?fcr ; ?predicate ?object }"


class contentFileset(Fileset):
    def __init__(self, sparqlData):
        self.sparqlData = sparqlData
        self.objectType = 'contentFileset'
        self.filterType = "content"
        super().__init__(self.sparqlData, self.objectType, self.filterType)
        self.construct = "CONSTRUCT { ?fileset rdf:type fedora:Container ; rdf:type fedora:Resource ; rdf:type pcdm:Object ; rdf:type works:FileSet; rdf:type ldp:Container ; rdf:type ldp:RDFSource ; pcdm:hasFile ?file ; pcdm:memberOf ?parent ; ?predicate ?object }"


class Thesis(Query):
    def __init__(self, sparqlData):
        self.objectType = 'thesis'
        self.construct = "CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ; dcterm:available ?available ; dcterm:accessRights ?visibility; rdf:type works:Work ; rdf:type pcdm:Object ; rdf:type bibo:Thesis; bibo:owner ?owner ; acl:embargoHistory ?history ; acl:visibilityAfterEmbargo ?visAfter"
        self.where = []
        self.select = "SELECT distinct ?resource WHERE { ?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type 'Thesis'^^xsd:string }"
        super().__init__(self.objectType, sparqlData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            where = "WHERE { ?resource info:hasModel 'GenericFile'^^xsd:string ; dcterm:type 'Thesis'^^xsd:string . FILTER (contains(str(?resource), '%s'))" % (self.splitBy[group])
            construct = self.construct
            for pair in self.mapping:
                construct = "%s ; <%s> ?%s" % (construct, pair[0], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
                where = " %s . OPTIONAL { ?resource <%s> ?%s . FILTER (str(?%s)!='') } " % (where, pair[1], re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')), re.sub(r'[0-9]+', '', pair[0].split('/')[-1].replace('#', '').replace('-', '')))
            self.queries[group] = "%s %s } %s . OPTIONAL {?permission webacl:accessTo ?resource ; webacl:mode webacl:Read ; webacl:agent ?visibility } . OPTIONAL {?permission webacl:accessTo ?resource ; webacl:mode webacl:Write ; webacl:agent ?owner } . OPTIONAL {?resource acl:hasEmbargo ?embargo . OPTIONAL {?embargo acl:embargoReleaseDate ?available } . OPTIONAL {?embargo acl:embargoHistory ?history } . OPTIONAL {?embargo acl:visibilityAfterEmbargo ?visAfter } }  . BIND(URI(replace(str(?resource), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/')) AS ?jupiterResource)}" % (self.prefixes, construct, where)
        self.writeQueries()


# ##  DATA TRANSPORT OBJECTS
# ##### Runs a query, sends data to get transformed, saves data to appropriate file


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
        self.directory = "results/%s/" % (self.objectType)
        self.filename = "results/%s/%s.nt" % (self.objectType, group)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def transformData(self):
        self.sparqlData.setReturnFormat(JSON)
        self.sparqlData.setQuery(self.q)
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


# ##  TRANSFORMATIONS
# #### functions for handling data passed over by the data object. Takes a triple, detects what kind of action needs to be taken based on the predicate, sends it to the appropriate function for transformations, then returns it back to the data handler to be saved.

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
            triple['object']['value'] = "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/%s/%s/%s/%s/%s" % (value[0:2], value[2:4], value[4:6], value[6:8], value)
            triple['object']['type'] = 'uri'
        self.output.append(triple)
        return self.output

    def modelshasMember(self, triple, objectType):
        if "http" not in triple['object']['value']:
            value = triple['object']['value']
            triple['object']['value'] = "http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/%s/%s/%s/%s/%s" % (value[0:2], value[2:4], value[4:6], value[6:8], value)
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
