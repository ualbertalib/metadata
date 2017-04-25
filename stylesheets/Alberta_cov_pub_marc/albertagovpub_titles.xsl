<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    
    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="/">
        <xsl:text>title&#09;file_name&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:variable name="docs"     select="collection('../metadata-wrangling/internet_archive_coll/albertagovernmentpublications/?select=Marc245_a.xml;recurse=yes')"/>
    
    <xsl:template match="*">
        <xsl:for-each select="$docs//*:description | $docs//*:systemID">
            <xsl:choose>
                <xsl:when test="self::*:description">
                    <xsl:value-of select="."/>
                </xsl:when>
                <xsl:when test="self::*:systemID">
                    <xsl:text>&#09;</xsl:text>
                    <xsl:variable name="file_id">
                        <xsl:value-of select="subsequence(reverse(tokenize(text(),'/')), 1, 1)"/>
                    </xsl:variable>
                    <xsl:value-of select="replace($file_id, '_marc.xml', '')"/>
                    <xsl:text>&#13;&#10;</xsl:text>
                </xsl:when>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    
    
   
    
    
</xsl:transform>
