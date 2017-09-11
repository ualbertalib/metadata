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
### onForm  
 [dc:Contributor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccontributor) *
 [dc:Creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator) *
 [dc:Rights](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:created](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermscreated) *
 [dcterms:description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription) *
 [dcterms:isVersionOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsisversionof) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:license](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslicense) *
 [dcterms:relation](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsrelation) *
 [dcterms:source](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermssource) *
 [dcterms:spatial](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsspatial) *
 [dcterms:temporal](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstemporal) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
### sort  
 [dcterms:created](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermscreated) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
### repeat  
 [dc:Contributor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccontributor) *
 [dc:Creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:alternative](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsalternative) *
 [dcterms:identifier](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsidentifier) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:spatial](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsspatial) *
 [dcterms:temporal](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstemporal) *
 [bibo:status](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#bibostatus) *
### required  
 [prism:doi](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi) *
 [dc:Creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
 [ual:ark](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualark) *
### display  
 [prism:doi](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi) *
 [dc:Contributor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccontributor) *
 [dc:Creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator) *
 [dc:Rights](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:alternative](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsalternative) *
 [dcterms:created](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermscreated) *
 [dcterms:description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription) *
 [dcterms:identifier](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsidentifier) *
 [dcterms:isVersionOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsisversionof) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:license](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslicense) *
 [dcterms:relation](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsrelation) *
 [dcterms:source](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermssource) *
 [dcterms:spatial](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsspatial) *
 [dcterms:temporal](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstemporal) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
 [bibo:status](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#bibostatus) *
### facet  
 [dc:Contributor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccontributor) *
 [dc:Creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:license](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslicense) *
 [dcterms:spatial](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsspatial) *
 [dcterms:temporal](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstemporal) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
 [prism:doi](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi) *
 [dc:Contributor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccontributor) *
 [dc:Creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator) *
 [dc:Rights](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights) *
 [dc:Subject](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject) *
 [dcterms:alternative](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsalternative) *
 [dcterms:created](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermscreated) *
 [dcterms:description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription) *
 [dcterms:identifier](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsidentifier) *
 [dcterms:isVersionOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsisversionof) *
 [dcterms:language](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage) *
 [dcterms:license](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslicense) *
 [dcterms:relation](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsrelation) *
 [dcterms:source](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermssource) *
 [dcterms:spatial](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsspatial) *
 [dcterms:temporal](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstemporal) *
 [dcterms:title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle) *
 [dcterms:type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype) *
 [bibo:status](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#bibostatus) *
 [ual:ark](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualark) *
 [ual:depositor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepositor) *
 [ual:fedora3Handle](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3handle) *
 [ual:fedora3UUID](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3uuid) *
 [ual:nnaFile](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualnnafile) *
 [ual:nnaItem](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualnnaitem) *
 [ual:unicorn](https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualunicorn) *

# Profile by property

### prism:doi  
comments: **always doi (currently set to searchable (should this be changed?)**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#prismdoi**  
onForm: **false**  
dataType: **auto**  
sort: **false**  
displayLabel: **doi**  
repeat: **false**  
required: **true**  
display: **true**  
indexAs: **http://purl.org/dc/terms/identifier**  
facet: **false**  
propertyName: **digital object identifier**  
### dc:Contributor  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccontributor**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **additional contributors**  
repeat: **true**  
required: **false**  
display: **true**  
facet: **true**  
propertyName: **contributor**  
### dc:Creator  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dccreator**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **author or creator**  
repeat: **true**  
required: **true**  
display: **true**  
facet: **true**  
propertyName: **creator**  
### dc:Rights  
comments: **cannot have both dc:license and dc:rights**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcrights**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **rights**  
repeat: **false**  
required: **false**  
display: **true**  
facet: **false**  
propertyName: **rights**  
### dc:Subject  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dcsubject**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **subject/keyword**  
repeat: **true**  
required: **true**  
display: **true**  
facet: **true**  
propertyName: **subject**  
### dcterms:alternative  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsalternative**  
onForm: **false**  
dataType: **text**  
sort: **false**  
displayLabel: **none**  
repeat: **true**  
required: **false**  
display: **true**  
facet: **false**  
propertyName: **alternative title**  
### dcterms:created  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermscreated**  
onForm: **true**  
dataType: **text**  
sort: **true**  
displayLabel: **date created**  
repeat: **false**  
required: **false**  
display: **true**  
facet: **false**  
propertyName: **date created**  
### dcterms:description  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsdescription**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **description**  
repeat: **false**  
required: **false**  
display: **true**  
indexAs: **http://purl.org/dc/terms/abstract**  
facet: **false**  
propertyName: **description**  
### dcterms:identifier  
comments: **often doi, but not always; currently set to searchable (should this be changed?)**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsidentifier**  
onForm: **false**  
dataType: **text**  
sort: **false**  
displayLabel: **doi**  
repeat: **true**  
required: **false**  
display: **true**  
indexAs: **http://prismstandard.org/namespaces/basic/3.0/doi**  
facet: **false**  
propertyName: **identifier**  
### dcterms:isVersionOf  
comments: **relation, source, and isversionof will eventually be mapped together (to some extent)**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsisversionof**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **citation for previous publication**  
repeat: **false**  
required: **false**  
display: **true**  
facet: **false**  
propertyName: **is version of**  
### dcterms:language  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage**  
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

dataType: **uri**  
sort: **false**  
displayLabel: **language**  
repeat: **true**  
required: **true**  
display: **true**  
onForm: **true**  
facet: **true**  
propertyName: **language**  
### dcterms:license  
comments: **cannot have both dc:license and dc:rights**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslicense**  
values displayed on form:  
  * **Attribution 4.0 International** (http://creativecommons.org/licenses/by/4.0/)  
  * **Attribution-NonCommercial 3.0 Unported** (http://creativecommons.org/licenses/by-nc/3.0/)  
  * **Attribution-ShareAlike 4.0 International** (http://creativecommons.org/licenses/by-sa/4.0/)  
  * **Attribution-NonCommercial 4.0 International** (http://creativecommons.org/licenses/by-nc/4.0/)  
  * **Attribution-NoDerivs 3.0 Unported** (http://creativecommons.org/licenses/by-nd/3.0/)  
  * **Attribution 3.0 Unported** (http://creativecommons.org/licenses/by/3.0/)  
  * **Attribution-NonCommercial-NoDerivatives 4.0 International** (http://creativecommons.org/licenses/by-nc-nd/4.0/)  
  * **Attribution-ShareAlike 3.0 Unported** (http://creativecommons.org/licenses/by-sa/3.0/)  
  * **CC0 1.0 Universal** (http://creativecommons.org/publicdomain/zero/1.0/)  
  * **Attribution-NoDerivatives 4.0 International** (http://creativecommons.org/licenses/by-nd/4.0/)  
  * **Public Domain Mark 1.0** (http://creativecommons.org/publicdomain/mark/1.0/)  
  * **Attribution-NonCommercial-ShareAlike 3.0 Unported** (http://creativecommons.org/licenses/by-nc-sa/3.0/)  
  * **Attribution-NonCommercial-ShareAlike 4.0 International** (http://creativecommons.org/licenses/by-nc-sa/4.0/)  
  * **Attribution-NonCommercial-NoDerivs 3.0 Unported** (http://creativecommons.org/licenses/by-nc-nd/3.0/)  

dataType: **uri**  
sort: **false**  
displayLabel: **license information**  
repeat: **false**  
required: **false**  
display: **true**  
onForm: **true**  
facet: **true**  
propertyName: **license**  
### dcterms:relation  
comments: **relation, source, and isversionof will eventually be mapped together (to some extent)**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsrelation**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **link to related item**  
repeat: **false**  
required: **false**  
display: **true**  
facet: **false**  
propertyName: **relation**  
### dcterms:source  
comments: **relation, source, and isversionof will eventually be mapped together (to some extent)**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermslanguage**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **source**  
repeat: **false**  
required: **false**  
display: **true**  
facet: **false**  
propertyName: **source**  
### dcterms:spatial  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermsspatial**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **place**  
repeat: **true**  
required: **false**  
display: **true**  
indexAs: **http://purl.org/dc/elements/1.1/Subject**  
facet: **true**  
propertyName: **spatial coverage**  
### dcterms:temporal  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstemporal**  
onForm: **true**  
dataType: **text**  
sort: **false**  
displayLabel: **time**  
repeat: **true**  
required: **false**  
display: **true**  
indexAs: **http://purl.org/dc/elements/1.1/Subject**  
facet: **true**  
propertyName: **temporal coverage**  
### dcterms:title  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstitle**  
onForm: **true**  
dataType: **text**  
sort: **true**  
displayLabel: **none**  
repeat: **false**  
required: **true**  
display: **true**  
facet: **false**  
propertyName: **title**  
### dcterms:type  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#dctermstype**  
onForm: **true**  
dataType: **uri**  
sort: **false**  
displayLabel: **type of item**  
repeat: **false**  
required: **true**  
display: **true**  
facet: **true**  
propertyName: **type**  
### bibo:status  
comments: **'draft', 'submitted', 'published' to be selected and concatenated on the end of dc:type when dc:type is 'article'**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#bibostatus**  
values displayed on form:  
  * **unpublished** (http://purl.org/ontology/bibo/status#unpublished)  
  * **published** (http://purl.org/ontology/bibo/status#published)  
  * **draft** (http://purl.org/ontology/bibo/status#draft)  
  * **submitted** (http://vivoweb.org/ontology/core#submitted)  
  * **accepted** (http://purl.org/ontology/bibo/status#accepted)  

dataType: **auto**  
sort: **false**  
displayLabel: **type of item**  
repeat: **true**  
required: **false**  
display: **true**  
onForm: **false**  
facet: **false**  
propertyName: **status**  
### ual:ark  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualark**  
onForm: **false**  
dataType: **text**  
sort: **false**  
displayLabel: **none**  
repeat: **false**  
required: **true**  
display: **false**  
facet: **false**  
propertyName: **archival resource key id**  
### ual:depositor  
comments: **legacy property; usage: admin email.**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualdepositor**  
onForm: **false**  
dataType: **auto**  
sort: **false**  
displayLabel: **none**  
repeat: **false**  
required: **false**  
display: **false**  
facet: **false**  
propertyName: **depositor**  
### ual:fedora3Handle  
comments: **legacy property**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3handle**  
onForm: **false**  
dataType: **text**  
sort: **false**  
displayLabel: **none**  
repeat: **false**  
required: **false**  
display: **false**  
facet: **false**  
propertyName: **fedora 3 handle**  
### ual:fedora3UUID  
comments: **legacy property**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualfedora3uuid**  
onForm: **false**  
dataType: **text**  
sort: **false**  
displayLabel: **none**  
repeat: **false**  
required: **false**  
display: **false**  
facet: **false**  
propertyName: **fedora 3 uuid**  
### ual:nnaFile  
comments: **legacy property**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualnnafile**  
onForm: **false**  
dataType: **text**  
sort: **false**  
displayLabel: **none**  
repeat: **false**  
required: **false**  
display: **false**  
facet: **false**  
propertyName: **northern north america filename**  
### ual:nnaItem  
comments: **legacy property**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualnnaitem**  
onForm: **false**  
dataType: **text**  
sort: **false**  
displayLabel: **none**  
repeat: **false**  
required: **false**  
display: **false**  
facet: **false**  
propertyName: **northern north america item id**  
### ual:unicorn  
comments: **legacy property**  
definedBy: **https://github.com/ualbertalib/metadata/tree/master/data_dictionary#ualunicorn**  
onForm: **false**  
dataType: **text**  
sort: **false**  
displayLabel: **none**  
repeat: **false**  
required: **false**  
display: **false**  
facet: **false**  
propertyName: **unicorn**  
