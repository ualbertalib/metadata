from SPARQLWrapper import JSON, SPARQLWrapper
import re
from rdflib import URIRef, Literal, Graph
sparqlData = "http://localhost:9999/blazegraph/namespace/gillingham_20171222/sparql"
sparqlData = SPARQLWrapper(sparqlData)
sparqlData.setReturnFormat(JSON)
sparqlData.setQuery("select distinct ?s where {?s ?p ?o}")
r = sparqlData.query().convert()['results']['bindings']
i = 0
graph = Graph()
for re in r:
	i += 1
	if (i-1)%1000 == 0:
		graph.remove((None,None,None))
	print (i)
	sparqlData.setQuery("construct {<%s> ?p ?o} where {<%s> ?p ?o}" %(re['s']['value'], re['s']['value']))
	result = sparqlData.query().convert()['results']['bindings']
	for triple in result:
		p = URIRef(triple['predicate']['value'])
		s = URIRef(triple['subject']['value'])
		if triple['object']['type'] =='uri':
			o = URIRef(triple['object']['value'])
		else:
			 o = Literal(triple['object']['value'])
		if i%1000 != 0:
			graph.add((s, p, o))
		elif i%1000 == 0:
			graph.add((s, p, o))
			filename = 'terms/segment-' + str(i/1000) + '.nt'
			graph.serialize(destination=filename, format='nt')
			#graph = Graph()
graph.serialize(destination=filename, format='nt')
	
