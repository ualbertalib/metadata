<?xml version="1.0"?>
<!-- Stylesheet to create reports from mods metadata -->
<!--
    Includes adapted templates by Sven-S. Porst to get paths for all elements and attributes -  <porst@sub.uni-goettingen.de> https://gist.github.com/ssp/4511872
-->
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:mods="http://www.loc.gov/mods/v3">
    
    <xsl:output method="text"/>
    
    <xsl:template match="/*">
        <xsl:text>Path&#09;Content&#09;Source&#09;Id&#09;Form or Genre&#09;Occurrence&#09;MODS version&#xa;</xsl:text>
        <xsl:apply-templates select="*|@*"/>
    </xsl:template>
    
    <xsl:template match="mods:mods//*">        
        <xsl:for-each select="ancestor-or-self::*">
            <xsl:value-of select="concat('/',name(.))"/>
        </xsl:for-each>        
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="text()[normalize-space()]"/>        
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="source"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="id"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="formorgenre"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="occurrence"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="modsversion"/>
        <xsl:text>&#xa;</xsl:text>        
        <xsl:apply-templates select="*|@*"/>
    </xsl:template>
    
    <xsl:template match="mods:mods//@*">
        <xsl:for-each select="ancestor::*">
            <xsl:value-of select="concat('/',name(.))"/>
        </xsl:for-each>
        <xsl:text>/@</xsl:text>
        <xsl:value-of select="name(.)"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="source"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="id"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="formorgenre"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="occurrence"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="modsversion"/>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
    
    <xsl:template name="source">
        <xsl:value-of select="//mods:recordContentSource"/>        
    </xsl:template>
    
    <xsl:template name="id">
        <xsl:value-of select="//mods:recordIdentifier[not(@type='accession number')]"/>        
    </xsl:template>
    
    <!--<xsl:template name="accession">
        <xsl:value-of select="//mods:recordIdentifier[@type='accession number']"/>        
    </xsl:template>-->
    
    <xsl:template name="formorgenre">
        <xsl:value-of select="//mods:form | //mods:genre"/>        
    </xsl:template>
    
    <xsl:template name="modsversion">
        <xsl:value-of select="/mods:collection/@version"/>
    </xsl:template>
    
    <xsl:template name="occurrence">
        <xsl:variable name="namesake">
            <xsl:value-of select="local-name()"/>
        </xsl:variable>
        <xsl:value-of select="count(preceding-sibling::*[last() and local-name()=$namesake])+1"/>
    </xsl:template>
    
    
    
    <!-- add genre, count?, occurrence, mods version , id -->
    
    
</xsl:transform>