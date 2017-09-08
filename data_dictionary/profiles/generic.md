# Jupiter Generic Application Profile
   
The Jupiter Data Dictionary is a collection of living documents. Below you will find an application profile for properties implemented in production Jupiter. Changes to these variables can be suggested by submitting a Github ticket. The metadata team will edit the document accordingly.

# Namespaces
   
   **bibo:** http://purl.org/ontology/bibo/  
   
   **cc:** http://creativecommons.org/ns#  
   
   **dc:** http://purl.org/dc/elements/1.1/  
   
   **dcterms:** http://purl.org/dc/terms/  
   
   **eprints:** http://www.ukoln.ac.uk/repositories/digirep/index/Eprints_Type_Vocabulary_Encoding_Scheme#  
   
   **fabio:** http://purl.org/spar/fabio/  
   
   **foaf:** http://xmlns.com/foaf/0.1/  
   
   **geonames:** http://www.geonames.org/ontology#  
   
   **iana:** http://www.iana.org/assignments/media-types/  
   
   **lang:** http://id.loc.gov/vocabulary/iso639-2/  
   
   **mrel:** http://id.loc.gov/vocabulary/relators/  
   
   **naf:** http://id.loc.gov/authorities/names/  
   
   **obo:** http://purl.obolibrary.org/obo/  
   
   **pcdm:** http://pcdm.org/models#  
   
   **prism:** http://prismstandard.org/namespaces/basic/3.0/  
   
   **rdf:** http://www.w3.org/1999/02/22-rdf-syntax-ns#  
   
   **rdfs:** http://www.w3.org/2000/01/rdf-schema#  
   
   **skos:** http://www.w3.org/2004/02/skos/core#  
   
   **status:** http://www.w3.org/2003/06/sw-vocab-status/ns#  
   
   **owl:** http://www.w3.org/2002/07/owl#  
   
   **ore:** http://www.openarchives.org/ore/terms/  
   
   **tgn:** http://vocab.getty.edu/tgn/  
   
   **ual:** http://terms.library.ualberta.ca/  
   
   **vivo:** http://vivoweb.org/ontology/core#  
   
   **works:** http://pcdm.org/works#  
   
   **xsd:** http://www.w3.org/2001/XMLSchema#  
   
   
### prism:doi
   
 **http://terms.library.ualberta.ca/indexAs**: http://purl.org/dc/terms/identifier
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: auto
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: doi
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: digital object identifier
 **http://terms.library.ualberta.ca/comments**: always doi (currently set to searchable (should this be changed?)
   
### dc:Contributor
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccontributor
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: additional contributors
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: contributor
 **http://terms.library.ualberta.ca/comments**: 
   
### dc:Creator
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: author or creator
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: creator
 **http://terms.library.ualberta.ca/comments**: 
   
### dc:Rights
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: rights
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: rights
 **http://terms.library.ualberta.ca/comments**: cannot have both dc:license and dc:rights
   
### dc:Subject
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: subject/keyword
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: subject
 **http://terms.library.ualberta.ca/comments**: 
   
### dcterms:alternative
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsalternative
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: alternative title
 **http://terms.library.ualberta.ca/comments**: 
   
### dcterms:created
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermscreated
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: date created
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: date created
 **http://terms.library.ualberta.ca/comments**: 
   
### dcterms:description
   
 **http://terms.library.ualberta.ca/indexAs**: http://purl.org/dc/terms/abstract
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: description
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: description
 **http://terms.library.ualberta.ca/comments**: 
   
### dcterms:identifier
   
 **http://terms.library.ualberta.ca/indexAs**: http://prismstandard.org/namespaces/basic/3.0/doi
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsidentifier
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: doi
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: identifier
 **http://terms.library.ualberta.ca/comments**: often doi, but not always; currently set to searchable (should this be changed?)
   
### dcterms:isVersionOf
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsisversionof
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: citation for previous publication
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: is version of
 **http://terms.library.ualberta.ca/comments**: relation, source, and isversionof will eventually be mapped together (to some extent)
   
### dcterms:language
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/display**: true
 **acceptedValues** (on form): Ukranian (lang:ukr)
 **acceptedValues** (on form): Spanish (lang:spa)
 **acceptedValues** (on form): Italian (lang:ita)
 **acceptedValues** (on form): Inupiaq (lang:ipk)
 **acceptedValues** (on form): Chinese (lang:zho)
 **acceptedValues** (on form): Vietnamese (lang:vie)
 **acceptedValues** (on form): No linguistic content (lang:zxx)
 **acceptedValues** (on form): German (lang:ger)
 **acceptedValues** (on form): Portuguese (lang:por)
 **acceptedValues** (on form): French (lang:fre)
 **acceptedValues** (on form): English (lang:eng)
 **acceptedValues** (on form): Russian (lang:rus)
 **acceptedValues** (on form): Japanese (lang:jpn)
 **acceptedValues** (on form): Other language (ual:other)
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: uri
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: language
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: language
 **http://terms.library.ualberta.ca/comments**: 
   
