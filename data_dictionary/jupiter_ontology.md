# Jupiter Data Dictionary

The Jupiter Data Dictionary is a collection of living documents. Below you will find the Jupiter ontology -- definitions for properties (predicates), terms (vocabulary or classes), and values (instances) used in the Jupiter project.  Current deployment specifications in Jupiter are described by application profiles. Changes to any of these documents can be suggested by submitting a Github issue. The metadata team will update the document accordingly. FYI: markdown files are accompanied by json files that may also be consulted.
# Namespaces

   **acl:** http://projecthydra.org/ns/auth/acl#  
   **bibo:** http://purl.org/ontology/bibo/  
   **cc:** http://creativecommons.org/ns#  
   **dc:** http://purl.org/dc/elements/1.1/  
   **dcterms:** http://purl.org/dc/terms/  
   **ebu:** http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#  
   **etd_ms:** http://www.ndltd.org/standards/metadata/etdms/1.0/  
   **fedora:** http://fedora.info/definitions/v4/repository#  
   **iana:** http://www.iana.org/assignments/media-types/  
   **info:** info:fedora/fedora-system:def/model#  
   **lang:** http://id.loc.gov/vocabulary/iso639-2/  
   **mrel:** http://id.loc.gov/vocabulary/relators/  
   **lcn:** http://id.loc.gov/authorities/names/  
   **obo:** http://purl.obolibrary.org/obo/  
   **owl:** http://www.w3.org/2002/07/owl#  
   **ore:** http://www.openarchives.org/ore/terms/  
   **pcdm:** http://pcdm.org/models#  
   **premis:** http://www.loc.gov/premis/rdf/v1#  
   **prism:** http://prismstandard.org/namespaces/basic/3.0/  
   **rels:** info:fedora/fedora-system:def/relations-external#  
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
   **webacl:** http://www.w3.org/ns/auth/acl#  
   **works:** http://pcdm.org/works#  
   **vivo:** http://vivoweb.org/ontology/core#  

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

