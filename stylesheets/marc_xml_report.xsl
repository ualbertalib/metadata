<?xml version="1.0"?>
<!-- Stylesheet to create reports from IA marc xml metadata -->
<!--
    Includes adapted templates by Sven-S. Porst to get paths for all elements and attributes - https://gist.github.com/ssp/4511872
-->
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/*">
        <xsl:text>Path&#09;Content&#09;URL&#09;Form or Genre&#09;Occurrence&#09;MODS version&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="docs"
        select="collection('/home/mparedes/main-metadata.git/metadata-wrangling/internet_archive_coll/cius_books/?select=*;recurse=no')"/>


    <xsl:template match="*">
        <xsl:for-each select="$docs//@tag">
            <xsl:value-of select="."/>
            <xsl:text>&#09;</xsl:text>
            <xsl:choose>
                <xsl:when test="ancestor::*:controlfield">                    
                    <xsl:value-of select="ancestor::*/text()[normalize-space()]"/>
                    <xsl:text>&#09;</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="ancestor::*/*:subfield"/>
                    <xsl:text>&#09;</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>



</xsl:transform>
