import re
from Classes.Query import QueryBuilder


class Generic(QueryBuilder):
    def __init__(self, queryHelper):
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
        super().__init__(self.objectType, queryHelper.sparqlData)

    def generateQueries(self, uri_generator):
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