<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dcterms="http://purl.org/dc/terms/"
    exclude-result-prefixes="xs"
    version="2.0">
    
    
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:template match="@*|node()">
        <xsl:copy copy-namespaces="yes">
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="*:title | *:namePart | *:publisher | *:extent | *:topic | *:temporal | *:geographic | *:abstract | *:accessCondition | *:tableOfContents | *:note">
        <xsl:variable name="namesake">
            <xsl:value-of select="local-name()"/>
        </xsl:variable>
        <xsl:copy copy-namespaces="yes">
            <xsl:apply-templates select="@*"/>
            <xsl:choose>
                <xsl:when test="local-name()='namePart'">
                    <xsl:variable name="role">
                        <xsl:value-of select="parent::*//*:roleTerm[@type='text']"/>
                    </xsl:variable>
                    <xsl:value-of select="concat($role,count(parent::*/preceding-sibling::*[local-name()='name'][//*:roleTerm[@type='text' and text()=$role]])+1)"/>
                </xsl:when>
                <xsl:when test="local-name()='abstract' or local-name()='accessCondition' or local-name()='tableOfContents' or local-name()='note'">
                    <xsl:value-of select="concat(local-name(),count(preceding-sibling::*[local-name()=$namesake])+1,'$',./text())"/>
                </xsl:when>
                <xsl:when test="local-name()='publisher'">
                    <xsl:value-of select="concat(local-name(),count(preceding-sibling::*[local-name()=$namesake])+1)"/>
                </xsl:when>
                <xsl:when test="parent::*[local-name()='subject']">
                    <xsl:value-of select="concat(local-name(),count(parent::*/preceding-sibling::*/*[local-name()=$namesake])+1)"/>
                </xsl:when>
            </xsl:choose>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- title | publisher | extent | topic | temporal | geographic
        <xsl:template match="*:genre | *:language | *:dateIssued | *:dateCreated  | *:name" priority="2">
        <xsl:copy-of select="."/>
    </xsl:template>-->
    
    <!-- change dates
        createdDate - //foxml:property[@NAME="info:fedora/fedora-system:def/model#createdDate"]/@VALUE
        lastModifiedDate - //foxml:property[@NAME="info:fedora/fedora-system:def/model#lastModifiedDate"]/@VALUE
        embargoedDate -//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//*:embargoedDate
        workflowDate -//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//*:workflowDate
        audit dates - audit:date
        all datastream created dates with sequential dates - //datastreamVersion/@CREATED
         -->
    <!-- change state to test visibility - //foxml:property[@NAME="info:fedora/fedora-system:def/model#state"]/@VALUE -->
    <!-- change PID and references -->
    <!-- change collection memberships -->
    
</xsl:stylesheet>