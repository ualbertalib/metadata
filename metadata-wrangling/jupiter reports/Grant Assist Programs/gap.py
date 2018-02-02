from SPARQLWrapper import JSON, SPARQLWrapper
import re
sparqlData = "http://localhost:9999/blazegraph/namespace/gillingham_20171222/sparql"
sparqlData = SPARQLWrapper(sparqlData)
for comm in ['44558r03c', '44558r50r', '44558r821']:
	print ("starting " + comm)
	q = "prefix info: <info:fedora/fedora-system:def/model#> prefix dcterm: <http://purl.org/dc/terms/>select distinct ?resource where {?resource info:hasModel 'GenericFile'^^xsd:string . ?resource <http://terms.library.ualberta.ca/identifiers/belongsToCommunity> ?community . optional {?resource <http://terms.library.ualberta.ca/identifiers/hasCollection> ?collection} . filter (exists {?read <http://www.w3.org/ns/auth/acl#accessTo> ?resource . ?read <http://www.w3.org/ns/auth/acl#mode> <http://www.w3.org/ns/auth/acl#Read>} && ?community = '%s')}" %(comm)
	with open(comm + '.tsv', 'a') as out:
		with open('gap_properties.txt', 'r') as file:
			out.write("resource" + "\t" + "Community" + "\t")
			for line in file:
				line = line.replace('\n', '').replace('<', '').replace('>', '')
				out.write(line + "\t")
			out.write("\n")
			file.close()
			print ("predicates for " + comm + " are done")
		sparqlData.setReturnFormat(JSON)
		sparqlData.setQuery(q) 
		r = sparqlData.query().convert()
		for re in r['results']['bindings']:
			resource = '<' + re['resource']['value'].replace('\n', '') + '>'
			print ("starting queries for " + resource)
			report = []
			with open('gap_properties.txt', 'r') as file:
				for predicate in file:
					predicate = predicate.replace('\n', '')
					query = "PREFIX bg: <http://206.167.181.123:9999/blazegraph/namespace/terms/>  PREFIX premis: <http://www.loc.gov/premis/rdf/v1#>  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>  PREFIX ual: <http://terms.library.ualberta.ca/>  PREFIX ualId: <http://terms.library.library.ca/identifiers/>  PREFIX ualids: <http://terms.library.ualberta.ca/id/> PREFIX ualid: <http://terms.library.ualberta.ca/identifiers/>  PREFIX ualdate: <http://terms.library.ualberta.ca/date/>  PREFIX ualrole: <http://terms.library.ualberta.ca/role/>  PREFIX ualthesis: <http://terms.library.ualberta.ca/thesis/>  PREFIX info: <info:fedora/fedora-system:def/model#>  PREFIX dcterm: <http://purl.org/dc/terms/>  PREFIX pcdm: <http://pcdm.org/models#>  PREFIX works: <http://pcdm.org/works#>  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  PREFIX fedora: <http://fedora.info/definitions/v4/repository#>  PREFIX iana: <http://www.iana.org/assignments/relation/>  PREFIX dc: <http://purl.org/dc/elements/1.1/>  PREFIX acl: <http://projecthydra.org/ns/auth/acl#>  PREFIX webacl: <http://www.w3.org/ns/auth/acl#>  PREFIX scholar: <http://scholarsphere.psu.edu/ns#>  PREFIX rels: <info:fedora/fedora-system:def/relations-external#>  PREFIX vivo: <http://vivoweb.org/ontology/core#>  PREFIX bibo: <http://purl.org/ontology/bibo/>  PREFIX mrels: <http://id.loc.gov/vocabulary/relators/>  PREFIX prism: <http://prismstandard.org/namespaces/basic/3.0/>  PREFIX cc: <http://creativecommons.org/ns#>  PREFIX fabio: <http://purl.org/spar/fabio/>  PREFIX lang: <http://id.loc.gov/vocabulary/iso639-2/>  PREFIX mrel: <http://id.loc.gov/vocabulary/relators/>  PREFIX naf: <http://id.loc.gov/authorities/names/>  PREFIX swrc: <http://ontoware.org/swrc/ontology#>  PREFIX schema: <http://schema.org/>  PREFIX ldp: <http://www.w3.org/ns/ldp#>  PREFIX use: <http://pcdm.org/use#>  PREFIX ebucore: <http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#>  PREFIX ore: <http://www.openarchives.org/ore/terms/> select ?p where {%s %s ?p}" %(resource, predicate)
					sparqlData.setReturnFormat(JSON)
					sparqlData.setQuery(query) 
					results = sparqlData.query().convert()
					if not results['results']['bindings']:
						report.append({'subject' : resource, 'predicate' : predicate, 'object': 'N/A'})	
					else:
						'''if predicate == '<http://terms.library.ualberta.ca/identifiers/hasCollectionId>' or predicate == '<http://terms.library.library.ca/identifiers/hasCollectionId>':'''
						for result in results['results']['bindings']:
							flag = "F"
							for i in report:
								if i['subject'] == resource and i['predicate'] == predicate:
									flag = "T"
									i['object'] = str(i['object']) + " | " + str(result['p']['value'].rstrip().replace('\n', '').replace("'", ""))
								else:
									continue
							if flag == "F":
								report.append({'subject' : resource, 'predicate' : predicate, 'object': str(result['p']['value']).rstrip().replace('\n', '').replace("'", "").replace('"', '').replace("\t", "")})
			print (resource + " queries done")
			out.write(report[0]['subject'] + "\t")
			if comm == '44558r03c':
				out.write('Grant Assist Program (Social Sciences / Humanities)' + "\t")
			if comm =='44558r821':
				out.write('	Grant Assist Program (Health Sciences)' + "\t")
			if comm == '44558r50r':
				out.write('	Grant Assist Program (Natural Sciences and Engineering)' + "\t")
			for i in report:
				if i['object'] != '':
					string = ""
					for j in i['object'].split('\n'):
						string = string + j.rstrip('\n').replace('\n', '').replace('\t', '').replace('\r', '')
					out.write(string + "\t")
				else:
					out.write("N/A" + "\t")
			out.write("\n")