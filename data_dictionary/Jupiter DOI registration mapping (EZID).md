# Jupiter DOI registration mapping (EZID)

This document specifies the EZID elements that must be included in an API call to EZID according to the [EZID API Guide](https://ezid.cdlib.org/doc/apidoc.html) in order to register a new item in Jupiter for a DOI, and maps them to specific values or to the Jupiter predicates that should supply the values.

When we transition to DataCite as our DOI provider, the element terms and syntax in the API call will be different, but the content should remain the same, because it reflects mandatory elements in the [DataCite schema (4.1)](https://schema.datacite.org/meta/kernel-4.1/).

## EZID Element Mappings
EZID Element | Value OR Jupiter Predicate (non-thesis items) | Value OR Jupiter Predicate (Thesis items) | Comment
-- | -- | -- | --
datacite.title | dcterms:title | dcterms:title | 
datacite.creator | dc:creator | ual:dissertant | EZID API guide: "Separate multiple names with `;`"
datacite.publicationyear | ual:sortYear | ual:sortYear | If a YYYY format value is unavailable, use the code `(:unav)`. Note that ual:sortYear is derived from dcterms:created and may not be in perfect alignment with DataCite instructions for embargoed items: "If an embargo period has been in effect, use the date when the embargo period ends."
datacite.resourcetype | Use a value in the form `General-Type/Specific-Type` from the mapping table below | use value `Text/Thesis` | 
datacite.publisher | Use value `University of Alberta Libraries` | Use value `University of Alberta Libraries` | 


## datacite.resourcetype Mappings
Jupiter dcterms:type | datacite.resourcetype value | Comment
-- | -- | --
Article (http://purl.org/ontology/bibo/Article) | Text/Article
Book (http://purl.org/ontology/bibo/Book) | Text/Book
Chapter (http://purl.org/ontology/bibo/Chapter) | Text/Chapter
Conference Paper (http://vivoweb.org/ontology/core#ConferencePaper) | Other/Conference Paper | This Jupiter type includes video and/or audio recordings of presentations
Conference Poster (http://vivoweb.org/ontology/core#ConferencePoster) | Image/Conference Poster
Dataset (http://vivoweb.org/ontology/core#Dataset) | Dataset
Image (http://purl.org/ontology/bibo/Image) | Image
Learning Object (http://terms.library.ualberta.ca/learningObject) | Other/Learning Object
Report (http://purl.org/ontology/bibo/Report) | Text/Report
Review (http://vivoweb.org/ontology/core#Review) | Text/Review
Research Material (http://terms.library.ualberta.ca/researchMaterial) | Other/Research Material
