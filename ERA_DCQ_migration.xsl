<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:foxml="info:fedora/fedora-system:def/foxml#"
    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:ualterms="http://terms.library/ualberta.ca"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:eraterms="http://era.library.ualberta.ca/eraterms"
    xmlns:thesis="http://www.ndltd.org/standards/metadata/etdms/1.0/"
    exclude-result-prefixes="xs xd"
    version="3.0">
    
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p>*** In progress ***</xd:p>
            <xd:p>Created Mar 30, 2015</xd:p>
            <xd:p>paredeso@ualberta.ca</xd:p>
            <xd:p>This stylesheet updates ERA FOXML descriptive metadata for migration into HydraNorth</xd:p>
            <xd:p>Prefix and namespace changes documented at:
                <xd:ul>
<xd:li>https://docs.google.com/spreadsheets/d/1twJvO-oEPvaSYL8HSqEf892t6-a8wUEclGN6CgKgdsI/edit?usp=sharing</xd:li> <xd:li>https://docs.google.com/spreadsheets/d/1hSd6kf4ABm-m8VtYNyqfJGtiZG7bLJQ3fWRbF_nVoIw/edit?usp=sharing</xd:li>
                </xd:ul>
            </xd:p>
        </xd:desc>
    </xd:doc> 
    
    <xsl:output method="xml" encoding="UTF-8"/>
    <!--<xsl:preserve-space elements="*"/>-->
    <xsl:strip-space elements="dcterms:* dc:*"/>
    
    <xsl:variable name="newline">
        <xsl:text>&#xa;</xsl:text>
    </xsl:variable>
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Condition:
        When DCQ is present: copy XML structure but keep only last DCQ datastream, modifying data
        according to templates. Otherwise: copy XML structure, then call template to create new
        DCQ datastream based on last DC datastream -->    
    <xsl:template match="foxml:digitalObject">
            <xsl:choose>
                <xsl:when test="foxml:datastream[@ID='DCQ']">
                    <xsl:copy>
                        <xsl:apply-templates select="@*|node()"/>
                    </xsl:copy>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:copy>
                        <xsl:apply-templates select="@*|node()"/>
                        <xsl:call-template name="newDCQ"/>
                    </xsl:copy>                                                                
                </xsl:otherwise>
            </xsl:choose>
    </xsl:template>
    
    
    <!-- Keep only last DCQ datastream -->
    <xsl:template match="foxml:datastream[@ID='DCQ']">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:value-of select="$newline"/>
            <xsl:apply-templates select="foxml:datastreamVersion[last()]"/>
            <xsl:value-of select="$newline"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- New DCQ datastream based on last DC datastream: created with xsl instructions to control
        namespace decl. -->
    <xsl:template name="newDCQ">
        <xsl:element name="foxml:datastream" inherit-namespaces="no">
            <xsl:attribute name="CONTROL_GROUP">X</xsl:attribute>
            <xsl:attribute name="ID">DCQ</xsl:attribute>
            <xsl:attribute name="STATE">A</xsl:attribute>
            <xsl:attribute name="VERSIONABLE">true</xsl:attribute>
            <xsl:value-of select="$newline"/>
            <xsl:element name="foxml:datastreamVersion" inherit-namespaces="no">
                <xsl:attribute name="ID">DCQ.0</xsl:attribute>
                <xsl:attribute name="LABEL">Item Metadata</xsl:attribute>
                <xsl:attribute name="MIMETYPE">text/xml</xsl:attribute>
                <xsl:value-of select="$newline"/>
                <xsl:element name="foxml:xmlContent">
                    <xsl:value-of select="$newline"/>
                    <xsl:element name="dc">
                        <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
                        <xsl:namespace name="dc">http://purl.org/dc/elements/1.1/</xsl:namespace>
                        <xsl:namespace name="ualterms">http://terms.library/ualberta.ca</xsl:namespace>
                        <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
                        <xsl:apply-templates
                            select="//foxml:datastream[@ID='DC']/foxml:datastreamVersion[last()]//oai_dc:dc/node()"/>
                    </xsl:element><xsl:value-of select="$newline"/>
                </xsl:element><xsl:value-of select="$newline"/>
            </xsl:element><xsl:value-of select="$newline"/>
        </xsl:element><xsl:value-of select="$newline"/>
    </xsl:template>
    
    
    <!-- Update namespaces and apply templates -->
    <xsl:template match="//dc">
        <xsl:copy copy-namespaces="no">
            <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
            <xsl:namespace name="dc">http://purl.org/dc/elements/1.1/</xsl:namespace>
            <xsl:namespace name="ualterms">http://terms.library/ualberta.ca</xsl:namespace>
            <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Update namespaces, attributes and apply templates (DC datastream unchanged) -->    
    <xsl:template match="//oai_dc:dc">
        <xsl:copy copy-namespaces="no">
            <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
            <xsl:namespace name="dc">http://purl.org/dc/elements/1.1/</xsl:namespace>
            <xsl:namespace name="oai_dc">http://www.openarchives.org/OAI/2.0/oai_dc/</xsl:namespace>
            <xsl:namespace name="ualterms">http://terms.library/ualberta.ca</xsl:namespace>
            <xsl:attribute name="xsi:schemaLocation">http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd</xsl:attribute>
            <xsl:apply-templates select="@*|node()" mode="noChange"/>
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
    <!-- ambiguous rule match -->
    <xsl:template match="foxml:datastream[@ID='DCQ' or @ID='DC']/foxml:datastreamVersion[last()]/@SIZE|foxml:datastream[@ID='DCQ' or @ID='DC']/foxml:datastreamVersion[last()]/@xsi:type[.='dcterms:URI' or .='anyURI']"/>
    <!-- DCQ dc: strip @dc and @xsi:schemaLocation (formerly used for thesis) -->
    <xsl:template match="//dc/@dc|//dc/@xsi:schemaLocation"/>

    
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
            <xsl:when test="matches(.,'\w+\s*(?:[Aa]ge|[Cc]entury|[Pp]eriod|[Yy]ear|[Mm]onth|[Dd]ay|[Ww]ar|[Ww]inter|[Ss]pring|[Ss]ummer|[Ff]all|[Au]tumn|[Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay|[Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember|[Dd]ecember)')">
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
            <xsl:otherwise>
                <xsl:element name="dcterms:coverage">
                    <xsl:apply-templates select="@*"/>
                    <xsl:value-of select="normalize-space()"/>
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
    <!-- Comment out this section when updating object type for images -->
                <!--<xsl:when test="matches(.,'[Rr]esearch\s?[Mm]aterial')">
                    <xsl:text>Research Material</xsl:text>
                </xsl:when>-->
    <!-- Use when updating object type for images -->
                <xsl:when test="matches(.,'[Rr]esearch\s?[Mm]aterial')">
                    <xsl:text>Image</xsl:text>
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
    <!-- mpo: to do: process elements in the eraterms namespace; copy local-name() and replace eraterms with ualterms -->
    <!-- mpo: to do: there are more eraterms att values, copy string after ':' except for local attribute value in identifiers -->
    <!-- *:identifier/@xsi:type changes -->
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
                <xsl:element name="ualterms:fedora3uuid">
                    <xsl:call-template name="string"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="text()[contains(.,'handle')]">
                <xsl:element name="ualterms:fedora3handle">
                    <xsl:call-template name="anyURI"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="namespace-uri()='http://purl.org/dc/elements/1.1/' and matches(.,'^TR\d')"/>    
            <xsl:when test="namespace-uri()='http://purl.org/dc/terms/' and matches(.,'TR\d')">
                <xsl:element name="ualterms:trid">
                    <xsl:call-template name="string"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="text()[matches(.,'^SER')]">
                <xsl:element name="ualterms:ser">
                    <xsl:call-template name="string"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="text()[matches(.,'^\d*$')]">
                <xsl:element name="ualterms:unicorn">
                    <xsl:call-template name="string"/>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:when>
            <!--<xsl:when test="text()[contains(.,'proquest')]">
                <xsl:element name="ualterms:proquest">
                    <xsl:call-template name="anyURI"/>
                    <xsl:apply-templates select="@*|node()"/>     
                </xsl:element>
            </xsl:when>-->
            <!-- mpo: to do: add option for halpern ids -->
            <xsl:otherwise>
                <xsl:element name="dcterms:identifier">
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <!-- eraterms:trid number identifier ualterms:trid-->    
    <xsl:template match="//*:dc/*[local-name()='trid']" priority="6">
        <xsl:element name="ualterms:trid">
            <xsl:call-template name="string"/>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>
    
    
    <!-- Fix typo in original FOXML -->
    <xsl:template match="rdf:Description/*[namespace-uri()='http://era.library.ualbertaca/schema/definitions.xsd#']">
        <xsl:element name="{name()}" namespace="http://era.library.ualberta.ca/schema/definitions.xsd#">
            <xsl:apply-templates select="@* | node()"/>
        </xsl:element>
    </xsl:template>
    
    
    <!--<xsl:template match="//@*[. = 'eraterms:local']">
        <xsl:attribute name="{name()}">
            <xsl:text>ualterms:local</xsl:text>
        </xsl:attribute>
    </xsl:template>-->
    
    
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