
from SPARQLWrapper import SPARQLWrapper, JSON

import sys

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
   PREFIX owl: <http://www.w3.org/2002/07/owl#>
   PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX quepy: <http://www.machinalis.com/quepy#>
    PREFIX dbpprop: <http://dbpedia.org/property/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    SELECT ?name ?birth ?death ?person WHERE {      ?person dbo:birthPlace :Berlin .      ?person dbo:birthDate ?birth .      ?person foaf:name ?name .      ?person dbo:deathDate ?death .      FILTER (?birth < "1900-01-01"^^xsd:date) . } ORDER BY ?name limit 10
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["name"]["value"])