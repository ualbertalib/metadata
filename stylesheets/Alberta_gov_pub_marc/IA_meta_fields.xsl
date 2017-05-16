<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:text>Title&#09;Publisher&#09;Creator&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="docs"     select="collection('../../metadata-wrangling/internet_archive_coll/albertagovernmentpublications/enhanced_marc_serials_monographs/meta?select=*marc.xml;recurse=yes')"/>

     <xsl:template match="*">
        <xsl:for-each select="$docs//*:root">
            <xsl:call-template name="context"/>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="context">
        <xsl:variable name="d">"</xsl:variable>
        <xsl:variable name="title">
            <xsl:value-of select="replace(//title, $d, '')"/>
        </xsl:variable>
        
        <xsl:value-of select="$title"/>
        <xsl:text>&#x9;</xsl:text>
        <xsl:value-of select="//publisher"/>
        <xsl:text>&#x9;</xsl:text>
        <xsl:value-of select="//creator"/>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
    
</xsl:transform>
