---
title: Jupiter Profile Template
author:
 Danoosh Davoodi
date: 2017-09-06
profile:
    organization: University of Alberta Libraries
    project: Jupiter
    namespaces:
        pcdm: http://pcdm.org/models#
        works: http://pcdm.org/works#
        rdfs: http://www.w3.org/2000/01/rdf-schema#
        dc: http://purl.org/dc/elements/1.1/
        dcterms: http://purl.org/dc/terms/
        bibo: http://purl.org/ontology/bibo/
        prism: http://prismstandard.org/namespaces/basic/3.0/
        ual: http://terms.library.ualberta.ca
---
# Jupiter Profile Template 
## Introduction 

This model describes the Jupiter project proposed data model and its use cases.


## Model
![Alt text](https://github.com/ualbertalib/metadata/blob/master/metadata-wrangling/draft%20single%20file.jpg)

### [`jupiter:Community < pcdm:Object`](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_community.md)
  ```turtle
    jupiter:Community a rdfs:Class .
  ```

### [`jupiter:Collection < pcdm:Collection`](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_collection.md) (works:Collection)
  ```turtle
    jupiter:Collection a rdfs:Class .
  ```

### [`jupiter:Item (Generic) < pcdm:Object`](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_generic.md) (works:Work)
  ```turtle
    jupiter:Item a rdfs:Class .
  ```

### [`jupiter:Item (Thesis) < pcdm:Object`](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_thesis.md) (works:Work)
  ```turtle
    jupiter:Item a rdfs:Class .
  ```

### `jupiter:FileSet < pcdm:Object`
  ```turtle
    jupiter:FileSet a rdfs:Class .
  ```

| Field            | Predicate              | Recommendation   | Expected Value         | Obligation       |
|------------------|------------------------|------------------|------------------------|------------------|
| member of        | `pcdm:memberOf`        | MUST             | `jupiter:Item`         | {1,1}            |
| has file         | `pcdm:hasFile`         | SHOULD           | `jupiter:File (pcdm:File)`| {1,n}           |
| label            | `rdfs:label`           | MAY              | Literal                | {1,1}            |

### `jupiter:File < pcdm:Object`
  ```turtle
    jupiter:File a rdfs:Class .
  ```

| Field            | Predicate              | Recommendation   | Expected Value         | Obligation       |
|------------------|------------------------|------------------|------------------------|------------------|
| file of          | `pcdm:fileOf`          | MUST             | `jupiter:FileSet`      | {1,1}            |
| label            | `rdfs:label`           | MAY              | Literal                | {1,1}            |


## Usage 
### Defining a new collection and reference to Collections
```turtle
<http://ual.ca/jupiter/collections/collection1> a jupiter:Collection ;
    dcterms:description "A Sample Collection" ;
    dcterms:title "1st collection" ;
    pcdm:hasMember <http://ual.ca/items/item1> .

<http://ual.ca/ns#SampleCollection> a rdfs:Class ;
    rdfs:label "Sample Collection"@en ;
    rdfs:subclassOf jupiter:Collection.

<http://ual.ca/communities/community1> a jupiter:Community ;
    pcdm:hasMember <http://ual.ca/collections/collection1> .
```

### Defining a new Item and reference to Items
```turtle
<http://ual.ca/jupiter/items/item1> a jupiter:Item ;
    dcterms:title "1st item" ;
    dcterms:alternate "item's other title" ;
    dcterms:identifier "A DOI" ;
    pcdm:hasRelatedObject <http://ual.ca/items/item2> ;
    pcdm:hasMember <http://ual.ca/fileset/fileset1> .

<http://ual.ca/ns#SampleWork> a rdfs:Class ;
    rdfs:label "Sample Work"@en ;
    rdfs:subclassOf jupiter:Item.

<http://ual.ca/collections/collection1> a jupiter:Collection ;
    pcdm:hasMember <http://ual.ca/items/item1> .
```

### Defining a new FileSet and reference to FileSets
```turtle 
<http://ual.ca/jupiter/fileset/fileset1> a jupiter:Item ;
    pcdm:hasFile <http://ual.ca/fileset/fileset1/file1> .

<http://ual.ca/ns#SampleFileSet> a rdfs:Class ;
    rdfs:label "Sample FileSet"@en ;
    rdfs:subclassOf jupiter:FileSet.

<http://ual.ca/works/work1> a jupiter:Item ;
    pcdm:hasMember <http://ual.ca/filesets/fileset1> .
```
