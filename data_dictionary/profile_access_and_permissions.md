 # Jupiter Guide Access Controls

This guide is meant to give clarity to the access control model implemented in Jupiter. It also describes how access controls were migrated from legacy ERA (aka HydraNorth). Changes to this model can be suggested by submitting a Github ticket. The metadata team will edit the document accordingly.

Access controls are the mechanism by which users are granted permissions for reading and/or writing to an object, as well as the scope of an object's visibility. They are defined on the object directly.

# Namespaces used in this document
  * **acl:** http://projecthydra.org/ns/auth/acl#
  * **bibo:** http://purl.org/ontology/bibo/
  * **dcterms:** http://purl.org/dc/terms/  
  * **ual:** http://terms.library.ualberta.ca/

# Annotations used in this document

   * **acceptedValues**
     * restricted values on this property
   * **appliesTo** 
     * the type of object for which this property is used (generic, thesis, collection, community)
   * **backwardCompatibleWith**
     * crosswalk to previously used terms (in ERA) for migration mapping  
   * **comment** 
     * Jupiter specific instructions for using this property
   * **usedWith**
     * the value can be used with these properties
   * **repeat**
     * can this property occur more than once? (boolean)


# Table of Contents:
  * Properties
    * [acl:embargoHistory](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#alcembargoistory)
    * [acl:visibilityAfterEmbargo](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#aclvisibilityafterembargo)
    * [bibo:owner](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#bibowner)
    * [dcterms:accessRights](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#dctermsaccessrights)
    * [dcterm:available](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#dctermsavailable)
  * Values
    * [ual:authenticated](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualauthenticated)
    * [ual:draft](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualdraft)
    * [ual:embargo](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualembargo)
    * [ual:public](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualpublic)

# Properties
### acl:embargoHistory
  * appliesTo:
    * thesis
  * backwardCompatibleWith:
    * acl:embargoHistory
  * comment:
    * describes the circumstances (i.e. date and change in visibility) under which the item was released from embargo
  * repeat:
    * false

### acl:visibilityAfterEmbargo
  * acceptedValues:
    * [ual:authenticated](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualauthenticated)
    * [ual:draft](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualdraft)
    * [ual:public](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualpublic)
  * appliesTo:
    * thesis
  * backwardCompatibleWith:
    * acl:visibilityAfterEmbargo
  * comment:
    * indicates the visibility of the object after the item is released from embargo
  * repeat:
    * false

### bibo:owner
  * acceptedValues:
    * mysql unique identifier
  * appliesTo:
    * thesis
    * generic
  * backwardCompatibleWith:
    * webacl 'write' group
  * comment:
    * At the point of migration, the "http://projecthydra.org/ns/auth/person#" prefix was stripped leaving only the ualberta email as the owner value. This HydraNorth legacy user value was preserved externally from Jupiter. Upon being ingested into Jupiter, the email was replaced by a unique ID generated from a mysql database containing user information.
  * repeat:
    * true

### dcterms:accessRights
  * acceptedValues:
    * [ual:authenticated](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualauthenticated)
    * [ual:draft](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualdraft)
    * [ual:embargo](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualembargo)
    * [ual:public](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#ualpublic)
  * appliesTo:
    * thesis
    * generic
    * collection
    * community
  * backwardCompatibleWith:
    * webacl 'read' group
  * comment:
    * indicates the current visibility of the object.
  * repeat:
    * false

### dcterms:available
  * appliesTo:
    * thesis
  * backwardCompatibleWith:
    * acl:embargoReleaseDate
  * comment:
    * indicates the date upon which the permissions change for an item under embargo ([dcterms:accessRights](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#dctermsaccessrights) takes the value declared in [acl:visibilityAfterEmbargo](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#aclvisibilityafterembargo))
  * repeat:
    * false

# Values

### ual:authenticated
  * usedWith:
    * [acl:visibilityAfterEmbargo](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#aclvisibilityafterembargo)
    * [dcterms:accessRights](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#dctermsaccessrights)
  * backwardCompatibleWith:
    * http://projecthydra.org/ns/auth/group#university_of_alberta
    * http://projecthydra.org/ns/auth/group#registered
    * "university_of_alberta"
  * comment:
    * visibility depends on CCID authentication
### ual:draft
  * usedWith:
    * [acl:visibilityAfterEmbargo](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#aclvisibilityafterembargo)
    * [dcterms:accessRights](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#dctermsaccessrights)
  * comment:
    * item is only visible to the owner
### ual:embargo
  * usedWith:
    * [acl:visibilityAfterEmbargo](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#aclvisibilityafterembargo)
    * [dcterms:accessRights](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#dctermsaccessrights)
  * backwardCompatibleWith:
    * acl:embargoReleaseDate > date of migration
  * comment:
    * item is behind an embargo
### ual:public
  * usedWith:
    * [acl:visibilityAfterEmbargo](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#aclvisibilityafterembargo)
    * [dcterms:accessRights](https://github.com/ualbertalib/metadata/blob/master/data_dictionary/profile_access_and_permissions.md#dctermsaccessrights)
  * backwardCompatibleWith:
    * http://projecthydra.org/ns/auth/group#public
    * "open"
    * "open_access"
  * item is visible to all users