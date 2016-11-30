from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import FOAF, RDFS, RDF, DCTERMS
g = Graph()
g.parse("con_hall.rdf")
mo = Namespace('http://purl.org/ontology/mo/') 
ua = Namespace('http://library.ualberta.ca/con_hall/') 
for person in g(mo.MusicArtist, FOAF.name, None):
    print(person)
