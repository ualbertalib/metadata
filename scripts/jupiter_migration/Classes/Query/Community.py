import re
from Classes.Query import QueryBuilder

class Community(QueryBuilder):
    def __init__(self, queryHelper):
        self.objectType = 'community'
        self.construct = """CONSTRUCT { ?jupiterResource info:hasModel 'IRItem'^^xsd:string ;
            rdf:type pcdm:Object; rdf:type ual:Community; ual:hydraNoid ?noid; dcterm:accessRights ?visibility"""
        self.where = ["""WHERE { ?resource info:hasModel 'Collection'^^xsd:string ;
            OPTIONAL { ?resource ualids:is_community 'true'^^xsd:boolean } .
            OPTIONAL { ?resource ualid:is_community 'true'^^xsd:boolean } .
            OPTIONAL { ?resource ual:is_community 'true'^^xsd:boolean }"""]
        self.select = None
        super().__init__(self.objectType, queryHelper.sparqlData)

    def generateQueries(self, uri_generator):
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
