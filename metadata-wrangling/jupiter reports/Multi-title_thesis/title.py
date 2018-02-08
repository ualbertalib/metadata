from SPARQLWrapper import JSON, SPARQLWrapper
import re
from rdflib import URIRef, Literal, Graph
sparqlData = "http://localhost:9999/blazegraph/namespace/gillingham_20171222/sparql"
sparqlData = SPARQLWrapper(sparqlData)
sparqlData.setReturnFormat(JSON)
sparqlData.setQuery("prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix dcterm: <http://purl.org/dc/terms/> prefix ualdate: <http://terms.library.ualberta.ca/date/> prefix ualid: <http://terms.library.ualberta.ca/identifiers/> prefix ulid: <http://terms.library.library.ca/identifiers/> select distinct ?s ?d ?e ?tt ?t where {?s <info:fedora/fedora-system:def/model#hasModel> 'GenericFile'^^xsd:string . ?s <http://id.loc.gov/vocabulary/relators/dis> ?d . ?s dcterm:title ?tt . ?s dcterm:type 'Thesis'^^xsd:string . ?s dcterm:alternative ?t . optional{?s ualid:year_created ?e . filter(xsd:integer(?e)<2009)} . optional{?s ulid:year_created ?e . filter(xsd:integer(?e)<2009)} . filter(str(?e) != '')}")
r = sparqlData.query().convert()['results']['bindings']
with open('pre-2009.tsv', 'w+') as o:
	o.write('NOID' + '\t' + 'Author' + '\t' + 'Title' + '\t' + 'Alternative title' + '\t' + 'Year' + '\t' + '\n')
	for triple in r:
		noid = triple['s']['value'].split('/')[-1]
		o.write(noid + '\t' + triple['d']['value'] + '\t' + triple['tt']['value'].replace('"', '').replace("'", "") + '\t' + triple['t']['value'].replace('"', '').replace("'", "") + '\t' + triple['e']['value'] + '\n')
o.close()
sparqlData.setQuery("prefix xsd: <http://www.w3.org/2001/XMLSchema#> prefix dcterm: <http://purl.org/dc/terms/> prefix ualdate: <http://terms.library.ualberta.ca/date/> prefix ualid: <http://terms.library.ualberta.ca/identifiers/> prefix ulid: <http://terms.library.library.ca/identifiers/> select distinct ?s ?d ?e ?tt ?t where {?s <info:fedora/fedora-system:def/model#hasModel> 'GenericFile'^^xsd:string . ?s <http://id.loc.gov/vocabulary/relators/dis> ?d . ?s dcterm:title ?tt . ?s dcterm:type 'Thesis'^^xsd:string . ?s dcterm:alternative ?t . optional{?s ualid:year_created ?e . filter(xsd:integer(?e)>=2009)} . optional{?s ulid:year_created ?e . filter(xsd:integer(?e)>=2009)} . filter(str(?e) != '')}")
r = sparqlData.query().convert()['results']['bindings']
with open('2009-present.tsv', 'w+') as o:
	o.write('NOID' + '\t' + 'Author' + '\t' + 'Title' + '\t' + 'Alternative title' + '\t' + 'Year' + '\t' + '\n')
	for triple in r:
		noid = triple['s']['value'].split('/')[-1]
		o.write(noid + '\t' + triple['d']['value'] + '\t' + triple['tt']['value'].replace('"', '').replace("'", "") + '\t' + triple['t']['value'].replace('"', '').replace("'", "") + '\t' + triple['e']['value'] + '\n')