'''q = "PREFIX bg: <http://206.167.181.123:9999/blazegraph/namespace/terms/>  PREFIX premis: <http://www.loc.gov/premis/rdf/v1#>  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  PREFIX ual: <http://terms.library.ualberta.ca/>  PREFIX ualids: <http://terms.library.ualberta.ca/identifiers/>  PREFIX ualid: <http://terms.library.ualberta.ca/id/>  PREFIX ualdate: <http://terms.library.ualberta.ca/date/>  PREFIX ualrole: <http://terms.library.ualberta.ca/role/>  PREFIX ualthesis: <http://terms.library.ualberta.ca/thesis/>  PREFIX info: <info:fedora/fedora-system:def/model#>  PREFIX dcterm: <http://purl.org/dc/terms/>  PREFIX pcdm: <http://pcdm.org/models#>  PREFIX works: <http://pcdm.org/works#>  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  PREFIX fedora: <http://fedora.info/definitions/v4/repository#>  PREFIX iana: <http://www.iana.org/assignments/relation/>  PREFIX dc: <http://purl.org/dc/elements/1.1/>  PREFIX acl: <http://projecthydra.org/ns/auth/acl#>  PREFIX webacl: <http://www.w3.org/ns/auth/acl#>  PREFIX scholar: <http://scholarsphere.psu.edu/ns#>  PREFIX rels: <info:fedora/fedora-system:def/relations-external#>  PREFIX vivo: <http://vivoweb.org/ontology/core#>  PREFIX bibo: <http://purl.org/ontology/bibo/>  PREFIX mrels: <http://id.loc.gov/vocabulary/relators/>  PREFIX prism: <http://prismstandard.org/namespaces/basic/3.0/>  PREFIX cc: <http://creativecommons.org/ns#>  PREFIX fabio: <http://purl.org/spar/fabio/>  PREFIX lang: <http://id.loc.gov/vocabulary/iso639-2/>  PREFIX mrel: <http://id.loc.gov/vocabulary/relators/>  PREFIX naf: <http://id.loc.gov/authorities/names/>  PREFIX swrc: <http://ontoware.org/swrc/ontology#>  PREFIX schema: <http://schema.org/>  PREFIX ldp: <http://www.w3.org/ns/ldp#>  PREFIX use: <http://pcdm.org/use#>  PREFIX ebucore: <http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#>  PREFIX ore: <http://www.openarchives.org/ore/terms/> CONSTRUCT { ?resource info:hasModel 'Collection'^^xsd:string ; rdf:type pcdm:Collection ; ual:hydraNoid ?noid; dcterm:accessRights ?visibility ; <http://fedora.info/definitions/v4/repository#created> ?repositorycreated ; <http://fedora.info/definitions/v4/repository#primaryType> ?repositoryprimaryType ; <http://fedora.info/definitions/v4/repository#lastModifiedBy> ?repositorylastModifiedBy ; <http://fedora.info/definitions/v4/repository#hasParent> ?repositoryhasParent ; <http://fedora.info/definitions/v4/repository#writable> ?repositorywritable ; <http://fedora.info/definitions/v4/repository#mixinTypes> ?repositorymixinTypes ; <http://fedora.info/definitions/v4/repository#lastModified> ?repositorylastModified ; <info:fedora/fedora-system:def/model#createdDate> ?modelcreatedDate ; <http://fedora.info/definitions/v4/repository#uuid> ?repositoryuuid ; <http://fedora.info/definitions/v4/repository#exportsAs> ?repositoryexportsAs ; <http://fedora.info/definitions/v4/repository#createdBy> ?repositorycreatedBy ; <http://terms.library.ualberta.ca/depositor> ?depositor ; <http://pcdm.org/models#memberOf> ?modelsmemberOf ; <http://pcdm.org/models#memberOf> ?modelsmemberOf ; <http://pcdm.org/models#memberOf> ?modelsmemberOf ; <http://terms.library.ualberta.ca/fedora3UUID> ?fedoraUUID ; <http://terms.library.ualberta.ca/fedora3UUID> ?fedoraUUID ; <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?rdfsyntaxnstype ; <http://purl.org/dc/terms/description> ?description ; <http://purl.org/dc/terms/title> ?title ; <http://purl.org/dc/elements/1.1/creator> ?creator } WHERE { ?resource info:hasModel 'Collection'^^xsd:string . filter ( not exists { ?resource ualids:is_community 'true'^^xsd:string } ) filter ( not exists { ?resource ualid:is_community 'true'^^xsd:string } ) filter ( not exists { ?resource ual:is_community 'true'^^xsd:string } ) filter ( not exists { ?resource ualids:is_community 'true'^^xsd:boolean } ) filter ( not exists { ?resource ualid:is_community 'true'^^xsd:boolean } ) filter ( not exists { ?resource ual:is_community 'true'^^xsd:boolean } ) . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#created> ?repositorycreated} . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#primaryType> ?repositoryprimaryType } . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#lastModifiedBy> ?repositorylastModifiedBy } . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#hasParent> ?repositoryhasParent} . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#writable> ?repositorywritable} . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#mixinTypes> ?repositorymixinTypes} . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#lastModified> ?repositorylastModified} . OPTIONAL { ?resource <info:fedora/fedora-system:def/model#createdDate> ?modelcreatedDate} . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#uuid> ?repositoryuuid} . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#exportsAs> ?repositoryexportsAs} . OPTIONAL { ?resource <http://fedora.info/definitions/v4/repository#createdBy> ?repositorycreatedBy} . OPTIONAL { ?resource <http://id.loc.gov/vocabulary/relators/dpt> ?depositor} . OPTIONAL { ?resource <http://terms.library.ualberta.ca/id/belongsToCommunity> ?modelsmemberOf} . OPTIONAL { ?resource <http://terms.library.library.ca/identifiers/belongsToCommunity> ?modelsmemberOf} . OPTIONAL { ?resource <http://terms.library.ualberta.ca/identifiers/belongsToCommunity> ?modelsmemberOf} . OPTIONAL { ?resource <http://terms.library.ualberta.ca/id/fedora3uuid> ?fedoraUUID} . OPTIONAL { ?resource <http://terms.library.library.ca/identifiers/fedora3uuid> ?fedoraUUID} . OPTIONAL { ?resource <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?rdfsyntaxnstype} . OPTIONAL { ?resource <http://purl.org/dc/terms/description> ?description} . OPTIONAL { ?resource <http://purl.org/dc/terms/title> ?title} . OPTIONAL { ?resource <http://purl.org/dc/terms/creator> ?creator } . OPTIONAL { ?permission webacl:accessTo ?resource ; webacl:mode webacl:Read ; webacl:agent ?visibility } }"
sparqlData.setQuery(q)
r = sparqlData.query().convert()['results']['bindings']
graph = Graph()
for triple in r:
	p = URIRef(triple['predicate']['value'])
	s = URIRef(triple['subject']['value'])
	if triple['object']['type'] =='uri':
		o = URIRef(triple['object']['value'])
	else:
		 o = Literal(triple['object']['value'])
	graph.add((s, p, o))
graph.serialize(destination='col.nt', format='nt')


with open ('collections1.nt', 'a') as f:
	for re in r:
		f.write('<' + re['subject']['value'] + '> ')
		f.write('<' + re['predicate']['value'] + '> ')
		if re['object']['value'] != '':
			if re['object']['type'] == 'uri':
				f.write('<' + re['object']['value'].replace("\n", "").replace("'", "").replace('"', '') + '> ' + ' .' + "\n")
			else:
				f.write('"' + re['object']['value'].replace("\n", "").replace("'", "").replace('"', '')  + '"'+ ' .' + "\n")
		else:
			f.write('""' + " . \n")'''