

class QueryHelper(object):
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
            self.generateQueries(uri_generator)
        except Exception:
            PrintException()

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