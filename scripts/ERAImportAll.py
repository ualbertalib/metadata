"""Extracts descriptive metadata from ERA triplestore, converts and saves to NT format (or any other format of your choosing)"""

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal


def main():
    #genericPredicates = getPredicates('GenericFile')
    #collectionPredicates = getPredicates('Collection')
    #commit({'GenericFile': genericPredicates, 'Collection': collectionPredicates})
    retrieve()

def retrieve():
    sparql = SPARQLWrapper("http://sheff.library.ualberta.ca:9999/blazegraph/namespace/jupiter-test/sparql")
    
    with open('resources.txt') as f:
        for uri in f.readlines():
            query = "select (count(*) as ?count) where { <%s> ?b ?c}" % (uri.strip())
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            for result in results["results"]["bindings"]:
                for key in result.keys():
                    if int(result[key]['value'])<1:
                        print(uri.strip())

def getPredicates(model):
    sparql = SPARQLWrapper("http://sheff.library.ualberta.ca:9999/blazegraph/namespace/fcrepo/sparql")
    predicates = []
    query = "prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT DISTINCT ?predicate WHERE {?resource <info:fedora/fedora-system:def/model#hasModel> '%s'^^xsd:string . ?resource ?predicate ?object}" % (model)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        label = result['predicate']['value'].split('/')[-1].replace('#', '').replace('-', '')
        predicates.append((result['predicate']['value'], label))
    return predicates


def commit(predicates):
    sparql = SPARQLWrapper("http://sheff.library.ualberta.ca:9999/blazegraph/namespace/fcrepo/sparql")
    
    for key in predicates.keys():
        for predicate in predicates[key]:
            query = "prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT* WHERE {?resource <info:fedora/fedora-system:def/model#hasModel> \"%s\"^^xsd:string" % (key)
            query = query + " . ?resource <%s> ?%s }" % (predicate[0], predicate[1])
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            g = Graph()
            for result in results["results"]["bindings"]:
                if predicate[1] in result.keys() and result[predicate[1]]['value'] is not '':
                    g.add((URIRef(result['resource']['value']), URIRef(predicate[0]), Literal(str(result[predicate[1]]['value']))))
            g.serialize(destination='/home/zschoenb/Documents/nt/' + key + predicate[1] + '.nt', format='nt', indent=4)



# FILES=/home/zschoenb/Documents/nt/*
# for f in $FILES
# do
    # curl -H 'Content-Type: text/turtle' --upload-file $f -X POST "http://206.167.181.123:9999/blazegraph/namespace/jupiter-test/sparql"


if __name__ == "__main__":
    main()
