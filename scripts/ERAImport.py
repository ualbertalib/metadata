"""Extracts descriptive metadata from ERA triplestore, converts and saves to NT format (or any other format of your choosing)"""

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, plugin
from rdflib.serializer import Serializer

predicates = {
    "type": "http://purl.org/dc/terms/type",
    "id": "http://purl.org/dc/terms/identifier",
    "title": "http://purl.org/dc/terms/title",
    "contributor": "http://purl.org/dc/terms/contributor",
    "creator": "http://purl.org/dc/terms/creator",
    "spatial": "http://purl.org/dc/terms/spatial",
    "temporal": "http://purl.org/dc/terms/temporal",
    "terms": "http://purl.org/dc/terms/subject",
    "date": "http://purl.org/dc/terms/created",
    "dissertant": "http://id.loc.gov/vocabulary/relators/dis",
    "dateAccepted": "http://purl.org/dc/terms/dateAccepted",
    "department": "http://vivoweb.org/ontology/core#AcademicDepartment",
    "degree": "http://purl.org/ontology/bibo/ThesisDegree",
    "specialization": "http://terms.library.ualberta.ca/thesis/specialization",
    "level": "http://terms.library.ualberta.ca/thesis/thesislevel",
    "supervisor": "http://id.loc.gov/vocabulary/relators/ths",
    "committee": "http://terms.library.ualberta.ca/role/thesiscommitteemember"
}

sparql = SPARQLWrapper("http://sheff.library.ualberta.ca:9999/blazegraph/namespace/fcrepo/sparql")
query = """prefix xsd: <http://www.w3.org/2001/XMLSchema#> SELECT * WHERE {?resource <info:fedora/fedora-system:def/model#hasModel> "GenericFile"^^xsd:string . OPTIONAL {?resource <http://purl.org/dc/terms/type> ?type } . OPTIONAL {?resource <http://purl.org/dc/terms/identifier> ?id } . OPTIONAL {?resource <http://purl.org/dc/terms/title> ?title } . OPTIONAL {?resource <http://purl.org/dc/terms/contributor> ?contributor } . OPTIONAL {?resource <http://purl.org/dc/terms/creator> ?creator } . OPTIONAL {?resource <http://purl.org/dc/terms/spatial> ?spatial } . OPTIONAL {?resource <http://purl.org/dc/terms/temporal> ?temporal } . OPTIONAL {?resource <http://purl.org/dc/terms/subject> ?terms } . OPTIONAL {?resource <http://purl.org/dc/terms/created> ?date } . OPTIONAL {?resource <http://id.loc.gov/vocabulary/relators/dis> ?dissertant } . OPTIONAL {?resource <http://purl.org/dc/terms/dateAccepted> ?dateAccepted } . OPTIONAL {?resource <http://vivoweb.org/ontology/core#AcademicDepartment> ?department } . OPTIONAL {?resource <http://purl.org/ontology/bibo/ThesisDegree> ?degree } . OPTIONAL {?resource <http://terms.library.ualberta.ca/thesis/specialization> ?specialization } . OPTIONAL {?resource <http://terms.library.ualberta.ca/thesis/thesislevel> ?level } . OPTIONAL {?resource <http://id.loc.gov/vocabulary/relators/ths> ?supervisor } . OPTIONAL {?resource <http://terms.library.ualberta.ca/role/thesiscommitteemember> ?committee} . OPTIONAL {?resource <http://terms.library.ualberta.ca/identifiers/hasCollection> ?collectionName} . } """
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

g = Graph()
for result in results["results"]["bindings"]:
    for key in predicates.keys():
        if key in result.keys() and result[key]['value'] is not '':
            g.add((URIRef(result['resource']['value']), URIRef(predicates[key]), Literal(str(result[key]['value']))))
g.serialize(destination='/home/zschoenb/Projects/ERAViz.json', format='json-ld', indent=4)
