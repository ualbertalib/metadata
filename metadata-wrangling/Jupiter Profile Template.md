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

### `jupiter:Community < pcdm:Object`



| Field            | Predicate              | Recommendation   | Expected Value         | Obligation       |
|------------------|------------------------|------------------|------------------------|------------------|
| description      | `dcterms:description`  | MUST             | Literal                | {1,1}            |
| title            | `dcterms:title`        | MUST             | Literal                | {1,1}            |
| has member       | `pcdm:hasMember`       | MUST             | `jupiter:Collection`   | {1,n}            |
| label            | `rdfs:label`           | MAY              | Literal                | {1,1}            |



### `jupiter:Collection < pcdm:Collection` (works:Collection)

| Field            | Predicate              | Recommendation   | Expected Value         | Obligation       |
|------------------|------------------------|------------------|------------------------|------------------|
| description      | `dcterms:description`  | MAY              | Literal                | {0,1}            |
| title            | `dcterms:title`        | MUST             | Literal                | {1,1}            |
| part of          | `dcterms:isPartOf`     | MUST             | `jupiter:Community`    | {1,1}            |
| has member       | `pcdm:hasMember`       | SHOULD           | `jupiter:Work`         | {0,n}            |
| label            | `rdfs:label`           | MAY              | Literal                | {1,1}            |



### `jupiter:Work (Generic) < pcdm:Object` (works:Work)

| Field            | Predicate              | Recommendation   | Expected Value         | Obligation       |
|------------------|------------------------|------------------|------------------------|------------------|
| ark              | `ual:ark`              | MUST             | Literal                | {1,1}            |
| subject          | `dc:subject`           | MUST             | Literal                | {1,n}            |
| title            | `dcterms:title`        | MUST             | Literal                | {1,1}            |
| alternative      | `dcterms:alternative`  | MAY              | Literal                | {0,n}            |
| identifier       | `dcterms:identifier`   | MAY              | Literal                | {0,n}            |
| nicorn           | `ual:unicorn`          | MAY              | Literal                | {0,n}            |
| fedora3uuid      | `ual:fedora3UUID`      | MAY              | Literal                | {0,n}            |
| fedora3handle    | `ual:fedora3Handle`    | MAY              | Literal                | {0,n}            |
| language         | `dcterms:language`     | MUST             | Literal                | [1,n}            |
| isVersionOf      | `dcterms:isVersionOf`  | MAY              | Literal                | {0,1}            |
| rights           | `dc:rights`            | MUST             | Literal                | {1,1}            |
| part of          | `dcterms:isPartOf`     | MUST             | `jupiter:Collection`   | {1,n}            |
| has member       | `pcdm:hasMember`       | MUST             | `jupiter:FileSet`      | {1,n}            |
| has related object | `pcdm:hasRelatedObject` | MAY             | `jupiter:Work`(pcdm:object)        | {0,n}            |

### `jupiter:Work (Thesis) < pcdm:Object` (works:Work)

