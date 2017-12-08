import random
import Classes.Helper as QueryHelper


class Technical(QueryHelper):
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

    def generateQueries(self, uri_generator):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = []
            filesetId = uri_generator.generatefileSetId()
            proxyId = uri_generator.generateProxyId(random.choice('0123456789ABCDEF') for i in range(16))
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