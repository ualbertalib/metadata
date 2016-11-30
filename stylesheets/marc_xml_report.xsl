<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/*">
        <xsl:text>Path&#09;Indicators&#09;Content&#09;Full marc&#09;Resource URL&#09;Form or Genre&#09;Occurrence&#09;MODS version&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="docs"
        select="collection('../metadata-wrangling/internet_archive_coll/cius_books/?select=*;recurse=no')"/>


    <xsl:template match="*">
        <xsl:for-each select="$docs//*:controlfield | $docs//*:subfield">
            <xsl:choose>
                <xsl:when test="self::*:controlfield">
                    <xsl:value-of select="@tag"/>
                    <xsl:text>&#09;</xsl:text>                    
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="concat(../@tag,'$',./@code)"/>
                    <xsl:text>&#09;</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:value-of select="replace(concat(../@ind1,../@ind2),'\s','-')"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="./text()[normalize-space()]"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:call-template name="context"/>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="context">
        <xsl:variable name="id">
            <xsl:value-of select="ancestor-or-self::*:record/*:controlfield[@tag='001']"/>
        </xsl:variable>
        
        <!-- Full marc record -->
        <xsl:value-of select="concat('https://archive.org/download/',$id,'/',$id,'_marc.xml')"/>
        <xsl:text>&#09;</xsl:text>
        <!-- URL -->
        <xsl:value-of select="ancestor-or-self::*:record/*:datafield[@tag='856' and @ind2='1']/*:subfield[@code='u']"/>
        <xsl:text>&#xa;</xsl:text>
        <!-- Open Library -->
        <!-- Form or genre -->
        <!-- Ocurrence -->
    </xsl:template>
    
    
    
</xsl:transform>
