# Jupiter Collection Application Profile

The Jupiter Data Dictionary is a collection of living documents. Below you will find an application profile for properties implemented in production Jupiter. Changes to these variables can be suggested by submitting a Github ticket. The metadata team will edit the document accordingly.

# Namespaces  
**bibo:** http://purl.org/ontology/bibo/  
**cc:** http://creativecommons.org/ns#  
**dc:** http://purl.org/dc/elements/1.1/  
**dcterms:** http://purl.org/dc/terms/  
**ebu:** http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#  
**etd_ms:** http://www.ndltd.org/standards/metadata/etdms/1.0/  
**lang:** http://id.loc.gov/vocabulary/iso639-2/  
**mrel:** http://id.loc.gov/vocabulary/relators/  
**lcn:** http://id.loc.gov/authorities/names/  
**obo:** http://purl.obolibrary.org/obo/  
**owl:** http://www.w3.org/2002/07/owl#  
**ore:** http://www.openarchives.org/ore/terms/  
**pcdm:** http://pcdm.org/models#  
**prism:** http://prismstandard.org/namespaces/basic/3.0/  
**rdf:** http://www.w3.org/1999/02/22-rdf-syntax-ns#  
**rdfs:** http://www.w3.org/2000/01/rdf-schema#  
**schema:** http://schema.org/  
**scholar:** http://scholarsphere.psu.edu/ns#  
**skos:** http://www.w3.org/2004/02/skos/core#  
**status:** http://www.w3.org/2003/06/sw-vocab-status/ns#  
**swrc:** http://ontoware.org/swrc/ontology#  
**ual:** http://terms.library.ualberta.ca/  
**ualdate:** http://terms.library.ualberta.ca/date/  
**ualid:** http://terms.library.ualberta.ca/id/  
**ualids:** http://terms.library.ualberta.ca/identifiers/  
**ualrole:** http://terms.library.ualberta.ca/role/  
**ualthesis:** http://terms.library.ualberta.ca/thesis/  
**works:** http://pcdm.org/works#  
**vivo:** http://vivoweb.org/ontology/core#  

# Definitions

   **acceptedValue** values belonging to properties with restricted value parameters (only those displayed on form)  
   **backwardCompatibleWith** crosswalk to previously used terms (in ERA) for migration mapping  
   **comments** Jupiter specific instructions for using or questions about this property  
   **definedBy** a link to the Jupiter ontology, including a general description of the property  
   **dataType** the kinds of values permitted for use by the property: 'text', 'enumerated text' (i.e. non-URI drop-down), 'uri' (i.e. dropdown with URI), 'auto' (generated by application logic)  
   **display** does this property appear when an object is displayed to the user? (boolean)  
   **displayLabel** if this object is displayed to the user, what is the label used to describe the property in the display?  
   **facet** is this property faceted in SOLR? (boolean)  
   **indexAs** another property with which this property should be indexed in SOLR  
   **onForm** does this property appear on the form when a user creates a new resource? (boolean)  
   **propertyName** an informal name for describing the property  
   **repeat** can this property occur more than once? (boolean)  
   **required** is the property required to have a value? (boolean)  
   **search** is this property searchable in Jupiter? (boolean)  
   **sort** is this property sortable in SOLR? (boolean)  
   **tokenize** is this property tokenized in SOLR? (boolean)  

