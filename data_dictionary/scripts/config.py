namespaces = [
	{"prefix": "bibo", "uri": "http://purl.org/ontology/bibo/"},
	{"prefix": "cc", "uri": "http://creativecommons.org/ns#"},
	{"prefix": "dc", "uri": "http://purl.org/dc/elements/1.1/"},
	{"prefix": "dcterms", "uri": "http://purl.org/dc/terms/"},
	{"prefix": "eprints", "uri": "http://www.ukoln.ac.uk/repositories/digirep/index/Eprints_Type_Vocabulary_Encoding_Scheme#"},
	{"prefix": "fabio", "uri": "http://purl.org/spar/fabio/"},
	{"prefix": "foaf", "uri": "http://xmlns.com/foaf/0.1/"},
	{"prefix": "geonames", "uri": "http://www.geonames.org/ontology#"},
	{"prefix": "iana", "uri": "http://www.iana.org/assignments/media-types/"},
	{"prefix": "lang", "uri": "http://id.loc.gov/vocabulary/iso639-2/"},
	{"prefix": "mrel", "uri": "http://id.loc.gov/vocabulary/relators/"},
	{"prefix": "naf", "uri": "http://id.loc.gov/authorities/names/"},
	{"prefix": "obo", "uri": "http://purl.obolibrary.org/obo/"},
	{"prefix": "pcdm", "uri": "http://pcdm.org/models#"},
	{"prefix": "prism", "uri": "http://prismstandard.org/namespaces/basic/3.0/"},
	{"prefix": "rdf", "uri": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"},
	{"prefix": "rdfs", "uri": "http://www.w3.org/2000/01/rdf-schema#"},
	{"prefix": "skos", "uri": "http://www.w3.org/2004/02/skos/core#"},
	{"prefix": "status", "uri": "http://www.w3.org/2003/06/sw-vocab-status/ns#"},
	{"prefix": "owl", "uri": "http://www.w3.org/2002/07/owl#"},
	{"prefix": "ore", "uri": "http://www.openarchives.org/ore/terms/"},
	{"prefix": "tgn", "uri": "http://vocab.getty.edu/tgn/"},
	{"prefix": "ual", "uri": "http://terms.library.ualberta.ca/"},
	{"prefix": "vivo", "uri": "http://vivoweb.org/ontology/core#"},
	{"prefix": "works", "uri": "http://pcdm.org/works#"},
	{"prefix": "xsd", "uri": "http://www.w3.org/2001/XMLSchema#"}
]

definitions = [
	{"term": "@type", "def": "the object class. Particulary important for determining scope for use of terms and values."},
	{"term": "rdfs:comment", "def": "defines the term or property"},
	{"term": "rdfs:domain", "def": "indicates terms (classes, values, datatypes, etc.) that may invoke a given property"},
	{"term": "rdfs:range", "def": "indicates terms (classes, values, datatypes, etc.) that must be used with this property"},
	{"term": "rdfs:label", "def": "the name of the term or property"},
	{"term": "rdfs:preflabel", "def": "the label preferred for display"},
	{"term": "owl:deprecated", "def": "indicates whether the property or term is active in the current deployment (default = false)"},
	{"term": "owl:backwardCompatible", "def": "mappings to previous vocabularies used in previous deployments"},
	{"term": "obo:IAO_0000112", "def": "usage example"},
	{"term": "obo:IAO_0000115", "def": "description"}
]

ddWelcome = ' The Jupiter Data Dictionary is a collection of living documents. Below you will find the Juputiter ontology -- definitions for properties (predicates), terms (vocabulary or classes), and values (instances) used in the Jupiter project.  See [application profiles](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profiles)  for current deployment specifications in Jupiter. Changes to any of these documents can be suggested by submitting a Github issue. The metadata team will update the document accordingly. FYI: markdown files are accompanied by json files that may also be consulted.'

profileWelcome = 'The Jupiter Data Dictionary is a collection of living documents. Below you will find an application profile for properties implemented in production Jupiter. Changes to these variables can be suggested by submitting a Github ticket. The metadata team will edit the document accordingly.'