<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:foxml="info:fedora/fedora-system:def/foxml#"
    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:ualterms="http://terms.library.ualberta.ca"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:eraterms="http://era.library.ualberta.ca/eraterms"
    xmlns:thesis="http://www.ndltd.org/standards/metadata/etdms/1.0/"
    exclude-result-prefixes="xs xd"
    version="3.0">
     
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Add missing namespace declaration in original FOXML-->    
    <xsl:template match="foxml:datastream[@ID='DCQ']">
        <xsl:copy>
            <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <!-- Fix double-nested DCQ datastreams in original FOXML-->
    <xsl:template match="//foxml:datastream[@ID='DCQ']//foxml:xmlContent[descendant::foxml:xmlContent]">
        <xsl:apply-templates select="descendant::foxml:xmlContent"/>
    </xsl:template>
    
    
    <!-- Fix namespace typo in original FOXML -->
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
    
    <!-- Delete identifier elements (without namespace prefix) in DCQ -->
    <xsl:template match="//foxml:datastream[@ID='DCQ']/foxml:datastreamVersion[last()]/identifier[not(node())]"/>
    
</xsl:stylesheet>