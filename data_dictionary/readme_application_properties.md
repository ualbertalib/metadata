# Application Specific Properties in Jupiter

## Item

### Properties available in application only

- member_of_paths
  - format: community_id/collection_id
  - used for: breadcrumbs, community/collection facets, item view, deposit form
  - predicate: http://terms.library.ualberta.ca/identifiers/path
  - multivalue: yes
  - reason of use: to avoid multiple calls to Solr when saving objects or fetching the collection/community information for item view or search facets. 

- record_created_at
  - format: sysytem date (Mon, 18 Dec 2017 01:00:20 UTC +00:00)
  - used for: When the object is created in Jupiter
  - predicate: http://terms.library.ualberta.ca/record_created_at
  - multivalue: no
  - reason of use: We need a sufficiently high-precision (millisecond resolution) timestamp, and ActiveFedora's property is not able to provide such level of precision. 

- doi_without_label
  - format: 10.7939/R39J1J
  - used for: present doi link on the user interface
  - predicate: N/A (Solr Only)
  - data: derived from data in attribute: prism: doi in Fedora
  - multivalue: no
  - reason of use: We need to index DOIs only for an exact match when searching on UI so users don't get a long list of items with similar DOI prefixes. Since we are doing an exact match only, and users cannot be expected to prefix their searches with "doi:", we need to do be clever to meet both Metadata and UX requirements, and so we index the DOI property without the "doi:" prefix. In this example "10.7939/R3TT77"
 
- item_type_with_status
  - format: item_type or article_publication_status 
  - used for: searching, faceting and forms for this combined attribute
  - predicate: N/A (Solr Only)
  - data: derived from dcterms:type + bibo:status (When item type is article, it will hold information for item_type + publication_status)
  - multivalue: no 

### Properties name mapping:
- contributors -> dc:contributor
- creators -> dc:creator
- languages -> dcterms:language
- item_type -> dcterms:type
- publication_status -> bibo:status
- fedora3_handle -> ual:fedora3Handle
- fedora3_uuid -> ual:fedora3UUID

## Collection

### Properties available in the application only

- community_id
  - format: uuid
  - used for: breadcrumbs, facets, collection view and creation form, community browse page
  - predicate: http://terms.library.ualberta.ca/identifiers/path
  - multivalue: no
  - reason of use: ActiveFedora controls memberOf and there's no good way to access the ID without incurring the overhead of an access to Fedora without reindexing the ID separately. There are also semantics. PCDM's memberOf is multivalued, but a Collection should have only one community, and so community_id is single-valued. It's also used to keep it consistent with member_of_paths so the facet results can be coalesced with Items

- community_title
  - format: string 
  - used for: display community title on collection related UI
  - predicate: N/A (Solr Only)
  - data: derived from UAL:community_id
  - reason of use: have the information available on the collection objects to reduce the overhead of rendering collections. 
 
### Properties name mapping:
- creators -> dc:creator
- fedora3_uuid -> ual:fedora3UUID 

## Community

### Properties name mapping:
- creators -> dc:creator
- fedora_uuid -> ual:fedora3UUID
