# origin
sparqlTerms = "http://206.167.181.123:9999/blazegraph/namespace/terms/sparql"
sparqlData = "http://sheff.library.ualberta.ca:9999/blazegraph/namespace/gillingham_2/sparql"  # dev, 1 hour to transform
# sparqlData = "http://206.167.181.123:9999/blazegraph/namespace/radioactive/sparql"  # complex objects, 10 minute tranfsformation
# sparqlData = "http://206.167.181.123:9999/blazegraph/namespace/simple/sparql"  # one of each object type
# destination
sparqlResults = "http://206.167.181.123:9999/blazegraph/namespace/results/sparql"

# object types to transform (comment out those you wish to skip)
types = [
	#"collection",
	#"community",
	#"generic",
	#"thesis",
	#"file",
	"relatedObject"
	]

# prefix dictionary
mig_ns = [
	{"prefix": "premis", "uri": "http://www.loc.gov/premis/rdf/v1#"},
	{"prefix": "rdfs", "uri": "http://www.w3.org/2000/01/rdf-schema#"},
	{"prefix": "ual", "uri": "http://terms.library.ualberta.ca/"},
	{"prefix": "ualids", "uri": "http://terms.library.ualberta.ca/identifiers/"},
	{"prefix": "ualid", "uri": "http://terms.library.ualberta.ca/id/"},
	{"prefix": "ualdate", "uri": "http://terms.library.ualberta.ca/date/"},
	{"prefix": "ualrole", "uri": "http://terms.library.ualberta.ca/role/"},
	{"prefix": "ualthesis", "uri": "http://terms.library.ualberta.ca/thesis/"},
	{"prefix": "info", "uri": "info:fedora/fedora-system:def/model#"},
	{"prefix": "dcterm", "uri": "http://purl.org/dc/terms/"},
	{"prefix": "pcdm", "uri": "http://pcdm.org/models#"},
	{"prefix": "works", "uri": "http://pcdm.org/works#"},
	{"prefix": "rdf", "uri": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"},
	{"prefix": "fedora", "uri": "http://fedora.info/definitions/v4/repository#"},
	{"prefix": "iana", "uri": "http://www.iana.org/assignments/relation/"},
	{"prefix": "dc", "uri": "http://purl.org/dc/elements/1.1/"},
	{"prefix": "acl", "uri": "http://projecthydra.org/ns/auth/acl#"},
	{"prefix": "webacl", "uri": "http://www.w3.org/ns/auth/acl#"},
	{"prefix": "scholar", "uri": "http://scholarsphere.psu.edu/ns#"},
	{"prefix": "rels", "uri": "info:fedora/fedora-system:def/relations-external#"},
	{"prefix": "vivo", "uri": "http://vivoweb.org/ontology/core#"},
	{"prefix": "bibo", "uri": "http://purl.org/ontology/bibo/"},
	{"prefix": "mrels", "uri": "http://id.loc.gov/vocabulary/relators/"},
	{"prefix": "prism", "uri": "http://prismstandard.org/namespaces/basic/3.0/"},
	{"prefix": "cc", "uri": "http://creativecommons.org/ns#"},
	{"prefix": "fabio", "uri": "http://purl.org/spar/fabio/"},
	{"prefix": "lang", "uri": "http://id.loc.gov/vocabulary/iso639-2/"},
	{"prefix": "mrel", "uri": "http://id.loc.gov/vocabulary/relators/"},
	{"prefix": "naf", "uri": "http://id.loc.gov/authorities/names/"},
	{"prefix": "swrc", "uri": "http://ontoware.org/swrc/ontology#"},
	{"prefix": "schema", "uri": "http://schema.org/"},
	{"prefix": "ldp", "uri": "http://www.w3.org/ns/ldp#"},
	{"prefix": "use", "uri": "http://pcdm.org/use#"},
	{"prefix": "ebucore", "uri": "http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#"},
	{"prefix": "ore", "uri": "http://www.openarchives.org/ore/terms/"},
]

# transformation mappings
vocabs = {
	"language": [
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/ukr",
			"mapping": ["Ukrainian"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/jpn",
			"mapping": ["Japanese"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/ger",
			"mapping": ["German"]
		},
		{
			"uri": "http://terms.library.ualberta.ca/other",
			"mapping": ["other", "Other"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/ita",
			"mapping": ["Italian"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/rus",
			"mapping": ["Russian"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/zxx",
			"mapping": ["No linguistic content", "No liguistic content"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/eng",
			"mapping": ["English", "english"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/fre",
			"mapping": ["French"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/por",
			"mapping": ["Portuguese"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/zho",
			"mapping": ["Chinese"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/vie",
			"mapping": []
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/ipk",
			"mapping": ["Inupiaq"]
		},
		{
			"uri": "http://id.loc.gov/vocabulary/iso639-2/spa",
			"mapping": ["Spanish", "spanish"]
		}
	],
	"license": [
		{
			"uri": "http://creativecommons.org/licenses/by/4.0/",
			"mapping": ["Creative Commons Attribution License", "Attribution 4.0 International", "http://creativecommons.org/licenses/by/4.0/"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-nc/3.0/",
			"mapping": ["Creative Commons Attribution-Non-Commercial 3.0 Unported"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-sa/4.0/",
			"mapping": ["Creative Commons Attribution-ShareAlike 4.0 International", "http://creativecommons.org/licenses/by-sa/4.0/", "Attribution-ShareAlike 4.0 International"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-nc/4.0/",
			"mapping": ["Attribution-NonCommercial 4.0 International", "http://creativecommons.org/licenses/by-nc/4.0/"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by/3.0/",
			"mapping": ["Attribution 3.0 International", "Creative Commons Attribution 3.0 Unported"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-nc-nd/4.0/",
			"mapping": ["http://creativecommons.org/licenses/by-nc-nd/4.0/", "Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International", "Attribution-NonCommercial-NoDerivatives 4.0 International", "Attribution-NonCommercial-NoDervis 4.0 International", "Attribution-non-commercial-No-Derivs 4.0 International", "Attribution-NonCommerical-NoDerivs 4.0 International"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-sa/3.0/",
			"mapping": ["Creative Commons Attribution-ShareAlike 3.0 Unported"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-nd/4.0/",
			"mapping": ["Creative Commons Attribution-NoDerivs 4.0 International", "http://creativecommons.org/licenses/by-nd/4.0/"]
		},
		{
			"uri": "http://creativecommons.org/publicdomain/mark/1.0/",
			"mapping": ["http://creativecommons.org/publicdomain/mark/1.0/"]
		},
		{
			"uri": "http://creativecommons.org/publicdomain/zero/1.0/",
			"mapping": ["http://creativecommons.org/publicdomain/zero/1.0/", "CC0 1.0 Universal"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
			"mapping": ["http://creativecommons.org/licenses/by-nc-sa/4.0/"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-nc-nd/3.0/",
			"mapping": ["Creative Commons Attribution-Non-Commercial-No Derivatives 3.0 Unported"]
		},
		{
			"uri": "http://creativecommons.org/licenses/by-nc-sa/2.5/ca/",
			"mapping": ["Creative Commons Attribution-NonCommercial-ShareAlike 2.5 Canada"]
		}
	],
	"type": [
		{
			"uri": "http://purl.org/ontology/bibo/Article",
			"mapping": ["Journal Article (Published)", "Journal Article (Draft-Submitted)"]
		},
		{
			"uri": "http://purl.org/ontology/bibo/Book",
			"mapping": ["Book"]
		},
		{
			"uri": "http://purl.org/ontology/bibo/Chapter",
			"mapping": ["Book Chapter"]
		},
		{
			"uri": "http://purl.org/ontology/bibo/Image",
			"mapping": ["Image"]
		},
		{
			"uri": "http://purl.org/ontology/bibo/Report",
			"mapping": ["Report", "Computing Science Technical Report", "Structural Engineering Report"]
		},
		{
			"uri": "http://terms.library.ualberta.ca/researchMaterial",
			"mapping": ["Research Material"]
		},
		{
			"uri": "http://vivoweb.org/ontology/core#ConferencePaper",
			"mapping": ["Conference/workshop Presentation"]
		},
		{
			"uri": "http://vivoweb.org/ontology/core#ConferencePoster",
			"mapping": ["Conference/workshop Poster"]
		},
		{
			"uri": "http://vivoweb.org/ontology/core#Dataset",
			"mapping": ["Dataset"]
		},
		{
			"uri": "http://vivoweb.org/ontology/core#Review",
			"mapping": ["Review"]
		},
		{
			"uri": "http://terms.library.ualberta.ca/learningObject",
			"mapping": ["Learning Object"]
		}
	],
	"thesisLevel":
	[
		{
			"uri": "http://purl.org/spar/fabio/MastersThesis",
			"mapping": ["Master's", "Master"]
		},
		{
			"uri": "http://purl.org/spar/fabio/DoctoralThesis",
			"mapping": ["Doctoral"]
		}
	]
}
