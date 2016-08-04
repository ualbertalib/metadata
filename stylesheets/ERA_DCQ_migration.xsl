<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:foxml="info:fedora/fedora-system:def/foxml#"
    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:ualdate="http://terms.library.ualberta.ca/date/"
    xmlns:ualid="http://terms.library.ualberta.ca/id/"
    xmlns:ualrole="http://terms.library.ualberta.ca/role/"
    xmlns:ualthesis="http://terms.library.ualberta.ca/thesis/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:eraterms="http://era.library.ualberta.ca/eraterms"
    xmlns:thesis="http://www.ndltd.org/standards/metadata/etdms/1.0/"
    xmlns:vivo="http://vivoweb.org/ontology/core#"
    xmlns:marcrel="http://id.loc.gov/vocabulary/relators/"
    xmlns:bibo="http://purl.org/ontology/bibo/"
    exclude-result-prefixes="xs xd"
    version="3.0">
    
    
    
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p>paredeso@ualberta.ca</xd:p>
            <xd:p>this stylesheet updates ERA FOXML descriptive metadata for migration into HydraNorth</xd:p>
            <xd:p>prefix and namespace changes documented at:
                <xd:ul>
                    <xd:li>https://docs.google.com/spreadsheets/d/1twJvO-oEPvaSYL8HSqEf892t6-a8wUEclGN6CgKgdsI/edit?usp=sharing</xd:li>
                    <xd:li>https://docs.google.com/spreadsheets/d/1hSd6kf4ABm-m8VtYNyqfJGtiZG7bLJQ3fWRbF_nVoIw/edit?usp=sharing</xd:li>
                </xd:ul>
            </xd:p>
        </xd:desc>
    </xd:doc> 
    
    
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    <xsl:strip-space elements="dc dcterms:* dc:*"/>

    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    
    <!-- When DCQ is present: copy XML structure but keep only last DCQ datastream, modifying data
        according to templates. Otherwise: copy XML structure, then call template to create new
        DCQ datastream based on last DC datastream -->    
    <xsl:template match="foxml:digitalObject">
        <xsl:copy>
            <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
            <xsl:apply-templates select="@*|node()"/>
            <xsl:if test="not(foxml:datastream[@ID='DCQ'])">
                <xsl:call-template name="newDCQ"/>
            </xsl:if>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Replace spaces in ownerId -->
    <xsl:template match="foxml:objectProperties/foxml:property[@NAME='info:fedora/fedora-system:def/model#ownerId']/@VALUE">
        <xsl:attribute name="VALUE">
            <xsl:value-of select="replace(.,'\s','_')"/>
        </xsl:attribute>
    </xsl:template>
    
    
    <!-- Replace spaces in submitterId -->
    <xsl:template match="//foxml:datastream[@ID='RELS-EXT']/foxml:datastreamVersion//*:RDF[namespace-uri()='http://www.w3.org/1999/02/22-rdf-syntax-ns#']/*:Description[namespace-uri()='http://www.w3.org/1999/02/22-rdf-syntax-ns#']/*:submitterId[namespace-uri()='http://era.library.ualberta.ca/schema/definitions.xsd#']">
        <xsl:copy>
            <xsl:value-of select="replace(.,'\s','_')"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Declare CCID access restriction if absent and item is part of restricted UAL Licensed Resources community (items protected at the application level in old ERA) -->
    <xsl:template match="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//rdf:Description[*:isMemberOf[@*:resource='info:fedora/uuid:11274e20-0426-4e80-84f4-bef79dbd6633']]">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
            <xsl:if test="not(*:isPartOf[@*:resource='info:fedora/ir:CCID_AUTH'])">
                <xsl:element name="isPartOf" namespace="info:fedora/fedora-system:def/relations-external#">
                    <xsl:attribute name="rdf:resource">info:fedora/ir:CCID_AUTH</xsl:attribute>
                </xsl:element>
            </xsl:if>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Fix double-nested DCQ datastreams / keep only last DCQ datastreamVersion / -->
    <xsl:template match="foxml:datastream[@ID='DCQ']">
        <xsl:choose>
            <xsl:when test=".//foxml:xmlContent//foxml:xmlContent">
                <xsl:copy copy-namespaces="no">
                    <xsl:apply-templates select="@*"/>
                    <xsl:copy copy-namespaces="no" select="foxml:datastreamVersion[last()]">
                        <xsl:apply-templates select="@*"/>
                        <xsl:apply-templates select="//foxml:xmlContent//foxml:xmlContent"/>
                    </xsl:copy>
                </xsl:copy>
            </xsl:when>
            <xsl:otherwise>
                <xsl:copy copy-namespaces="no">
                    <xsl:apply-templates select="@*"/>
                    <xsl:apply-templates select="foxml:datastreamVersion[last()]"/>
                </xsl:copy>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <!-- Namespaces -->
    <xsl:template name="namespaces">
        <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
        <xsl:namespace name="dc">http://purl.org/dc/elements/1.1/</xsl:namespace>        
        <xsl:namespace name="ualdate">http://terms.library.ualberta.ca/date/</xsl:namespace>
        <xsl:namespace name="ualid">http://terms.library.ualberta.ca/id/</xsl:namespace>
        <xsl:namespace name="ualrole">http://terms.library.ualberta.ca/role/</xsl:namespace>
        <xsl:namespace name="ualthesis">http://terms.library.ualberta.ca/thesis/</xsl:namespace>
        <xsl:namespace name="vivo">http://vivoweb.org/ontology/core#</xsl:namespace>
        <xsl:namespace name="marcrel">http://id.loc.gov/vocabulary/relators/</xsl:namespace>
        <xsl:namespace name="bibo">http://purl.org/ontology/bibo/</xsl:namespace>
        <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
    </xsl:template>
    
    
    <!-- New DCQ datastream based on last DC datastream: created with xsl instructions to control
        namespace declarations -->
    <xsl:template name="newDCQ">
        <xsl:element name="foxml:datastream" inherit-namespaces="no">
            <xsl:attribute name="CONTROL_GROUP">X</xsl:attribute>
            <xsl:attribute name="ID">DCQ</xsl:attribute>
            <xsl:attribute name="STATE">A</xsl:attribute>
            <xsl:attribute name="VERSIONABLE">true</xsl:attribute>
            <xsl:element name="foxml:datastreamVersion" inherit-namespaces="no">
                <xsl:attribute name="ID">DCQ.0</xsl:attribute>
                <xsl:attribute name="LABEL">Item Metadata</xsl:attribute>
                <xsl:attribute name="MIMETYPE">text/xml</xsl:attribute>
                <xsl:element name="foxml:xmlContent">
                    <xsl:element name="dc">
                        <xsl:call-template name="namespaces"/>
                        <xsl:apply-templates
                            select="//foxml:datastream[@ID='DC']/foxml:datastreamVersion[last()]//oai_dc:dc/node()"/>
                    </xsl:element>
                </xsl:element>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    
    
    <!-- Update namespaces, apply templates, when thesis add rights statement -->
    <xsl:template match="//dc[last()]">        
        <xsl:copy copy-namespaces="no">
            <xsl:call-template name="namespaces"/>
            <xsl:apply-templates select="@*|node()"/>
            <xsl:if test="not(*:rights)">
                <xsl:call-template name="rights">
                    <xsl:with-param name="dateSub">
                        <xsl:value-of select="replace(substring(./*[local-name()[matches(.,'date[sS]ubmitted')]],1,10),'-','')"/>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:if>
        </xsl:copy>
    </xsl:template>    
    
    
    
    <!-- Update namespaces, attributes and apply templates (dc: unchanged) -->    
    <xsl:template match="//oai_dc:dc">
        <xsl:copy copy-namespaces="no">
            <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
            <xsl:namespace name="dc">http://purl.org/dc/elements/1.1/</xsl:namespace>
            <xsl:namespace name="oai_dc">http://www.openarchives.org/OAI/2.0/oai_dc/</xsl:namespace>
            <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
            <xsl:attribute name="xsi:schemaLocation">http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd</xsl:attribute>
            <xsl:apply-templates select="node()" mode="noChange"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Control namespace declarations in dc/dcterms:* children-->
    <xsl:template match="//*:dc/dcterms:*">
        <xsl:copy copy-namespaces="no">
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Update dc prefix to dcterms in DCQ datastream-->
    <xsl:template match="*:dc/dc:*" priority="5">
        <xsl:element name="dcterms:{local-name()}" inherit-namespaces="no">
            <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>
    
    
    <xsl:template match="oai_dc:dc/dc:*" mode="noChange">
        <xsl:copy-of select="." copy-namespaces="no"/>
    </xsl:template>
    
    
    <!-- Strip attributes -->
    <!-- Last DC or DCQ datastream: strip @Size, strip @xsi:type with dctermsURI or anyURI values -->
    <xsl:template match="foxml:datastream[@ID='DCQ' or @ID='DC']/foxml:datastreamVersion[last()]/@SIZE|foxml:datastream[@ID='DCQ' or @ID='DC']/foxml:datastreamVersion[last()]/@xsi:type[.='dcterms:URI' or .='anyURI']"/>
    <xsl:template match="//dc/@dc"/>
    <xsl:template match="//dc/@xsi:schemaLocation"/>

    
    <!-- Move dates from coverage and spatial into dcterms:temporal and locations to dcterms:spatial -->
    <xsl:template match="//*:coverage" priority="6">
        <xsl:choose>
            <xsl:when test="string(number(.))!='NaN'">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="matches(.,'[0-9]{4}s?')">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="matches(.,'[0-9]{4}(-|/)[0-9]{4}')">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="matches(.,'[0-3]?[0-9](?:-|/)[0-3]?[0-9](?:-|/)(?:[0-9]{2})?[0-9]{2}')">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="matches(.,'\w+\s*(?:[Aa]ge|[Cc]entury|[Cc]ontemporary|[Pp]eriod|[Yy]ear|[Mm]onth|[Dd]ay|[Ww]inter|[Ss]pring|[Ss]ummer|[Ff]all|[Au]tumn|[Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|[Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember)')">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:when>
            <!-- match alphabetic string -->
            <xsl:when test="matches(.,'[A-Za-z]+')">
                <xsl:element name="dcterms:spatial">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:when>
            <!-- match roman numerals -->
            <!--<xsl:when test="matches(.,'(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})(?:.*entury)?')">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:when>-->
            <xsl:when test="not(text())"/>
            <xsl:otherwise>
                <xsl:element name="dcterms:coverage">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template match="//*:creator" priority="6">
        <xsl:choose>
            <xsl:when test="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//rdf:Description[*:isMemberOfCollection[@*:resource[matches(.,'(?:uuid:d7cceac1-cdb6-4f6c-8f99-e46cd28c292b|uuid:7af76c0f-61d6-4ebc-a2aa-79c125480269)')]]]">
                <xsl:element name="marcrel:dis">
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="dcterms:creator">
                    <xsl:choose>
                        <xsl:when test="text()[contains(.,'UofA Anthro')]">
                            <xsl:text>University of Alberta Department of Anthropology</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="normalize-space()"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <!-- Move date into dcterms:created -->
    <xsl:template match="//dc:date|//dcterms:date" priority="6">
        <xsl:element name="dcterms:created" inherit-namespaces="no">
            <xsl:apply-templates select="@*"/>
            <xsl:value-of select="normalize-space()"/>
        </xsl:element>
    </xsl:template>
    
    
    <xsl:template match="dcterms:datesubmitted" priority="6">
        <xsl:element name="dcterms:dateSubmitted">
            <xsl:apply-templates select="@*"/>
            <xsl:value-of select="normalize-space()"/>
        </xsl:element>
    </xsl:template>
    
    
    <xsl:template match="*:isversionof" priority="6">
        <xsl:element name="dcterms:isVersionOf">
            <xsl:value-of select="normalize-space()"/>
        </xsl:element>
    </xsl:template>
    
    
    <!-- Split *:rights into dcterms:rights or dcterms:license -->
    <xsl:template match="//*:rights" priority="6">        
        <xsl:choose>
            <xsl:when test="contains(.,'http:')">
                <xsl:element name="dcterms:license">
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//rdf:Description[*:isMemberOfCollection[@*:resource[matches(.,'(?:uuid:d7cceac1-cdb6-4f6c-8f99-e46cd28c292b|uuid:7af76c0f-61d6-4ebc-a2aa-79c125480269)')]]]">
                <xsl:call-template name="rights">                    
                    <xsl:with-param name="dateSub">
                        <xsl:value-of select="replace(substring(../*[local-name()[matches(.,'date[sS]ubmitted')]],1,10),'-','')"/>
                    </xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="dcterms:rights">
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    
    <xsl:template name="rights">
        <xsl:param name="dateSub"/>
        <xsl:if test="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//rdf:Description[*:isMemberOfCollection[@*:resource[matches(.,'(?:uuid:d7cceac1-cdb6-4f6c-8f99-e46cd28c292b|uuid:7af76c0f-61d6-4ebc-a2aa-79c125480269)')]]]">
            <xsl:element name="dcterms:rights">
                <xsl:choose>
                    <xsl:when test="../*[local-name()[matches(.,'date[sS]ubmitted')]] and $dateSub &lt; 20160301">
                        <xsl:text>This thesis is made available by the University of Alberta Libraries with permission of the copyright owner solely for the purpose of private, scholarly or scientific research. This thesis, or any portion thereof, may not otherwise be copied or reproduced without the written consent of the copyright owner, except to the extent permitted by Canadian copyright law.</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>This thesis is made available by the University of Alberta Libraries with permission of the copyright owner solely for non-commercial purposes. This thesis, or any portion thereof, may not otherwise be copied or reproduced without the written consent of the copyright owner, except to the extent permitted by Canadian copyright law.</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:element>
        </xsl:if>
    </xsl:template>
    
    
    
    <!-- *:relation changed to *:source -->
    <!-- special case: only for Halpern Image Archive community -->
    <xsl:template match="//*:relation[//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//*:isMemberOf[@rdf:resource='info:fedora/uuid:fabad4e3-0f6e-4368-bb80-0a110d72c0e9']]" priority="6">
        <xsl:element name="dcterms:source">
            <xsl:apply-templates select="@* | node()"/>  
        </xsl:element>
    </xsl:template>
    
    
    <!-- Move dates currently in spatial into temporal -->
    <xsl:template match="//*:spatial" priority="6">
        <xsl:choose>
            <xsl:when test="string(number(.))!='NaN'">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="matches(.,'[0-9]{4}s?')">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="matches(.,'[0-9]{4}(-|/)[0-9]{4}')">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="matches(.,'[0-3]?[0-9](?:-|/)[0-3]?[0-9](?:-|/)(?:[0-9]{2})?[0-9]{2}')">
                <xsl:element name="dcterms:temporal">
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="dcterms:spatial">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <!-- Cleanup embedded markup in subject fields -->
    <xsl:template match="//*:subject" priority="6">
        <xsl:element name="dcterms:subject" inherit-namespaces="no">
            <xsl:apply-templates select="@*"/>
            <xsl:value-of select="normalize-space()"/>
        </xsl:element>
    </xsl:template>
    
    
    <!-- Normalize type values as of 2015-04-->
    <xsl:template match="//*:type" priority="6">
        <xsl:element name="dcterms:type">
            <xsl:choose>
                <xsl:when test="matches(.,'[Bb]ook\s?[Cc]hapter')">
                    <xsl:text>Book Chapter</xsl:text>
                </xsl:when>            
                <xsl:when test="matches(.,'ConferenceWorkshopPoster|Conference Workshop Poster')">
                    <xsl:text>Conference/workshop Poster</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'ConferenceWorkshopPresentation|Conference Workshop Presentation')">
                    <xsl:text>Conference/workshop Presentation</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'JournalArticleDraftSubmitted')">
                    <xsl:text>Journal Article (Draft-Submitted)</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'JournalArticlePublished')">
                    <xsl:text>Journal Article (Published)</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'LearningObject')">
                    <xsl:text>Learning Object</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'report')">
                    <xsl:text>Report</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'[Rr]esearch\s?[Mm]aterial')">
                    <xsl:choose>
                        <xsl:when test="//*:datastream[@ID[matches(.,'^DS\d*')]]/*:datastreamVersion[last()][@MIMETYPE[contains(.,'image')]]">
                            <xsl:text>Image</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>Research Material</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test="matches(.,'thesis')">
                    <xsl:text>Thesis</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:element>
    </xsl:template>

    
    <!-- Identifiers (IN PROGRESS) -->
    <!-- mpo: to do: There are dc / dcterms identifier and description elements containing ids -->
    <xsl:template match="//dc/*:identifier/@xsi:type[. = 'eraterms:local' or 'dcterms:URI']" priority="6"/>
    <xsl:template name="string">
        <xsl:attribute name="xsi:type">
            <xsl:text>string</xsl:text>
        </xsl:attribute>
    </xsl:template>
    <xsl:template name="anyURI">
        <xsl:attribute name="xsi:type">
            <xsl:text>anyURI</xsl:text>
        </xsl:attribute>
    </xsl:template>
    
    
    <xsl:template match="//*:dc/*:identifier" priority="6">
        <xsl:choose>
            <xsl:when test="text()[contains(.,'uuid')]">
                <xsl:element name="ualid:fedora3uuid">
                    <xsl:call-template name="string"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="text()[contains(.,'handle')]">
                <xsl:element name="ualid:thesescanada">
                    <xsl:call-template name="anyURI"/>
                    <xsl:value-of select="concat('TC-AEU-',substring-after(.,'era.'))"/>
                </xsl:element>
                <xsl:element name="ualid:fedora3handle">
                    <xsl:call-template name="anyURI"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="namespace-uri()='http://purl.org/dc/elements/1.1/' and matches(.,'^TR\d')"/>    
            <xsl:when test="namespace-uri()='http://purl.org/dc/terms/' and matches(.,'TR\d')">
                <xsl:element name="ualid:trid">
                    <xsl:call-template name="string"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="text()[matches(.,'^SER')]">
                <xsl:element name="ualid:ser">
                    <xsl:call-template name="string"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="text()[matches(.,'(^\d*$)|(unicorn:)')]">
                <xsl:element name="ualid:unicorn">
                    <xsl:call-template name="string"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <!-- extract date from Dept of Anthro ids (file names)-->
            <xsl:when test="text()[matches(.,'^([12][09]\d{2})[\.-]\d{3}[\.-]\d{3}.*\.[Tt][Ii][Ff]')]">
                <xsl:element name="dcterms:created">
                    <xsl:value-of select="replace(., '^([12][09]\d{2})[\.-]\d{3}[\.-]\d{3}.*\.[Tt][Ii][Ff]', '$1')"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="text()[matches(.,'proquest:1969\.055\.001_d_\.[Tt][Ii][Ff]')]">
                <xsl:element name="dcterms:created">
                    <xsl:value-of select="replace(., 'proquest:1969\.055\.001_d_\.[Tt][Ii][Ff]', '1969')"/>
                </xsl:element>
            </xsl:when>
            <!-- other Dept of Anthro ids -->
            <xsl:when test="text()[matches(.,'(?:^\d{3}[-_]\d{3}-\d{3}.*\.[Tt][Ii][Ff])')]"/>
            <!-- Halpern ids -->
            <xsl:when test="text()[matches(.,'^(?:(?:A|\d{2,3})_.{2,4})|(?:halpern:nna)||(?:\d{3}_\d)|(?:[A-za-z]_\d{3}.?)')]"/>
            <xsl:when test="text()[matches(.,'proquest')]">
                <xsl:element name="ualid:proquest">
                    <xsl:call-template name="anyURI"/>
                    <xsl:apply-templates select="@*|node()"/>     
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="dcterms:identifier">
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    
    <!-- Theses -->
    <xsl:template match="*:contributor[namespace-uri()='http://www.ndltd.org/standards/metadata/etdms/1.0/']" priority="6">
        <xsl:choose>
            <xsl:when test="@role='advisor'">
                <xsl:element name="marcrel:ths">
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>  
            </xsl:when>
            <xsl:when test="@role='committeemember'">
                <xsl:element name="ualrole:thesiscommitteemember">
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>  
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="dcterms:contributor">
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="*:degree[namespace-uri()='http://www.ndltd.org/standards/metadata/etdms/1.0/']" priority="6">
        <xsl:for-each select="*:discipline">
            <xsl:element name="vivo:AcademicDepartment">
                <xsl:value-of select="replace(.,'Dept.','Department')"/>
            </xsl:element>
         </xsl:for-each>
        <xsl:for-each select="*:grantor">
            <xsl:element name="marcrel:dgg">
                <xsl:value-of select="normalize-space()"/>
            </xsl:element>
        </xsl:for-each>
        <xsl:for-each select="*:level">
            <xsl:element name="ualthesis:thesislevel">
                <xsl:value-of select="normalize-space()"/>
            </xsl:element>
        </xsl:for-each>
        <xsl:for-each select="*:name">
            <xsl:element name="bibo:ThesisDegree">
                <xsl:value-of select="normalize-space()"/>
            </xsl:element>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="*:dateaccepted" priority="6">
        <xsl:element name="dcterms:dateAccepted">
            <xsl:value-of select="normalize-space()"/>
        </xsl:element>
        <xsl:if test="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//rdf:Description[*:isMemberOfCollection[@*:resource[matches(.,'(?:uuid:d7cceac1-cdb6-4f6c-8f99-e46cd28c292b|uuid:7af76c0f-61d6-4ebc-a2aa-79c125480269)')]]] and not(//*:graduationdate)">        
            <xsl:element name="ualdate:graduationdate">
                <xsl:value-of select="normalize-space()"/>
            </xsl:element>
        </xsl:if>
    </xsl:template>
    
    
    
    <!-- eraterms -->
    <xsl:template match="*[namespace-uri()='http://era.library.ualberta.ca/eraterms']" priority="6">
        <xsl:if test="local-name()='graduationdate'">
            <xsl:element name="ualdate:graduationdate">
                <xsl:attribute name="xsi:type">
                    <xsl:text>gYearMonth</xsl:text>
                </xsl:attribute>
                <xsl:value-of select="normalize-space()"/>
            </xsl:element>
        </xsl:if>
        <xsl:if test="local-name()='specialization'">
            <xsl:element name="ualthesis:specialization">
                <xsl:value-of select="normalize-space()"/>
            </xsl:element>
        </xsl:if>
        <xsl:if test="local-name()='trid'">
            <xsl:element name="ualid:trid">
                <xsl:call-template name="string"/>
                <xsl:value-of select="normalize-space()"/>
            </xsl:element>
        </xsl:if>
    </xsl:template>
    
    
    
    <!-- Fix typo in original FOXML -->
    <xsl:template match="rdf:Description/*[namespace-uri()='http://era.library.ualbertaca/schema/definitions.xsd#']">
        <xsl:element name="{name()}" namespace="http://era.library.ualberta.ca/schema/definitions.xsd#">
            <xsl:apply-templates select="@* | node()"/>
        </xsl:element>
    </xsl:template>
    
    
    
    <!-- Fix datastream ID mismatch in original FOXML -->
    <xsl:template match="//foxml:datastream[@ID='DCQ']//foxml:datastreamVersion/@ID[contains(.,'DC.')]">
        <xsl:attribute name="ID">
            <xsl:value-of select="concat('DCQ', substring-after( ., 'DC'))"/>
        </xsl:attribute>
    </xsl:template>

    
    
    <!-- normalize initials spacing in creator and contributor names -->
    <!--<xsl:template match="//*:creator|//*:contributor">
        <xsl:choose>
            <xsl:when test="matches(.,'(\w+,\s?)([A-Z])\.\s?([A-Z])\.?\s?([A-Z]\.?\s?)?')">
                <xsl:analyze-string select="." regex="(\w+,\s?)([A-Z])\.\s?([A-Z])\.?\s?([A-Z]\.?\s?)?"></xsl:analyze-string>
                <xsl:element name="dcterms:{local-name()}">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="regex-group(1)"/>
                    <xsl:value-of select="regex-group(2)"/>
                    <xsl:text>. </xsl:text>
                    <xsl:value-of select="regex-group(3)"/>
                    <xsl:text>. </xsl:text>
                    <xsl:value-of select="regex-group(4)"/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="dcterms:{local-name()}">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>-->
    
    <!--<xsl:template match="//*:creator|//*:contributor">
        <xsl:for-each select=".">
            <xsl:analyze-string select="." regex="(\w+,\s?)([A-Z])\.\s?([A-Z])\.?\s?([A-Z]\.?\s?)?')">
                <xsl:matching-substring>
                    <xsl:value-of select="concat()"></xsl:value-of>
                </xsl:matching-substring>
            </xsl:analyze-string>
        </xsl:for-each>
    </xsl:template>-->
    
</xsl:stylesheet>