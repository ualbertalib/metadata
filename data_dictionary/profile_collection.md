# Jupiter Collection Application Profile

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

# Definitions

   **@type** the object class. Particulary important for determining scope for use of terms and values.  
   **rdfs:comment** defines the term or property  
   **rdfs:domain** indicates terms (classes, values, datatypes, etc.) that may invoke a given property  
   **rdfs:range** indicates terms (classes, values, datatypes, etc.) that must be used with this property  
   **rdfs:label** the name of the term or property  
   **rdfs:preflabel** the label preferred for display  
   **owl:deprecated** indicates whether the property or term is active in the current deployment (default = false)  
   **owl:backwardCompatible** mappings to previous vocabularies used in previous deployments  
   **obo:IAO_0000112** usage example  
   **obo:IAO_0000115** description  

# Profile by annotation
### display  
 [dcterms:description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
### sort  
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
### onForm  
 [dcterms:description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
### required  
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [dc:Creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator) *
 [dcterms:description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [ual:depositor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepositor) *

# Profile by property

### dc:Creator  
display: **false**  
repeat: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator**  
onForm: **false**  
sort: **false**  
propertyName: **creator**  
dataType: **text**  
facet: **false**  
required: **false**  
displayLabel: **none**  
### dcterms:description  
display: **true**  
repeat: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription**  
onForm: **true**  
sort: **false**  
propertyName: **description**  
dataType: **text**  
facet: **false**  
required: **false**  
displayLabel: **description**  
### dcterms:title  
display: **true**  
repeat: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle**  
onForm: **true**  
sort: **true**  
comments: **required for communties**  
propertyName: **title**  
dataType: **text**  
facet: **false**  
required: **true**  
displayLabel: **title**  
### ual:depositor  
display: **false**  
repeat: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepositor**  
onForm: **false**  
sort: **false**  
comments: **legacy property; usage: admin email.**  
propertyName: **depositor**  
dataType: **auto**  
facet: **false**  
required: **false**  
displayLabel: **none**  
