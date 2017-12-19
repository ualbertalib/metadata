import re
import random
from tools import PrintException
from config import mig_ns
from SPARQLWrapper import JSON, SPARQLWrapper
import json


class QueryBuilder(object):
    """ Query objects are dynamically generated, and contain SPARQL CONSTRUCT queries with input from the jupiter application profile """
    def __init__(self, objectType, tripleStoreData):
        self.mapping = []
        self.objectType = objectType
        self.sparqlTerms = SPARQLWrapper(tripleStoreData.sparqlTerms)  # doesn't need to change (the terms store doesn't change)
        self.sparqlData = SPARQLWrapper(tripleStoreData.sparqlData)  # sets the triple store from which to get data (simple, test, or dev)
        self.sparqlTerms.setMethod("POST")
        self.sparqlData.setMethod("POST")
        self.queries = {}
        self.splitBy = {}
        self.prefixes = ""
        self.filename = ""
        for ns in mig_ns:
            self.prefixes = self.prefixes + " PREFIX {0}: <{1}> ".format(ns['prefix'], ns['uri'])
        self.getMappings()
        try:
            self.generateQueries()
        except Exception:
            PrintException()

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

    def writeQueries(self):
        for group in self.queries:
            for num, query in enumerate(self.queries[group]):
                self.queries[group][num]['construct'] = ' '.join(self.queries[group][num]['construct'].replace('\n', ' ').split())
                self.queries[group][num]['where'] = ' '.join(self.queries[group][num]['where'].replace('\n', ' ').split())
        filename = "cache/{0}.json".format(self.objectType)
        with open(filename, 'w+') as f:
            json.dump([self.queries], f, sort_keys=True, indent=4, separators=(',', ': '))


class Collection(QueryBuilder):
    def __init__(self, objectType, tripleStoreData):
        self.construct = """CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ; bibo:owner "eraadmi@ualberta.ca" ;
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
        super().__init__(objectType, tripleStoreData)

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


class Community(QueryBuilder):
    def __init__(self, objectType, tripleStoreData):
        self.construct = """CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ; bibo:owner "eraadmi@ualberta.ca" ;
            rdf:type pcdm:Object; rdf:type ual:Community; ual:hydraNoid ?noid; dcterm:accessRights ?visibility"""
        self.where = ["""WHERE { ?resource info:hasModel 'Collection'^^xsd:string ;
            OPTIONAL { ?resource ualids:is_community 'true'^^xsd:boolean } .
            OPTIONAL { ?resource ualid:is_community 'true'^^xsd:boolean } .
            OPTIONAL { ?resource ual:is_community 'true'^^xsd:boolean }"""]
        self.select = None
        super().__init__(objectType, tripleStoreData)

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


class Thesis(QueryBuilder):
    def __init__(self, objectType, tripleStoreData):
        self.construct = """CONSTRUCT {
            ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            rdf:type works:Work ;
            rdf:type pcdm:Object ;
            rdf:type bibo:Thesis;
            bibo:owner ?owner ;
            acl:embargoHistory ?history ;
            acl:visibilityAfterEmbargo ?visAfter ;
            dcterm:available ?available ;
            dcterm:accessRights ?accessRights;
            ual:hydraNoid ?noid"""
        self.where = []
        self.select = """SELECT distinct ?resource WHERE {
            ?resource info:hasModel 'GenericFile'^^xsd:string ;
            dcterm:type 'Thesis'^^xsd:string
        }"""
        super().__init__(objectType, tripleStoreData)

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


class Generic(QueryBuilder):
    def __init__(self, objectType, tripleStoreData):
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
        super().__init__(objectType, tripleStoreData)

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


class Related_Object(QueryBuilder):
    """ related members: content and characterization"""
    def __init__(self, objectType, tripleStoreData):
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
        super().__init__(objectType, tripleStoreData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = []
            for fileType in ['fedora3foxml', 'era1stats']:
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
                    BIND(URI(CONCAT(STR(?relatedObject), '/filesetID/files')) AS ?relatedFiles) .
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
                    BIND(URI(CONCAT(STR(?jupiterRelatedObject), '/filesetID')) AS ?relatedFileset) .
                    BIND(URI(CONCAT(str(?jupiterRelatedObject), '/proxy')) AS ?proxy) .
                    }}""".format(where, fileType, fileType)
            self.writeQueries()



class Technical(QueryBuilder):
    """ direct members: content and characterization"""
    def __init__(self, objectType, tripleStoreData):
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
        super().__init__(objectType, tripleStoreData)

    def generateQueries(self):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = []
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
                        BIND(URI(replace(replace(str(?directMember), 'http://gillingham.library.ualberta.ca:8080/fedora/rest/prod/', 'http://uat.library.ualberta.ca:8080/fcrepo/rest/uat/'), '{}', 'filesetID')) AS ?jupiterDirectFileset)
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
                        BIND(URI(replace(str(?jupiterDirectFileset), '/filesetID', '')) AS ?jupiterResource) .
                        BIND(URI(CONCAT(str(?jupiterResource), '/proxy')) AS ?proxy) .
                    }}""".format(where, fileType, fileType)
            self.writeQueries()