# Table of Contents
### Properties 
  * [pcdm:fileOf](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmfileof)  
  * [pcdm:hasFile](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmhasfile)  
  * [pcdm:hasMember](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmhasmember)  
  * [pcdm:hasRelatedObject](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmhasrelatedobject)  
  * [pcdm:memberOf](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmmemberof)  
  * [pcdm:relatedObjectOf](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmrelatedobjectof)  
  * [prism:doi](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#prismdoi)  
  * [dc:contributor](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dccontributor)  
  * [dc:creator](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dccreator)  
  * [dc:rights](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dcrights)  
  * [dc:subject](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dcsubject)  
  * [dcterms:abstract](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsabstract)  
  * [dcterms:alternative](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsalternative)  
  * [dcterms:contributor](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermscontributor)  
  * [dcterms:created](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermscreated)  
  * [dcterms:creator](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermscreator)  
  * [dcterms:dateAccepted](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsdateaccepted)  
  * [dcterms:dateSubmitted](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsdatesubmitted)  
  * [dcterms:description](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsdescription)  
  * [dcterms:identifier](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsidentifier)  
  * [dcterms:isVersionOf](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsisversionof)  
  * [dcterms:language](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermslanguage)  
  * [dcterms:license](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermslicense)  
  * [dcterms:modified](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsmodified)  
  * [dcterms:relation](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsrelation)  
  * [dcterms:rights](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsrights)  
  * [dcterms:source](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermssource)  
  * [dcterms:spatial](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermsspatial)  
  * [dcterms:subject](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermssubject)  
  * [dcterms:temporal](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermstemporal)  
  * [dcterms:title](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermstitle)  
  * [dcterms:type](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermstype)  
  * [bibo:degree](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibodegree)  
  * [bibo:status](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibostatus)  
  * [http://swrc.ontoware.org/ontology#institution](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//swrc.ontoware.org/ontology#institution)  
  * [ual:commiteeMember](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualcommiteemember)  
  * [ual:department](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualdepartment)  
  * [ual:depositor](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualdepositor)  
  * [ual:dissertant](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualdissertant)  
  * [ual:fedora3Handle](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualfedora3handle)  
  * [ual:fedora3UUID](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualfedora3uuid)  
  * [ual:graduationDate](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualgraduationdate)  
  * [ual:hydraNoid](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualhydranoid)  
  * [ual:nnaFile](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualnnafile)  
  * [ual:nnaItem](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualnnaitem)  
  * [ual:path](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualpath)  
  * [ual:proquest](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualproquest)  
  * [ual:restrictedCollection](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualrestrictedcollection)  
  * [ual:sortYear](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualsortyear)  
  * [ual:specialization](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualspecialization)  
  * [ual:supervisor](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualsupervisor)  
  * [ual:thesisLevel](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualthesislevel)  
  * [ual:unicorn](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualunicorn)  
  * [ore:aggregates](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#oreaggregates)  
  * [ore:isAggregatedBy](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#oreisaggregatedby)  

### Terms 
  * [cc:License](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#cclicense)  
  * [lang:iso639-2_Language](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langiso639-2_language)  
  * [pcdm:AlternateOrder](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmalternateorder)  
  * [pcdm:Collection](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmcollection)  
  * [pcdm:File](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmfile)  
  * [pcdm:Object](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#pcdmobject)  
  * [works:FileSet](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#worksfileset)  
  * [works:Range](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#worksrange)  
  * [works:TopRange](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#workstoprange)  
  * [works:Work](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#workswork)  
  * [dcterms:LicenseDocument](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermslicensedocument)  
  * [dcterms:LinguisticSystem](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#dctermslinguisticsystem)  
  * [bibo:Article](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#biboarticle)  
  * [bibo:Book](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibobook)  
  * [bibo:Chapter](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibochapter)  
  * [bibo:DocumentStatus](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibodocumentstatus)  
  * [bibo:Image](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#biboimage)  
  * [bibo:Report](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#biboreport)  
  * [bibo:Thesis](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibothesis)  
  * [http://purl.org/spar/fabio/DoctoralThesis](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//purl.org/spar/fabio/doctoralthesis)  
  * [http://purl.org/spar/fabio/MastersThesis](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//purl.org/spar/fabio/mastersthesis)  
  * [http://purl.org/spar/fabio/Thesis](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//purl.org/spar/fabio/thesis)  
  * [ual:learningObject](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#uallearningobject)  
  * [ual:researchMaterial](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualresearchmaterial)  
  * [ual:workType](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualworktype)  
  * [vivo:ConferencePaper](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#vivoconferencepaper)  
  * [vivo:ConferencePoster](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#vivoconferenceposter)  
  * [vivo:Dataset](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#vivodataset)  
  * [vivo:Review](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#vivoreview)  
  * [ore:Aggregation](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#oreaggregation)  
  * [http://xmlns.com/foaf/0.1/Organization](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//xmlns.com/foaf/0.1/organization)  

### Values 
  * [http://creativecommons.org/licenses/by-nc-nd/3.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-nc-nd/3.0/)  
  * [http://creativecommons.org/licenses/by-nc-nd/4.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-nc-nd/4.0/)  
  * [http://creativecommons.org/licenses/by-nc-sa/3.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-nc-sa/3.0/)  
  * [http://creativecommons.org/licenses/by-nc-sa/4.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-nc-sa/4.0/)  
  * [http://creativecommons.org/licenses/by-nc/3.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-nc/3.0/)  
  * [http://creativecommons.org/licenses/by-nc/4.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-nc/4.0/)  
  * [http://creativecommons.org/licenses/by-nd/3.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-nd/3.0/)  
  * [http://creativecommons.org/licenses/by-nd/4.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-nd/4.0/)  
  * [http://creativecommons.org/licenses/by-sa/3.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-sa/3.0/)  
  * [http://creativecommons.org/licenses/by-sa/4.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by-sa/4.0/)  
  * [http://creativecommons.org/licenses/by/3.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by/3.0/)  
  * [http://creativecommons.org/licenses/by/4.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/licenses/by/4.0/)  
  * [http://creativecommons.org/publicdomain/mark/1.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/publicdomain/mark/1.0/)  
  * [http://creativecommons.org/publicdomain/zero/1.0/](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#http//creativecommons.org/publicdomain/zero/1.0/)  
  * [lcn:n79058482](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#lcnn79058482)  
  * [lang:eng](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langeng)  
  * [lang:fre](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langfre)  
  * [lang:ger](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langger)  
  * [lang:ipk](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langipk)  
  * [lang:ita](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langita)  
  * [lang:jpn](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langjpn)  
  * [lang:por](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langpor)  
  * [lang:rus](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langrus)  
  * [lang:spa](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langspa)  
  * [lang:ukr](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langukr)  
  * [lang:vie](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langvie)  
  * [lang:zho](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langzho)  
  * [lang:zxx](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#langzxx)  
  * [bibo:status#accepted](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibostatus#accepted)  
  * [bibo:status#draft](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibostatus#draft)  
  * [bibo:status#published](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibostatus#published)  
  * [bibo:status#unpublished](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#bibostatus#unpublished)  
  * [ual:other](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#ualother)  
  * [vivo:submitted](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/jupiter_ontology.md#vivosubmitted)  


# Properties  
### pcdm:fileOf

   **rdfs:comment**   
  Links from a File to its containing Object.  

   **rdfs:domain**   
  http://pcdm.org/models#File  

   **rdfs:label**   
  is file of  

   **rdfs:range**   
  http://pcdm.org/models#Object  

   **rdfs:subPropertyOf**   
  http://www.openarchives.org/ore/terms/isAggregatedBy  

   **owl:inverseOf**   
  http://pcdm.org/models#hasFile  

***
### pcdm:hasFile

   **rdfs:comment**   
  Links to a File contained by this Object.  

   **rdfs:domain**   
  http://pcdm.org/models#Object  

   **rdfs:label**   
  has file  

   **rdfs:range**   
  http://pcdm.org/models#File  

   **rdfs:subPropertyOf**   
  http://www.openarchives.org/ore/terms/aggregates  

***
### pcdm:hasMember

   **rdfs:comment**   
  Links to a subsidiary Object or Collection. Typically used to link          to component parts, such as a book linking to a page.  Note on transitivity: hasMember is          not defined as transitive, but applications may treat it as transitive as local needs          dictate.  

   **rdfs:domain**   
  http://www.openarchives.org/ore/terms/Aggregation  

   **rdfs:label**   
  has member  

   **rdfs:range**   
  http://www.openarchives.org/ore/terms/Aggregation  

   **rdfs:subPropertyOf**   
  http://www.openarchives.org/ore/terms/aggregates  

   **owl:inverseOf**   
  http://pcdm.org/models#memberOf  

***
### pcdm:hasRelatedObject

   **rdfs:comment**   
  Links to a related Object that is not a component part, such as an object representing a donor agreement or policies that govern the resource.  

   **rdfs:domain**   
  http://www.openarchives.org/ore/terms/Aggregation  

   **rdfs:label**   
  has related object  

   **rdfs:range**   
  http://pcdm.org/models#Object  

   **rdfs:subPropertyOf**   
  http://www.openarchives.org/ore/terms/aggregates  

   **owl:inverseOf**   
  http://pcdm.org/models#relatedObjectOf  

***
### pcdm:memberOf

   **rdfs:comment**   
  Links from an Object or Collection to a containing Object or Collection.  

   **rdfs:domain**   
  http://www.openarchives.org/ore/terms/Aggregation  

   **rdfs:label**   
  is member of  

   **rdfs:range**   
  http://www.openarchives.org/ore/terms/Aggregation  

   **rdfs:subPropertyOf**   
  http://www.openarchives.org/ore/terms/isAggregatedBy  

***
### pcdm:relatedObjectOf

   **rdfs:comment**   
  Links from an Object to a Object or Collection that it is related to.  

   **rdfs:domain**   
  http://pcdm.org/models#Object  

   **rdfs:label**   
  is related object of  

   **rdfs:range**   
  http://www.openarchives.org/ore/terms/Aggregation  

   **rdfs:subPropertyOf**   
  http://www.openarchives.org/ore/terms/isAggregatedBy  

***
### prism:doi

   **rdfs:comment**   
  The Digital Object Identifier, DOI, for the article.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://prismstandard.org/namespaces/basic/3.0  

   **rdfs:label**   
  Digital Object Identifier  

***
### dc:contributor

   **dcterms:description**   
  Examples of a Contributor include a person, an organization, or a service. Typically, the name of a Contributor should be used to indicate the entity.  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#contributor-006  

   **rdfs:comment**   
  An entity responsible for making contributions to the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/elements/1.1/  

   **rdfs:label**   
  Contributor  

***
### dc:creator

   **dcterms:description**   
  Examples of a Creator include a person, an organization, or a service. Typically, the name of a Creator should be used to indicate the entity.  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#creator-006  

   **rdfs:comment**   
  An entity primarily responsible for making the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/elements/1.1/  

   **rdfs:label**   
  Creator  

***
### dc:rights

   **dcterms:description**   
  Typically, rights information includes a statement about various property rights associated with the resource, including intellectual property rights.  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#rights-006  

   **rdfs:comment**   
  Information about rights held in and over the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/elements/1.1/  

   **rdfs:label**   
  Rights  

***
### dc:subject

   **dcterms:description**   
  Typically, the subject will be represented using keywords, key phrases, or classification codes. Recommended best practice is to use a controlled vocabulary.  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#subject-007  

   **rdfs:comment**   
  The topic of the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/elements/1.1/  

   **rdfs:label**   
  Subject  

***
### dcterms:abstract

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#abstract-003  

   **rdfs:comment**   
  A summary of the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Thesis  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Abstract  

   **rdfs:range**   
  http://www.w3.org/2000/01/rdf-schema#Literal  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/description  
  http://purl.org/dc/terms/description  

***
### dcterms:alternative

   **dcterms:description**   
  The distinction between titles and alternative titles is application-specific.  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#alternative-003  

   **rdfs:comment**   
  An alternative name for the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Alternative Title  

   **rdfs:range**   
  http://www.w3.org/2000/01/rdf-schema#Literal  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/title  
  http://purl.org/dc/terms/title  

***
### dcterms:contributor

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/contributor  

***
### dcterms:created

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#created-003  

   **rdfs:comment**   
  Date of creation of the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Article  
  http://purl.org/ontology/bibo/Book  
  http://purl.org/ontology/bibo/Chapter  
  http://purl.org/ontology/bibo/Image  
  http://purl.org/ontology/bibo/Report  
  http://terms.library.ualberta.ca/learningObject  
  http://terms.library.ualberta.ca/researchMaterial  
  http://vivoweb.org/ontology/core#ConferencePaper  
  http://vivoweb.org/ontology/core#ConferencePoster  
  http://vivoweb.org/ontology/core#Dataset  
  http://vivoweb.org/ontology/core#Review  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Date Created  

   **rdfs:range**   
  http://www.w3.org/2000/01/rdf-schema#Literal  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/date  

***
### dcterms:creator

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/creator  

***
### dcterms:dateAccepted

   **dcterms:description**   
  Examples of resources to which a Date Accepted may be relevant are a thesis (accepted by a university department) or an article (accepted by a journal).  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#dateAccepted-002  

   **rdfs:comment**   
  Date of acceptance of the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Thesis  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Date Accepted  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/date  

***
### dcterms:dateSubmitted

   **dcterms:description**   
  Examples of resources to which a Date Submitted may be relevant are a thesis (submitted to a university department) or an article (submitted to a journal).  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#dateSubmitted-002  

   **rdfs:comment**   
  Date of submission of the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Thesis  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Date Submitted  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/date  

***
### dcterms:description

   **dcterms:description**   
  Description may include but is not limited to: an abstract, a table of contents, a graphical representation, or a free-text account of the resource.  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#descriptionT-001  

   **rdfs:comment**   
  An account of the resource.  

   **rdfs:domain**   
  http://pcdm.org/models#Collection  
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Article  
  http://purl.org/ontology/bibo/Book  
  http://purl.org/ontology/bibo/Chapter  
  http://purl.org/ontology/bibo/Image  
  http://purl.org/ontology/bibo/Report  
  http://terms.library.ualberta.ca/learningObject  
  http://terms.library.ualberta.ca/researchMaterial  
  http://vivoweb.org/ontology/core#ConferencePaper  
  http://vivoweb.org/ontology/core#ConferencePoster  
  http://vivoweb.org/ontology/core#Dataset  
  http://vivoweb.org/ontology/core#Review  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Description  

   **rdfs:range**   
  http://www.w3.org/2000/01/rdf-schema#Literal  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/description  

***
### dcterms:identifier

   **dcterms:description**   
  Recommended best practice is to identify the resource by means of a string conforming to a formal identification system.   

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#identifierT-001  

   **rdfs:comment**   
  An unambiguous reference to the resource within a given context.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Identifier  

   **rdfs:range**   
  http://www.w3.org/2000/01/rdf-schema#Literal  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/identifier  

***
### dcterms:isVersionOf

   **rdfs:comment**   
  A related resource of which the described resource is a version, edition, or adaptation.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Is Version Of  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/relation  

***
### dcterms:language

   **dcterms:description**   
  Recommended best practice is to use a controlled vocabulary such as RFC 4646 [RFC4646].  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#languageT-001  

   **rdfs:comment**   
  A language of the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Language  

   **rdfs:range**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

***
### dcterms:license

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#license-002  

   **rdfs:comment**   
  A legal document giving official permission to do something with the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  License  

   **rdfs:range**   
  http://creativecommons.org/ns#License  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/rights  

***
### dcterms:modified

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#modified-003  

   **rdfs:comment**   
  Date on which the resource was changed.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Thesis  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Date Modified  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/date  

***
### dcterms:relation

   **rdfs:comment**   
  A related resource. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Article  
  http://purl.org/ontology/bibo/Book  
  http://purl.org/ontology/bibo/Chapter  
  http://purl.org/ontology/bibo/Image  
  http://purl.org/ontology/bibo/Report  
  http://terms.library.ualberta.ca/learningObject  
  http://terms.library.ualberta.ca/researchMaterial  
  http://vivoweb.org/ontology/core#ConferencePaper  
  http://vivoweb.org/ontology/core#ConferencePoster  
  http://vivoweb.org/ontology/core#Dataset  
  http://vivoweb.org/ontology/core#Review  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Relation  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/relation  

***
### dcterms:rights

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/rights  

***
### dcterms:source

   **rdfs:comment**   
  A related resource from which the described resource is derived. The described resource may be derived from the related resource in whole or in part. Recommended best practice is to identify the related resource by means of a string conforming to a formal identification system.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Article  
  http://purl.org/ontology/bibo/Book  
  http://purl.org/ontology/bibo/Chapter  
  http://purl.org/ontology/bibo/Image  
  http://purl.org/ontology/bibo/Report  
  http://terms.library.ualberta.ca/learningObject  
  http://terms.library.ualberta.ca/researchMaterial  
  http://vivoweb.org/ontology/core#ConferencePaper  
  http://vivoweb.org/ontology/core#ConferencePoster  
  http://vivoweb.org/ontology/core#Dataset  
  http://vivoweb.org/ontology/core#Review  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms  

   **rdfs:label**   
  Source  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/source  

***
### dcterms:spatial

   **rdfs:comment**   
  Spatial characteristics of the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  
  http://purl.org/ontology/bibo/Article  
  http://purl.org/ontology/bibo/Book  
  http://purl.org/ontology/bibo/Chapter  
  http://purl.org/ontology/bibo/Image  
  http://purl.org/ontology/bibo/Report  
  http://terms.library.ualberta.ca/learningObject  
  http://terms.library.ualberta.ca/researchMaterial  
  http://vivoweb.org/ontology/core#ConferencePaper  
  http://vivoweb.org/ontology/core#ConferencePoster  
  http://vivoweb.org/ontology/core#Dataset  
  http://vivoweb.org/ontology/core#Review  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Spatial Coverage  

   **rdfs:range**   
  http://purl.org/dc/terms/Location  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/coverage  

   **skos:editorialNote**   
  Extended to use literal range. To meet DCterms spec, a LOD vocabulary must be implemented.  

***
### dcterms:subject

   **dcterms:description**   
  Typically, the subject will be represented using keywords, key phrases, or classification codes. Recommended best practice is to use a controlled vocabulary.  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#subjectT-002  

   **rdfs:comment**   
  The topic of the resource.  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Subject  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/subject  

   **skos:note**   
  This term is intended to be used with non-literal values as defined in the DCMI Abstract Model (http://dublincore.org/documents/abstract-model/).  As of December 2007, the DCMI Usage Board is seeking a way to express this intention with a formal range declaration.  

***
### dcterms:temporal

   **rdfs:comment**   
  Temporal characteristics of the resource.  

   **rdfs:domain**   
  http://purl.org/ontology/bibo/Article  
  http://purl.org/ontology/bibo/Book  
  http://purl.org/ontology/bibo/Chapter  
  http://purl.org/ontology/bibo/Image  
  http://purl.org/ontology/bibo/Report  
  http://terms.library.ualberta.ca/learningObject  
  http://terms.library.ualberta.ca/researchMaterial  
  http://vivoweb.org/ontology/core#ConferencePaper  
  http://vivoweb.org/ontology/core#ConferencePoster  
  http://vivoweb.org/ontology/core#Dataset  
  http://vivoweb.org/ontology/core#Review  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Temporal Coverage  

   **rdfs:range**   
  http://purl.org/dc/terms/PeriodOfTime  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/coverage  

   **skos:editorialNote**   
  Extended to use literal range. To meet DCterms spec, a LOD vocabulary must be implemented.  

***
### dcterms:title

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#titleT-002  

   **rdfs:comment**   
  A name given to the resource.  

   **rdfs:domain**   
  http://pcdm.org/models#Collection  
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Title  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/title  

***
### dcterms:type

   **dcterms:description**   
  Recommended best practice is to use a controlled vocabulary such as the DCMI Type Vocabulary [DCMITYPE]. To describe the file format, physical medium, or dimensions of the resource, use the Format element.  

   **dcterms:hasVersion**   
  http://dublincore.org/usage/terms/history/#typeT-001  

   **rdfs:comment**   
  The nature or genre of the resource.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Type  

   **rdfs:range**   
  http://purl.org/ontology/bibo/Article  
  http://purl.org/ontology/bibo/Book  
  http://purl.org/ontology/bibo/Chapter  
  http://purl.org/ontology/bibo/Image  
  http://purl.org/ontology/bibo/Report  
  http://purl.org/ontology/bibo/Thesis  
  http://terms.library.ualberta.ca/learningObject  
  http://terms.library.ualberta.ca/researchMaterial  
  http://terms.library.ualberta.ca/workType  
  http://vivoweb.org/ontology/core#ConferencePaper  
  http://vivoweb.org/ontology/core#ConferencePoster  
  http://vivoweb.org/ontology/core#Dataset  
  http://vivoweb.org/ontology/core#Review  
  http://www.w3.org/2000/01/rdf-schema#Class  

   **rdfs:subPropertyOf**   
  http://purl.org/dc/elements/1.1/type  

***
### bibo:degree

   **obo:IAO_0000112**   
  The source of the public description and this info is found here:  http://bibotools.googlecode.com/svn/bibo-ontology/trunk/doc/index.html.  Bibo considers this term "unstable".  The bibo editorial note is: "We are not defining, using an enumeration, the range of the bibo:degree to the defined list of bibo:ThesisDegree. We won't do it because we want people to be able to define new degress if needed by some special usecases. Creating such an enumeration would restrict this to happen."  

   **rdfs:comment**   
  The thesis degree.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  degree  

   **status:term_status**   
  unstable  

   **skos:editorialNote**   
  We are not defining, using an enumeration, the range of the bibo:degree to the defined list of bibo:ThesisDegree. We won't do it because we want people to be able to define new degress if needed by some special usecases. Creating such an enumeration would restrict this to happen.  

   **http://www.w3.org/2008/05/skos#editorialNote**   
  [editor: Zach Schoenberger; date: 22-08-2017] Currently being used with literal. To bring in line with vocab, instances of 'thesis degree' need to be used, minted in ual namespace.  

***
### bibo:status

   **rdfs:comment**   
  The publication status of (typically academic) content.  

   **rdfs:domain**   
  http://purl.org/ontology/bibo/Article  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  status  

   **rdfs:range**   
  http://purl.org/ontology/bibo/DocumentStatus  

   **status:term_status**   
  stable  

   **skos:editorialNote**   
  We are not defining, using an enumeration, the range of the bibo:status to the defined list of bibo:DocumentStatus. We won't do it because we want people to be able to define new status if needed by some special usecases. Creating such an enumeration would restrict this to happen.  

***
### http://swrc.ontoware.org/ontology#institution

   **ual:preferredValue**   
  http://id.loc.gov/authorities/names/n79058482  

   **rdfs:comment**   
  The University where the graduating student was enrolled.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://swrc.ontoware.org/  

   **rdfs:label**   
  Institution  

   **rdfs:range**   
  http://xmlns.com/foaf/0.1/Organization  

***
### ual:commiteeMember

   **rdfs:comment**   
  A person who was a member of a group of persons responsible for evaluating and approving the student's thesis.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Commitee Member  

***
### ual:department

   **rdfs:comment**   
  A distinct, usually specialized educational unit within an educational organization responsible for the degree program to which the graduating student belonged.  
  Example: "Department of Biological Sciences" or "Department of Chemistry"  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Department  

***
### ual:depositor

   **rdfs:comment**   
  User responsible for depositing the resource  

   **rdfs:domain**   
  http://pcdm.org/models#Collection  
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Depositor  

***
### ual:dissertant

   **rdfs:comment**   
  A person responsible for making the thesis.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Dissertant  

***
### ual:fedora3Handle

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Fedora 3 Handle  

***
### ual:fedora3UUID

   **rdfs:domain**   
  http://pcdm.org/models#Collection  
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Fedora 3 UUID  

***
### ual:graduationDate

   **rdfs:comment**   
  Date student graduated from degree program.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Graduation Date  

***
### ual:hydraNoid

   **rdfs:domain**   
  http://pcdm.org/models#Collection  
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Hydra NOID  

***
### ual:nnaFile

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Northern North America Filename  

***
### ual:nnaItem

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Northern North America Item ID  

***
### ual:path

   **rdfs:comment**   
  captures the community/collection pair to which an object belongs. used for circumventing pcdm:memberOf.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Path  

***
### ual:proquest

   **rdfs:comment**   
  Proquest Id for legacy thesis  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Proquest  

***
### ual:restrictedCollection

   **rdfs:comment**   
  indicates if deposit into collection is restricted to admin only.  

   **rdfs:domain**   
  http://pcdm.org/works#Collection  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Restriced Collection  

***
### ual:sortYear

   **rdfs:comment**   
  Year part of creation date for non-thesis items and graduation date for thesis items. Used for sorting purposes.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Sort Year  

***
### ual:specialization

   **rdfs:comment**   
  Example: "Microbiology and Biotechnology"; "Comparative Literature"  
  Subject focus of degree awarded.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Specialization  

***
### ual:supervisor

   **rdfs:comment**   
  Person responsible for the role of advising the graduating student.  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Supervisor  

***
### ual:thesisLevel

   **rdfs:comment**   
  The degree credential awarded  

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Thesis Level  

   **rdfs:range**   
  http://purl.org/spar/fabio/Thesis  

***
### ual:unicorn

   **rdfs:domain**   
  http://pcdm.org/works#Work  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Unicorn  

***
### ore:aggregates

***
### ore:isAggregatedBy

***
# Terms  
### cc:License

   **rdfs:comment**   
  a set of requests/permissions to users of a Work, e.g. a copyright license, the public domain, information for distributors  

   **rdfs:isDefinedBy**   
  https://creativecommons.org/ns#  

   **rdfs:label**   
  License  

   **rdfs:subClassOf**   
  http://purl.org/dc/terms/LicenseDocument  

***
### lang:iso639-2_Language

   **rdfs:comment**   
  An instance of this class is an ISO639-2 Language.  A finite set of individuals are instances of an ISO639-2 Language.  

   **rdfs:label**   
  ISO639-2 Language  

***
### pcdm:AlternateOrder

   **rdfs:comment**   
          An AlternateOrder is an alternate ordering of its parent's members.  It should only order the        parent's members, and otherwise has all of the features of ordering (some members may be        omitted from the order, members may appear more than once in the order, etc.).        

   **rdfs:label**   
  Alternate Order  

   **rdfs:subClassOf**   
  http://pcdm.org/models#Object  

***
### pcdm:Collection

   **rdfs:comment**   
          A Collection is a group of resources. Collections have descriptive metadata, access metadata,        and may links to works and/or collections. By default, member works and collections are an        unordered set, but can be ordered using the ORE Proxy class.        

   **rdfs:label**   
  Collection  

   **rdfs:subClassOf**   
  http://www.openarchives.org/ore/terms/Aggregation  

***
### pcdm:File

   **rdfs:comment**   
          A File is a sequence of binary data and is described by some accompanying metadata.        The metadata typically includes at least basic technical metadata (size, content type,        modification date, etc.), but can also include properties related to preservation,        digitization process, provenance, etc. Files MUST be contained by exactly one Object.        

   **rdfs:label**   
  File  

***
### pcdm:Object

   **rdfs:comment**   
          An Object is an intellectual entity, sometimes called a "work", "digital object", etc.        Objects have descriptive metadata, access metadata, may contain files and other Objects as        member "components". Each level of a work is therefore represented by an Object instance,        and is capable of standing on its own, being linked to from Collections and other Objects.        Member Objects can be ordered using the ORE Proxy class.        

   **rdfs:label**   
  Object  

   **rdfs:subClassOf**   
  http://www.openarchives.org/ore/terms/Aggregation  

***
### works:FileSet

   **rdfs:comment**   
        A group of related Files, typically a single master File and its derivatives.      

   **rdfs:label**   
  FileSet  

   **rdfs:subClassOf**   
  http://pcdm.org/models#Object  

***
### works:Range

   **rdfs:comment**   
        A section of a Work, corresponding to a IIIF Range.  Has member FileSets representing the      physical parts of the Work are part of the section (e.g., which pages are in a chapter).      

   **rdfs:label**   
  Range  

   **rdfs:subClassOf**   
  http://pcdm.org/models#Object  

   **skos:closeMatch**   
  http://iiif.io/model/shared-canvas/1.0/#Range  

***
### works:TopRange

   **rdfs:comment**   
        A logical ordering of the component parts of a Work, corresponding to a IIIF Range with      the "top" viewing hint.  Has member Ranges that represent the logical structure, such      as chapters within a book, scenes in a film, etc.      

   **rdfs:label**   
  TopRange  

   **rdfs:subClassOf**   
  http://pcdm.org/models#Object  

   **skos:closeMatch**   
  http://iiif.io/model/shared-canvas/1.0/#Range  

***
### works:Work

   **rdfs:comment**   
        A work or intellectual entity, such as a book, film, dissertation, etc.      Works have member FileSets representing their physical structure (e.g., pages in a book),      and related TopRanges representing their logical structure or structures (e.g., sections      and chapters in a book).      

   **rdfs:label**   
  Work  

   **rdfs:subClassOf**   
  http://pcdm.org/models#Object  

***
### dcterms:LicenseDocument

   **rdfs:label**   
  License Document  

***
### dcterms:LinguisticSystem

   **rdfs:isDefinedBy**   
  http://purl.org/dc/terms/  

   **rdfs:label**   
  Linguistic System  

***
### bibo:Article

   **rdfs:comment**   
  A written composition in prose, usually nonfiction, on a specific topic, forming an independent part of a book or other publication, as a newspaper or magazine.  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  Article  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

   **status:term_status**   
  stable  

   **skos:preflabel**   
  Journal Article  

***
### bibo:Book

   **rdfs:comment**   
  A written or printed work of fiction or nonfiction, usually on sheets of paper fastened or bound together within covers.  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  Book  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

   **status:term_status**   
  stable  

***
### bibo:Chapter

   **rdfs:comment**   
  A chapter of a book.  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  Chapter  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

   **status:term_status**   
  unstable  

   **skos:preflabel**   
  Chapter  

***
### bibo:DocumentStatus

   **rdfs:comment**   
  The status of the publication of a document.  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  Document Status  

   **status:term_status**   
  stable  

***
### bibo:Image

   **rdfs:comment**   
  A document that presents visual or diagrammatic information.  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  Image  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

   **status:term_status**   
  stable  

***
### bibo:Report

   **rdfs:comment**   
  A document describing an account or statement describing in detail an event, situation, or the like, usually as the result of observation, inquiry, etc..  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  Report  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

   **status:term_status**   
  stable  

***
### bibo:Thesis

   **rdfs:comment**   
  A document created to summarize research findings associated with the completion of an academic degree.  

   **rdfs:isDefinedBy**   
  http://purl.org/ontology/bibo/  

   **rdfs:label**   
  Thesis  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

   **status:term_status**   
  stable  

***
### http://purl.org/spar/fabio/DoctoralThesis

   **rdfs:comment**   
  A thesis reporting the research undertaken during a period of graduate study leading to a doctoral degree.  

   **rdfs:isDefinedBy**   
  http://purl.org/spar/fabio/  

   **rdfs:label**   
  doctoral thesis  

   **rdfs:subClassOf**   
  http://purl.org/spar/fabio/Thesis  

   **owl:disjointWith**   
  http://purl.org/spar/fabio/MastersThesis  

***
### http://purl.org/spar/fabio/MastersThesis

   **rdfs:comment**   
  A thesis reporting a research project undertaken as part of a graduate course of education leading to a master's degree.  

   **rdfs:isDefinedBy**   
  http://purl.org/spar/fabio/  

   **rdfs:label**   
  master's thesis  

   **rdfs:subClassOf**   
  http://purl.org/spar/fabio/Thesis  

***
### http://purl.org/spar/fabio/Thesis

***
### ual:learningObject

   **rdfs:comment**   
  a collection of content items, practice items, and assessment items that are combined based on a single learning objective  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Learning Object  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

***
### ual:researchMaterial

   **rdfs:comment**   
  a resource that cannot be neatly defined within the scope of any other type (i.e. "other")  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Research Material  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

***
### ual:workType

   **rdfs:comment**   
  Different classes for determining instances of a work according to the nature of the archived object.  

   **rdfs:isDefinedBy**   
  http://terms.library.ualberta.ca  

   **rdfs:label**   
  Work Type  

***
### vivo:ConferencePaper

   **obo:IAO_0000115**   
  A paper presented at a conference; optionally collected into a Proceedings or a special Journal issue  

   **rdfs:label**   
  Conference Paper  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

***
### vivo:ConferencePoster

   **obo:IAO_0000115**   
  The digital file (or physical equivalent), if available after the conference, vs. the act of attending/presenting: use ConferencePresentation for information about date/time/location/name of the event where the poster was presented  

   **rdfs:label**   
  Conference Poster  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

***
### vivo:Dataset

   **obo:IAO_0000112**   
  US Patent Data; US Job Data  

   **obo:IAO_0000115**   
  A named collection of data, usually containing only one type of data  

   **rdfs:label**   
  Dataset  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

***
### vivo:Review

   **obo:IAO_0000115**   
  An article reviewing one or more other information resources (a book, one or more other articles, movies, etc)  

   **rdfs:label**   
  Review  

   **rdfs:subClassOf**   
  http://terms.library.ualberta.ca/workType  

***
### ore:Aggregation

***
### http://xmlns.com/foaf/0.1/Organization

   **rdfs:comment**   
  The Organization class represents a kind of Agent corresponding to social instititutions such as companies, societies etc.  

   **rdfs:isDefinedBy**   
  http://xmlns.com/foaf/spec/  

   **rdfs:label**   
  Organization  

***
# Values  
### http://creativecommons.org/licenses/by-nc-nd/3.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-NonCommercial-NoDerivs 3.0 Unported  

***
### http://creativecommons.org/licenses/by-nc-nd/4.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-NonCommercial-NoDerivatives 4.0 International  

***
### http://creativecommons.org/licenses/by-nc-sa/3.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-NonCommercial-ShareAlike 3.0 Unported  

***
### http://creativecommons.org/licenses/by-nc-sa/4.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-NonCommercial-ShareAlike 4.0 International  

***
### http://creativecommons.org/licenses/by-nc/3.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-NonCommercial 3.0 Unported  

***
### http://creativecommons.org/licenses/by-nc/4.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-NonCommercial 4.0 International  

***
### http://creativecommons.org/licenses/by-nd/3.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-NoDerivs 3.0 Unported  

***
### http://creativecommons.org/licenses/by-nd/4.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-NoDerivatives 4.0 International  

***
### http://creativecommons.org/licenses/by-sa/3.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-ShareAlike 3.0 Unported  

***
### http://creativecommons.org/licenses/by-sa/4.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution-ShareAlike 4.0 International  

***
### http://creativecommons.org/licenses/by/3.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution 3.0 Unported  

***
### http://creativecommons.org/licenses/by/4.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Attribution 4.0 International  

***
### http://creativecommons.org/publicdomain/mark/1.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  Public Domain Mark 1.0  

***
### http://creativecommons.org/publicdomain/zero/1.0/

   **@type**   
  http://creativecommons.org/ns#License  

   **rdfs:label**   
  CC0 1.0 Universal  

***
### lcn:n79058482

   **@type**   
  http://xmlns.com/foaf/0.1/Organization  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/authorities/names  

   **rdfs:label**   
  University of Alberta  

***
### lang:eng

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  English  

***
### lang:fre

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  French  

***
### lang:ger

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  German  

***
### lang:ipk

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Inupiaq  

***
### lang:ita

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Italian  

***
### lang:jpn

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Japanese  

***
### lang:por

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Portuguese  

***
### lang:rus

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Russian  

***
### lang:spa

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Spanish  

***
### lang:ukr

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Ukranian  

***
### lang:vie

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Vietnamese  

***
### lang:zho

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  Chinese  

***
### lang:zxx

   **@type**   
  http://id.loc.gov/vocabulary/iso639-2/iso639-2_Language  
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:isDefinedBy**   
  http://id.loc.gov/vocabulary/iso639-2/  

   **rdfs:label**   
  No linguistic content  

***
### bibo:status#accepted

   **@type**   
  http://purl.org/ontology/bibo/DocumentStatus  

   **rdfs:comment**   
  Accepted for publication after peer reviewing.  

   **rdfs:label**   
  accepted  

   **status:term_status**   
  stable  

   **skos:preflabel**   
  Accepted  

***
### bibo:status#draft

   **@type**   
  http://purl.org/ontology/bibo/DocumentStatus  

   **rdfs:comment**   
  Document drafted  

   **rdfs:label**   
  draft  

   **status:term_status**   
  stable  

   **skos:preflabel**   
  Draft  

***
### bibo:status#published

   **@type**   
  http://purl.org/ontology/bibo/DocumentStatus  

   **rdfs:comment**   
  Published document  

   **rdfs:label**   
  published  

   **status:term_status**   
  stable  

   **skos:preflabel**   
  Published  

***
### bibo:status#unpublished

   **@type**   
  http://purl.org/ontology/bibo/DocumentStatus  

   **rdfs:comment**   
  Unpublished document  

   **rdfs:label**   
  unpublished  

   **status:term_status**   
  stable  

   **skos:preflabel**   
  Unpublished  

***
### ual:other

   **@type**   
  http://purl.org/dc/terms/LinguisticSystem  

   **rdfs:label**   
  Other language  

***
### vivo:submitted

   **@type**   
  http://purl.org/ontology/bibo/DocumentStatus  

   **rdfs:label**   
  submitted  

   **skos:preflabel**   
  Submitted  

***