# Properties (Quick Find)
  * [memberOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#pcdmmemberof  )  
  * [creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dccreator  )  
  * [description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermsdescription  )  
  * [title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermstitle  )  
  * [depositor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#ualdepositor  )  
  * [fedora3UUID](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#ualfedora3uuid  )  
  * [hydraNoid](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#ualhydranoid  )  
  * [restrictedCollection](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#ualrestrictedcollection  )  
  * [dateIngested](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#ebudateingested  )  
  * [type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#rdftype  )  

# Profile by annotation
### backwardCompatibleWith  
  * [created](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedoracreated) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#created  
  * [createdBy](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedoracreatedby) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#createdBy  
  * [exportsAs](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedoraexportsas) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#exportsAs  
  * [hasParent](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedorahasparent) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#hasParent  
  * [lastModified](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedoralastmodified) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#lastModified  
  * [lastModifiedBy](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedoralastmodifiedby) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#lastModifiedBy  
  * [mixinTypes](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedoramixintypes) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#mixinTypes  
  * [primaryType](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedoraprimarytype) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#primaryType  
  * [uuid](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedorauuid) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#uuid  
  * [writable](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#fedorawritable) is backward compatible with:  
    * http://fedora.info/definitions/v4/repository#writable  
  * [memberOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#pcdmmemberof) is backward compatible with:  
    * http://terms.library.library.ca/identifiers/belongsToCommunity  
    * http://terms.library.ualberta.ca/identifiers/belongsToCommunity  
    * http://terms.library.ualberta.ca/id/belongsToCommunity  
  * [creator](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dccreator) is backward compatible with:  
    * http://purl.org/dc/terms/creator  
  * [description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermsdescription) is backward compatible with:  
    * http://purl.org/dc/terms/description  
  * [title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermstitle) is backward compatible with:  
    * http://purl.org/dc/terms/title  
  * [depositor](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#ualdepositor) is backward compatible with:  
    * http://id.loc.gov/vocabulary/relators/dpt  
  * [fedora3UUID](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#ualfedora3uuid) is backward compatible with:  
    * http://terms.library.library.ca/identifiers/fedora3uuid  
    * http://terms.library.ualberta.ca/id/fedora3uuid  
  * [type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#rdftype) is backward compatible with:  
    * http://www.w3.org/1999/02/22-rdf-syntax-ns#type  
  * [createdDate](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#infocreateddate) is backward compatible with:  
    * info:fedora/fedora-system:def/model#createdDate  
### display  
  * [memberOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#pcdmmemberof  )  
  * [description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermsdescription  )  
  * [title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermstitle  )  
### onForm  
  * [memberOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#pcdmmemberof  )  
  * [description](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermsdescription  )  
  * [title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermstitle  )  
### required  
  * [memberOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#pcdmmemberof  )  
  * [title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermstitle  )  
  * [type](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#rdftype  )  
### search  
  * [memberOf](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#pcdmmemberof  )  
  * [title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermstitle  )  
### sort  
  * [title](https://github.com/ualbertalib/metadata/tree/master/data_dictionary/profile_collection.md#dctermstitle  )  

# Profile by property

### fedora:created  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#created  
### fedora:createdBy  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#createdBy  
### fedora:exportsAs  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#exportsAs  
### fedora:hasParent  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#hasParent  
### fedora:lastModified  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#lastModified  
### fedora:lastModifiedBy  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#lastModifiedBy  
### fedora:mixinTypes  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#mixinTypes  
### fedora:primaryType  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#primaryType  
### fedora:uuid  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#uuid  
### fedora:writable  
  * backwardCompatibleWith:  
    * http://fedora.info/definitions/v4/repository#writable  
### pcdm:memberOf  
  * backwardCompatibleWith:  
    * http://terms.library.library.ca/identifiers/belongsToCommunity  
    * http://terms.library.ualberta.ca/identifiers/belongsToCommunity  
    * http://terms.library.ualberta.ca/id/belongsToCommunity  
  * comment:  
    * indicates community inheritence  
  * dataType:  
    * uri  
  * display:  
    * true  
  * facet:  
    * false  
  * onForm:  
    * true  
  * repeat:  
    * false  
  * required:  
    * true  
  * search:  
    * true  
  * sort:  
    * false  
### dc:creator  
  * backwardCompatibleWith:  
    * http://purl.org/dc/terms/creator  
  * dataType:  
    * text  
  * definedBy:  
    * https://github.com/ualbertalib/metadata/tree/master/data_dictionary/jupiter_ontology.md#dccreator  
  * display:  
    * false  
  * facet:  
    * false  
  * onForm:  
    * false  
  * propertyName:  
    * creator  
  * repeat:  
    * false  
  * required:  
    * false  
  * sort:  
    * false  
### dcterms:description  
  * backwardCompatibleWith:  
    * http://purl.org/dc/terms/description  
  * dataType:  
    * text  
  * definedBy:  
    * https://github.com/ualbertalib/metadata/tree/master/data_dictionary/jupiter_ontology.md#dctermsdescription  
  * display:  
    * true  
  * displayLabel:  
    * description  
  * facet:  
    * false  
  * onForm:  
    * true  
  * propertyName:  
    * description  
  * repeat:  
    * false  
  * required:  
    * false  
  * search:  
    * false  
  * sort:  
    * false  
### dcterms:title  
  * backwardCompatibleWith:  
    * http://purl.org/dc/terms/title  
  * comments:  
    * required for communties  
  * dataType:  
    * text  
  * definedBy:  
    * https://github.com/ualbertalib/metadata/tree/master/data_dictionary/jupiter_ontology.md#dctermstitle  
  * display:  
    * true  
  * displayLabel:  
    * title  
  * facet:  
    * false  
  * onForm:  
    * true  
  * propertyName:  
    * title  
  * repeat:  
    * false  
  * required:  
    * true  
  * search:  
    * true  
  * sort:  
    * true  
### ual:depositor  
  * backwardCompatibleWith:  
    * http://id.loc.gov/vocabulary/relators/dpt  
  * comments:  
    * legacy property; usage: admin email.  
  * dataType:  
    * auto  
  * definedBy:  
    * https://github.com/ualbertalib/metadata/tree/master/data_dictionary/jupiter_ontology.md#ualdepositor  
  * display:  
    * false  
  * facet:  
    * false  
  * onForm:  
    * false  
  * propertyName:  
    * depositor  
  * repeat:  
    * false  
  * required:  
    * false  
  * sort:  
    * false  
### ual:fedora3UUID  
  * backwardCompatibleWith:  
    * http://terms.library.library.ca/identifiers/fedora3uuid  
    * http://terms.library.ualberta.ca/id/fedora3uuid  
### ual:hydraNoid  
  * comments:  
    * hydra north legacy noid migrated through script  
  * repeat:  
    * false  
### ual:restrictedCollection  
  * comment:  
    * indicates if deposit into collection is restricted to admin only  
  * dataType:  
    * boolean  
  * display:  
    * false  
  * facet:  
    * false  
  * onForm:  
    * false  
  * propertyName:  
    * Restricted Collection  
  * repeat:  
    * false  
  * required:  
    * false  
  * search:  
    * false  
  * sort:  
    * false  
### ebu:dateIngested  
  * comments:  
    * backward compatible with http://fedora.info/definitions/v4/repository#created  
    * backward compatible with info:fedora/fedora-system:def/model#createdDate  
    * map first to info:createdDate. if not available, map next to fedora:created  
### rdf:type  
  * accepted value:  
    * **pcdm:Collection** (http://pcdm.org/models#Collection)  
  * values displayed on form:  
  * backwardCompatibleWith:  
    * http://www.w3.org/1999/02/22-rdf-syntax-ns#type  
  * dataType:  
    * auto  
  * propertyName:  
    * rdf Type  
  * required:  
    * true  
### info:createdDate  
  * backwardCompatibleWith:  
    * info:fedora/fedora-system:def/model#createdDate  
