# Jupiter Thesis Application Profile

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
### repeat  
 [dc:Rights](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:abstract](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsabstract) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
 [ual:commiteeMember](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualcommiteemember) *
 [ual:department](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepartment) *
 [ual:specialization](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualspecialization) *
 [ual:supervisor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualsupervisor) *
### sort  
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
### facet  
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
### display  
 [prism:doi](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:alternative](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsalternative) *
 [dcterms:identifier](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsidentifier) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [bibo:degree](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#bibodegree) *
 [ual:commiteeMember](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualcommiteemember) *
 [ual:department](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepartment) *
 [ual:dissertant](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdissertant) *
 [ual:graduationDate](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualgraduationdate) *
 [ual:institution](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualinstitution) *
 [ual:specialization](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualspecialization) *
 [ual:supervisor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualsupervisor) *
 [ual:thesisLevel](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualthesislevel) *
### required  
 [prism:doi](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi) *
 [dc:Rights](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:abstract](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsabstract) *
 [dcterms:dateAccepted](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdateaccepted) *
 [dcterms:dateSubmitted](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdatesubmitted) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
 [ual:commiteeMember](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualcommiteemember) *
 [ual:department](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepartment) *
 [ual:dissertant](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdissertant) *
 [ual:graduationDate](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualgraduationdate) *
 [ual:institution](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualinstitution) *
 [ual:specialization](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualspecialization) *
 [ual:supervisor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualsupervisor) *
 [prism:doi](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi) *
 [dc:Rights](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:abstract](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsabstract) *
 [dcterms:alternative](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsalternative) *
 [dcterms:dateAccepted](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdateaccepted) *
 [dcterms:dateSubmitted](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdatesubmitted) *
 [dcterms:identifier](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsidentifier) *
 [dcterms:isVersionOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsisversionof) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
 [bibo:degree](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#bibodegree) *
 [ual:commiteeMember](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualcommiteemember) *
 [ual:department](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepartment) *
 [ual:depositor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepositor) *
 [ual:dissertant](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdissertant) *
 [ual:fedora3Handle](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3handle) *
 [ual:fedora3UUID](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3uuid) *
 [ual:graduationDate](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualgraduationdate) *
 [ual:institution](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualinstitution) *
 [ual:proquest](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualproquest) *
 [ual:specialization](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualspecialization) *
 [ual:supervisor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualsupervisor) *
 [ual:thesisLevel](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualthesislevel) *
 [ual:unicorn](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualunicorn) *

# Profile by property

### prism:doi  
repeat: **false**  
displayLabel: **doi**  
onForm: **none**  
dataType: **auto**  
propertyName: **digital object identifier**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi**  
comments: **always doi (currently set to searchable (should this be changed?)**  
required: **true**  
sort: **false**  
### dc:Rights  
repeat: **true**  
displayLabel: **rights**  
onForm: **none**  
dataType: **text**  
propertyName: **rights**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights**  
required: **true**  
sort: **false**  
### dc:Subject  
repeat: **true**  
displayLabel: **subject/keyword**  
onForm: **none**  
dataType: **text**  
propertyName: **subject**  
facet: **true**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcubject**  
required: **true**  
sort: **false**  
### dcterms:abstract  
repeat: **true**  
displayLabel: **abstract**  
onForm: **none**  
dataType: **text**  
propertyName: **abstract**  
facet: **none**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsabstract**  
indexAs: **http://purl.org/dc/terms/description**  
required: **true**  
sort: **false**  
### dcterms:alternative  
repeat: **false**  
displayLabel: **none**  
onForm: **none**  
dataType: **text**  
propertyName: **alternative title**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsalternative**  
required: **false**  
sort: **false**  
### dcterms:dateAccepted  
repeat: **false**  
displayLabel: **none**  
onForm: **none**  
dataType: **auto**  
propertyName: **date accepted**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdateaccepted**  
required: **true**  
sort: **false**  
### dcterms:dateSubmitted  
repeat: **false**  
displayLabel: **none**  
onForm: **none**  
dataType: **auto**  
propertyName: **date submitted**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdatesubmitted**  
required: **true**  
sort: **false**  
### dcterms:identifier  
repeat: **false**  
displayLabel: **doi**  
onForm: **none**  
dataType: **text**  
propertyName: **identifier**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsidentifier**  
indexAs: **http://prismstandard.org/namespaces/basic/3.0/doi**  
comments: **often doi, but not always; currently set to searchable (should this be changed?)**  
required: **false**  
sort: **false**  
### dcterms:isVersionOf  
repeat: **false**  
displayLabel: **citation for previous publication**  
onForm: **none**  
dataType: **text**  
propertyName: **is version of**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsisversionof**  
required: **false**  
sort: **false**  
### dcterms:language  
repeat: **true**  
displayLabel: **language**  
onForm: **none**  
dataType: **uri**  
propertyName: **language**  
facet: **true**  
values displayed on form:  
  * **Ukranian** (http://id.loc.gov/vocabulary/iso639-2/ukr)  
  * **Japanese** (http://id.loc.gov/vocabulary/iso639-2/jpn)  
  * **German** (http://id.loc.gov/vocabulary/iso639-2/ger)  
  * **Other language** (http://terms.library.ualberta.ca/other)  
  * **Italian** (http://id.loc.gov/vocabulary/iso639-2/ita)  
  * **Russian** (http://id.loc.gov/vocabulary/iso639-2/rus)  
  * **No linguistic content** (http://id.loc.gov/vocabulary/iso639-2/zxx)  
  * **English** (http://id.loc.gov/vocabulary/iso639-2/eng)  
  * **French** (http://id.loc.gov/vocabulary/iso639-2/fre)  
  * **Portuguese** (http://id.loc.gov/vocabulary/iso639-2/por)  
  * **Chinese** (http://id.loc.gov/vocabulary/iso639-2/zho)  
  * **Vietnamese** (http://id.loc.gov/vocabulary/iso639-2/vie)  
  * **Inupiaq** (http://id.loc.gov/vocabulary/iso639-2/ipk)  
  * **Spanish** (http://id.loc.gov/vocabulary/iso639-2/spa)  

display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage**  
required: **true**  
sort: **false**  
### dcterms:title  
repeat: **false**  
displayLabel: **none**  
onForm: **none**  
dataType: **text**  
propertyName: **title**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle**  
required: **true**  
sort: **true**  
### dcterms:type  
repeat: **true**  
displayLabel: **type of item**  
onForm: **none**  
dataType: **uri**  
propertyName: **type**  
facet: **true**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype**  
required: **true**  
sort: **false**  
### bibo:degree  
repeat: **false**  
displayLabel: **degree**  
onForm: **none**  
dataType: **enumerated text**  
propertyName: **degree**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#bibodegree**  
required: **false**  
sort: **false**  
### ual:commiteeMember  
repeat: **true**  
displayLabel: **examining committee member and department**  
onForm: **none**  
dataType: **text**  
propertyName: **commitee member**  
facet: **none**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualcommiteeember**  
indexAs: **http://purl.org/dc/elements/1.1/Contributor**  
required: **true**  
sort: **none**  
### ual:department  
repeat: **true**  
displayLabel: **department**  
onForm: **none**  
dataType: **text**  
propertyName: **department**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepartment**  
required: **true**  
sort: **false**  
### ual:depositor  
repeat: **false**  
displayLabel: **none**  
onForm: **none**  
dataType: **auto**  
propertyName: **depositor**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepositor**  
comments: **legacy property; usage: admin email.**  
required: **false**  
sort: **false**  
### ual:dissertant  
repeat: **false**  
displayLabel: **author or creator**  
onForm: **none**  
dataType: **text**  
propertyName: **dissertant**  
facet: **none**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdissertant**  
indexAs: **http://purl.org/dc/elements/1.1/Creator**  
required: **true**  
sort: **none**  
### ual:fedora3Handle  
repeat: **false**  
displayLabel: **none**  
onForm: **none**  
dataType: **text**  
propertyName: **fedora 3 handle**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3handle**  
comments: **legacy property**  
required: **false**  
sort: **false**  
### ual:fedora3UUID  
repeat: **false**  
displayLabel: **none**  
onForm: **none**  
dataType: **text**  
propertyName: **fedora 3 uuid**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3uuid**  
comments: **legacy property**  
required: **false**  
sort: **false**  
### ual:graduationDate  
repeat: **false**  
displayLabel: **graduation date**  
onForm: **none**  
dataType: **auto**  
propertyName: **graduation date**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualgraduationdate**  
required: **true**  
sort: **false**  
### ual:institution  
repeat: **false**  
displayLabel: **degree grantor**  
onForm: **none**  
dataType: **auto**  
propertyName: **institution**  
facet: **false**  
values displayed on form:  
  * **University of Alberta** (http://id.loc.gov/authorities/names/n79058482)  

display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualinstitution**  
required: **true**  
sort: **false**  
### ual:proquest  
repeat: **false**  
displayLabel: **none**  
onForm: **none**  
dataType: **text**  
propertyName: **proquest**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualproquest**  
comments: **legacy property**  
required: **false**  
sort: **false**  
### ual:specialization  
repeat: **true**  
displayLabel: **specialization**  
onForm: **none**  
dataType: **text**  
propertyName: **specialization**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualspecialization**  
required: **true**  
sort: **false**  
### ual:supervisor  
repeat: **true**  
displayLabel: **supervisor and department**  
onForm: **none**  
dataType: **text**  
propertyName: **supervisor**  
facet: **none**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualsupervisor**  
indexAs: **http://purl.org/dc/elements/1.1/Contributor**  
required: **true**  
sort: **none**  
### ual:thesisLevel  
repeat: **false**  
displayLabel: **degree level**  
onForm: **none**  
dataType: **uri**  
propertyName: **thesis level**  
facet: **false**  
display: **true**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualthesislevel**  
required: **false**  
sort: **false**  
### ual:unicorn  
displayLabel: **none**  
onForm: **none**  
dataType: **text**  
propertyName: **unicorn**  
facet: **false**  
display: **false**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualunicorn**  
comments: **legacy property**  
required: **false**  
sort: **false**  
backwardCompatibleWith: **http://terms.library.ualberta.ca/id/unicorn**  
