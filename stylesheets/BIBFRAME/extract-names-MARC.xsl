<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    
    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="/">
        <xsl:text>Field/subfield&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:variable name="docs" select="collection('../../metadata-wrangling/BIBFRAME/2015Imprint/2015Imprints-enrichedMarc?select=*.xml;recurse=yes')"/>
    
    <xsl:template match="*">
        <xsl:for-each select="$docs//*:subfield">
            <xsl:variable name="test">
                 <xsl:value-of select="."/>
            </xsl:variable>
            <xsl:if test="contains($test, 'http://id.loc.gov/authorities/name')">
                <xsl:for-each select="parent::*/node()">
                    <xsl:value-of select="."/>
                    <xsl:text> | </xsl:text>
                </xsl:for-each>
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="../@tag"/>
                <xsl:text>&#xa;</xsl:text>
            </xsl:if>
            
        </xsl:for-each>
        
    </xsl:template>
    
</xsl:transform>
