# Application Specific Properties in Jupiter

## Item

### Properties available in application only

- member_of_paths
  - format: community_id/collection_id
  - used for: breadcrumbs, community/collection facets, item view, deposit form
  - predicate: http://terms.library.ualberta.ca/identifiers/path
  - multivalue: yes
  - reason of use: to avoid multiple calls to Solr when fetching the collection/community information for item view or search facets. 

- doi_without_label
  - format: 10.7939/R39J1J
  - used for: present doi link on the user interface
  - predicate: N/A (Solr Only)
  - data: derived from data in attribute: prism: doi in Fedora
  - multivalue: no
  - reason of use: to enable search and present doi link in the proper URL structure - https://doi.org/10.7939/R39J1J
- item_type_with_status
  - format: Articles_publication_status
  - used for: searching, faceting and forms for this combined attribute
  - predicate: N/A (Solr Only)
  - data: derived from dcterms:type + bibo:status
  - multivalue: yes

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
  - reason of use: to avoid multiple calls to solr when fetching the community information, and to keep it consistent with member_of_paths so the facet results can be coalesced with Items

- community_title
  - format: string 
  - used for: display community title on collection related UI
  - predicate: N/A (Solr Only)
  - data: derived from UAL:community_id
  - reason of use: to avoid additional calls to solr to retrieve the title whenever the information is need. 
 
### Properties name mapping:
- creators -> dc:creator
- fedora3_uuid -> ual:fedora3UUID 

## Community

### Properties name mapping:
- creators -> dc:creator
- fedora_uuid -> ual:fedora3UUID
