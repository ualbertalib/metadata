from SPARQLWrapper import JSON, SPARQLWrapper, RDFXML, N3

project_folder_path = "/home/danydvd/git/remote/CanLink/code"      # for the server
# project_folder_path = "/Users/maharshmellow/Google Drive/Code/Github/CanLink/code"      # for local development
sparql = "http://206.167.181.124:7200/repositories/cldi-test-7"
dbp_sparql = "http://dbpedia.org/sparql/"
dbp_data = SPARQLWrapper(dbp_sparql)
dbp_data.setReturnFormat(JSON)
sparqlData = SPARQLWrapper(sparql)
sparqlData.setCredentials("admin", "4Metadata!")
sparqlData.setReturnFormat(JSON)
csh_sparql = "http://206.167.181.124:7200/repositories/CSH"
csh_sparqlData = SPARQLWrapper(csh_sparql)
csh_sparqlData.setCredentials("admin", "4Metadata!")
csh_sparqlData.setReturnFormat(JSON)

init_results_limit = 25

#name enrichment variables 
log_file = "error.log"
query_type = "/authorities/names"
apis = ['search_api_VFP', 'search_api_LC', 'search_api_LCS']

solr_base ='http://206.167.181.124:8983/solr/Canlink/select'
#solr_base ='http://206.167.181.124:8983/solr/CLDI-2/select'
solr_facet_limit = 15
solr_rows = 'rows=30000'
solr_sort_init = 'sort=score%20Desc'
solr_facet_fields = 'facet.field=creator_str&facet.field=subject_str&facet.field=degree&facet.field=lang_str&facet.field=institution_str'
solr_deg_map = {
	"msc": "MSc",
    "phd": "PhD",
    "med": "MEd",
    "ma": "MA",
    "master": "Master",
    "meng": "MEng",
    "mn": "MN",
    "llm": "LLM",
    "masc": "MASc",
    "msw": "MSW",
    "mba": "MBA",
    "mws": "MWS",
    "menv": "MEnv",
    "mphysed": "MPhysEd",
    "march": "MArch",
    "mfa": "MFA",
    "lld": "LLD",
    "mcoun": "MCoun",
    "mmath": "MMath",
    "dba": "DBA",
    "des": "Dec",
    "dsc": "DSc",
    "maed": "MAEd",
    "mdent": "MDent",
    "mdes": "MDes",
    "mhstud": "MHStud"
}

namespaces = {
	'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf:',
	'http://rdfs.org/ns/void#': 'rdfs:',
	'http://canlink.library.ualberta.ca/': 'canlink:',
	'http://www.w3.org/2002/07/owl#': 'owl:',
	'http://www.w3.org/ns/prov#': 'prov:',
	'http://dbpedia.org/resource/': 'dbpedia:',
	'http://id.loc.gov/vocabulary/relators/': 'rel:',
	'http://schema.org/': 'schema:',
	'http://purl.org/vocab/frbr/core#': 'frbr:',
	'http://sparql.cwrc.ca/ontologies/genre#': 'cwrc:',
	'http://xmlns.com/foaf/0.1/': 'foaf:',
	'http://purl.org/dc/terms/': 'dcterms:',
	'http://purl.org/ontology/bibo/': 'bibo:',
	'http://vivoweb.org/ontology/core#': 'vivo',
	'http://id.loc.gov/authorities/subjects/': 'lcsh:',
	'http://data.bnf.fr/ark:/': 'bnf:',
	'http://sparql.cwrc.ca/ontologies/genre#': 'cwrc:',
	'http://www.w3.org/ns/dcat#': 'dcat',
	'http://www.w3.org/2004/02/skos/core#': 'skos:',
	'http://rdfs.org/ns/void#': 'void:'
}