import random
import Classes.Helper as QueryHelper


class Related_Object(QueryHelper):
    """ related members: content and characterization"""
    def __init__(self, queryHelper):
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
        super().__init__(self.objectType, queryHelper.sparqlData)

    def generateQueries(self, uri_generator):
        self.getSplitBy()
        for group in self.splitBy.keys():
            self.queries[group] = []
            for fileType in ['fedora3foxml', 'era1stats']:
                filesetId = uri_generator.generatefileSetId()
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
                    }}""".format(where, fileType, fileType, filesetId, uri_generator.generateProxyId(random.choice('0123456789ABCDEF') for i in range(16)))
            self.writeQueries()
