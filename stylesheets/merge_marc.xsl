<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:marcrel="http://id.loc.gov/vocabulary/relators"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    version="3.0">
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    
    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="marc:record">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
            <xsl:call-template name="catkey"/>
        </xsl:copy>
    </xsl:template>
 
    
    <xsl:template name="catkey">
        <xsl:variable name="filename" select="concat('/home/mparedes/main-metadata.git/metadata-wrangling/alberta_government_publications/test/',//marc:controlfield[@tag='001'],'_marc.xml')"/>
        <xsl:element name="controlfield" namespace="http://www.loc.gov/MARC21/slim">
            <xsl:attribute name="tag">091</xsl:attribute>
            <xsl:value-of select="document($filename)//marc:controlfield[@tag='001']"/>
        </xsl:element>
    </xsl:template>
    
    
</xsl:stylesheet>
