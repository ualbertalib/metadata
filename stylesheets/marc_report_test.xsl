<?xml version="1.0"?>
<!-- Stylesheet to create reports from IA marc xml metadata -->
<!--
    Includes adapted templates by Sven-S. Porst to get paths for all elements and attributes - https://gist.github.com/ssp/4511872
-->
<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0" xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    
    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="/*">
        <xsl:text>Path&#09;Content&#09;URL&#09;Form or Genre&#09;Occurrence&#09;MODS version&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
    
    <!--<xsl:template match="//*:mods">
        <xsl:apply-templates/>
    </xsl:template>-->
    
    <xsl:template match="*" name="elements">        
        <xsl:for-each select="ancestor-or-self::*">
            <xsl:value-of select="concat('/',local-name(.))"/>
        </xsl:for-each>        
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="replace(text()[normalize-space()],'\t|\n|&#13;',' ')"/>        
        <xsl:text>&#09;</xsl:text>
        <!--<xsl:call-template name="context"/>-->
        <xsl:apply-templates select="*|@*"/>
    </xsl:template>
    
    <!--<xsl:template match="@*" name="attributes">
        <xsl:for-each select="ancestor::*">
            <xsl:value-of select="concat('/',local-name(.))"/>
        </xsl:for-each>
        <xsl:text>/@</xsl:text>
        <xsl:value-of select="local-name(.)"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select=".[normalize-space()]"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="context"/>
    </xsl:template>
    
    <xsl:template name="context">
        <xsl:call-template name="url"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="formorgenre"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="occurrence"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:call-template name="modsversion"/>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>-->
    
    <!--<xsl:template name="source">
        <xsl:value-of select="ancestor-or-self::*:mods//*:recordContentSource"/>        
    </xsl:template>-->
    
    <!--<xsl:template name="id">
        <xsl:value-of select="ancestor-or-self::*:mods/*:identifier[@type='local:newspaper'] | *:mods/*:recordInfo/*:recordIdentifier[not(@type='accession number')]"/>
    </xsl:template>-->
    
    <xsl:template name="url">
        <xsl:variable name="id">
            <xsl:value-of select="ancestor-or-self::*:mods/*:recordInfo/*:recordIdentifier[not(@source='accession number')]"/>
        </xsl:variable>
        <xsl:variable name="collection">
            <xsl:value-of select="ancestor-or-self::*:mods/*:recordInfo/*:recordContentSource[not(@authority='local:person')]"/>
        </xsl:variable>
        <xsl:variable name="nid">
            <xsl:value-of select="ancestor-or-self::*:mods/*:identifier[@type='local:newspaper']"/>
        </xsl:variable>
        <xsl:variable name="genre">
            <xsl:value-of select="ancestor-or-self::*:mods//*:genre[not(parent::*:relatedItem)]"/>
        </xsl:variable>
        <xsl:variable name="peelsite">
            <xsl:text>http://peel.library.ualberta.ca/</xsl:text>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test="$collection[contains(.,'Royal')]">
                <xsl:value-of select="concat('http://royal.library.ualberta.ca/royalcommissions/dspCitation.cfm?ID=',$id)"/>
            </xsl:when>
            <xsl:when test="$collection[contains(.,'Folklore')]">
                <xsl:value-of select="concat('http://folklore.library.ualberta.ca/dspCitation.cfm?ID=',$id)"/>
            </xsl:when>
            <xsl:when test="ancestor-or-self::*:mods/*:recordInfo/*:recordContentSource[@authority='local:project'][contains(.,'mapsproject')]">
                <xsl:value-of select="concat($peelsite,'maps/',$id,'.html')"/>
            </xsl:when>
            <xsl:when test="$genre[contains(.,'newspaper')]">
                <xsl:value-of select="concat($peelsite,'newspapers/',$nid)"/>
            </xsl:when>
            <xsl:when test="$genre[contains(.,'postcard')]">
                <xsl:value-of select="concat($peelsite,'postcards/',$id,'.html')"/>
            </xsl:when>
            <xsl:when test="ancestor-or-self::*:mods/*:relatedItem//*:title[contains(.,'Magee')]">
                <xsl:value-of select="concat($peelsite,'magee/',$id,'.html')"/>
            </xsl:when>
            <xsl:when test="$id[starts-with(.,'P0')]">
                <xsl:value-of select="concat($peelsite,'bibliography/',$id,'.html')"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <!--<xsl:template name="accession">
        <xsl:value-of select="//*:recordIdentifier[@type='accession number']"/>        
    </xsl:template>-->
    
    <xsl:template name="formorgenre">
        <xsl:value-of select="ancestor-or-self::*:mods//*:genre[not(parent::*:relatedItem)] | ancestor-or-self::*:mods//*:form[not(parent::*:relatedItem)]"/>        
    </xsl:template>
    
    <xsl:template name="modsversion">
        <xsl:variable name="version">
            <xsl:value-of select="substring-after(/*/@xsi:schemaLocation,'http://www.loc.gov/standards/mods/v3/mods-')"/>
        </xsl:variable>
        <xsl:choose>
            <xsl:when test="ancestor-or-self::*:mods/@version">
                <xsl:value-of select="ancestor-or-self::*:mods/@version"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="substring-before($version,'.xsd')"/>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    <xsl:template name="occurrence">
        <xsl:variable name="namesake">
            <xsl:value-of select="local-name(.)"/>
        </xsl:variable>
        <xsl:value-of select="count(preceding-sibling::*[last() and local-name()=$namesake])+1+count(following-sibling::*[last() and local-name()=$namesake])"/>
    </xsl:template>
    
    
</xsl:transform>