### dcterms:license
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslicense
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/display**: true
 **acceptedValues** (on form): Attribution-NonCommercial 3.0 Unported (http://creativecommons.org/licenses/by-nc/3.0/)
 **acceptedValues** (on form): Attribution-ShareAlike 4.0 International (http://creativecommons.org/licenses/by-sa/4.0/)
 **acceptedValues** (on form): Attribution-NonCommercial-NoDerivs 3.0 Unported (http://creativecommons.org/licenses/by-nc-nd/3.0/)
 **acceptedValues** (on form): Attribution-NoDerivs 3.0 Unported (http://creativecommons.org/licenses/by-nd/3.0/)
 **acceptedValues** (on form): Attribution-NonCommercial 4.0 International (http://creativecommons.org/licenses/by-nc/4.0/)
 **acceptedValues** (on form): Public Domain Mark 1.0 (http://creativecommons.org/publicdomain/mark/1.0/)
 **acceptedValues** (on form): Attribution 3.0 Unported (http://creativecommons.org/licenses/by/3.0/)
 **acceptedValues** (on form): Attribution-ShareAlike 3.0 Unported (http://creativecommons.org/licenses/by-sa/3.0/)
 **acceptedValues** (on form): Attribution-NoDerivatives 4.0 International (http://creativecommons.org/licenses/by-nd/4.0/)
 **acceptedValues** (on form): Attribution-NonCommercial-NoDerivatives 4.0 International (http://creativecommons.org/licenses/by-nc-nd/4.0/)
 **acceptedValues** (on form): Attribution 4.0 International (http://creativecommons.org/licenses/by/4.0/)
 **acceptedValues** (on form): CC0 1.0 Universal (http://creativecommons.org/publicdomain/zero/1.0/)
 **acceptedValues** (on form): Attribution-NonCommercial-ShareAlike 3.0 Unported (http://creativecommons.org/licenses/by-nc-sa/3.0/)
 **acceptedValues** (on form): Attribution-NonCommercial-ShareAlike 4.0 International (http://creativecommons.org/licenses/by-nc-sa/4.0/)
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: uri
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: license information
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: license
 **http://terms.library.ualberta.ca/comments**: cannot have both dc:license and dc:rights
   
### dcterms:relation
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsrelation
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: link to related item
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: relation
 **http://terms.library.ualberta.ca/comments**: relation, source, and isversionof will eventually be mapped together (to some extent)
   
### dcterms:source
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: source
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: source
 **http://terms.library.ualberta.ca/comments**: relation, source, and isversionof will eventually be mapped together (to some extent)
   
### dcterms:spatial
   
 **http://terms.library.ualberta.ca/indexAs**: http://purl.org/dc/elements/1.1/Subject
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsspatial
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: place
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: spatial coverage
 **http://terms.library.ualberta.ca/comments**: 
   
### dcterms:temporal
   
 **http://terms.library.ualberta.ca/indexAs**: http://purl.org/dc/elements/1.1/Subject
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstemporal
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: time
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: temporal coverage
 **http://terms.library.ualberta.ca/comments**: 
   
### dcterms:title
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: title
 **http://terms.library.ualberta.ca/comments**: 
   
### dcterms:type
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: uri
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: type of item
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: type
 **http://terms.library.ualberta.ca/comments**: 
   
### bibo:status
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#bibostatus
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/display**: true
 **acceptedValues** (on form): accepted (bibo:status#accepted)
 **acceptedValues** (on form): published (bibo:status#published)
 **acceptedValues** (on form): draft (bibo:status#draft)
 **acceptedValues** (on form): unpublished (bibo:status#unpublished)
 **acceptedValues** (on form): submitted (vivo:submitted)
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: auto
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: type of item
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: status
 **http://terms.library.ualberta.ca/comments**: 'draft', 'submitted', 'published' to be selected and concatenated on the end of dc:type when dc:type is 'article'
   
### ual:ark
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualark
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: archival resource key id
 **http://terms.library.ualberta.ca/comments**: 
   
### ual:depositor
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepositor
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: auto
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: depositor
 **http://terms.library.ualberta.ca/comments**: legacy property; usage: admin email.
   
### ual:fedora3Handle
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3handle
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: fedora 3 handle
 **http://terms.library.ualberta.ca/comments**: legacy property
   
### ual:fedora3UUID
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3uuid
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: fedora 3 uuid
 **http://terms.library.ualberta.ca/comments**: legacy property
   
### ual:nnaFile
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualnnafile
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: northern north america filename
 **http://terms.library.ualberta.ca/comments**: legacy property
   
### ual:nnaItem
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualnnaitem
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: northern north america item id
 **http://terms.library.ualberta.ca/comments**: legacy property
   
### ual:unicorn
   
 **http://terms.library.ualberta.ca/indexAs**: 
 **http://terms.library.ualberta.ca/definedBy**: https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualunicorn
 **http://terms.library.ualberta.ca/display**: true
 **http://www.w3.org/1999/02/22-rdf-syntax-ns#type**: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
 **http://terms.library.ualberta.ca/tokenize**: 
 **http://terms.library.ualberta.ca/dataType**: text
 **http://terms.library.ualberta.ca/required**: true
 **http://terms.library.ualberta.ca/displayLabel**: none
 **http://terms.library.ualberta.ca/facet**: true
 **http://terms.library.ualberta.ca/sort**: true
 **http://terms.library.ualberta.ca/repeat**: true
 **http://terms.library.ualberta.ca/onForm**: true
 **http://terms.library.ualberta.ca/propertyName**: unicorn
 **http://terms.library.ualberta.ca/comments**: legacy property