| Field            | Predicate              | Recommendation   | Expected Value         | Obligation       |
|------------------|------------------------|------------------|------------------------|------------------|
| institution      | `ual:institution`      | MUST             | Literal                | {1,1}            |
| dissertant       | `ual:dissertant`       | MUST             | Literal                | {1,1}            |
| supervisor       | `ual:supervisor`       | MUST             | Literal                | {1,n}            |
| committee member | `ual:committeeMember`  | MUST             | Literal                | {1,n}            |
| department       | `ual:department`       | MUST             | Literal                | {1,n}            |
| subject          | `dc:subject`           | MUST             | Literal                | {1,n}            |
| specialization   | `ual:specialization`   | MAY              | Literal                | {0,1}            |
| dateSubmitted    | `dcterms:dateSubmitted`| MUST             | Date                   | {1,1}            |
| dateAccepted     | `dcterms:dateAccepted` | MUST             | Date                   | {1,1}            |
| graduationdate   | `ual:graduationdate`   | MUST             | Date                   | {1,1}            |
| title            | `dcterms:title`        | MUST             | Literal                | {1,1}            |
| alternative      | `dcterms:alternative`  | MAY              | Literal                | {0,n}            |
| degree           | `bibo:degree`          | MUST             | Literal                | {1,1}            |
| thesislevel      | `ual:thesislevel`      | MUST             | Literal                | {1,1}            |
| identifier       | `dcterms:identifier`   | MAY              | Literal                | {0,n}            |
| nicorn           | `ual:unicorn`          | MAY              | Literal                | {0,n}            |
| fedora3uuid      | `ual:fedora3UUID`      | MAY              | Literal                | {0,n}            |
| fedora3handle    | `ual:fedora3Handle`    | MAY              | Literal                | {0,n}            |
| proquest         | `ual:proquest`         | MAY              | Literal                | {0,1}            |
| digital object identifier | `prism:doi`   | MUST             | Literal                | {1,1}            |
| abstract         | `dcterms:abstract`     | MUST             | Literal                | {1,1}            |
| language         | `dcterms:language`     | MUST             | Literal                | [1,n}            |
| isVersionOf      | `dcterms:isVersionOf`  | MAY              | Literal                | {0,1}            |
| rights           | `dc:rights`            | MUST             | Literal                | {1,1}            |
| part of          | `dcterms:isPartOf`     | MUST             | `jupiter:Collection`   | {1,n}            |
| has member       | `pcdm:hasMember`       | MUST             | `jupiter:FileSet`      | {1,n}            |
| has related object | `pcdm:hasRelatedObject` | MAY             | `jupiter:Work`(pcdm:object)        | {0,n}            |

### `jupiter:FileSet < pcdm:Object`

| Field            | Predicate              | Recommendation   | Expected Value         | Obligation       |
|------------------|------------------------|------------------|------------------------|------------------|
| part of          | `dcterms:isPartOf`     | MUST             | `jupiter:Work`         | {1,1}            |
| has file         | `pcdm:hasFile`         | SHOULD           | `jupiter:File (pcdm:File)`| {1,n}           |
| label            | `rdfs:label`           | MAY              | Literal                | {1,1}            |


## Usage 
### Defining a new collection and reference to Collections
```turtle
<http://ual.ca/jupiter/collections/collection1> a jupiter:Collection ;
    dcterms:description "A Sample Collection" ;
    dcterms:title "1st collection" ;
    pcdm:hasMember <http://ual.ca/works/work1> .

<http://ual.ca/ns#SampleCollection> a rdfs:Class ;
    rdfs:label "Sample Collection"@en ;
    rdfs:subclassOf jupiter:Collection.

<http://ual.ca/communities/community1> a jupiter:Community ;
    pcdm:hasMember <http://ual.ca/collections/collection1> .
```

### Defining a new Work and reference to Works
```turtle
<http://ual.ca/jupiter/works/work1> a jupiter:Work ;
    dcterms:title "1st work" ;
    dcterms:alternate "work's other title" ;
    dcterms:identifier "A DOI" ;
    pcdm:hasRelatedObject <http://ual.ca/works/work2> ;
    pcdm:hasMember <http://ual.ca/fileset/fileset1> .

<http://ual.ca/ns#SampleWork> a rdfs:Class ;
    rdfs:label "Sample Work"@en ;
    rdfs:subclassOf jupiter:Work.

<http://ual.ca/collections/collection1> a jupiter:Collection ;
    pcdm:hasMember <http://ual.ca/works/work1> .
```

### Defining a new FileSet and reference to FileSets
```turtle 
<http://ual.ca/jupiter/fileset/fileset1> a jupiter:Work ;
    pcdm:hasFile <http://ual.ca/fileset/fileset1/file1> .

<http://ual.ca/ns#SampleFileSet> a rdfs:Class ;
    rdfs:label "Sample FileSet"@en ;
    rdfs:subclassOf jupiter:FileSet.

<http://ual.ca/works/work1> a jupiter:Work ;
    pcdm:hasMember <http://ual.ca/filesets/fileset1> .
```
