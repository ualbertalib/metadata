<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:mods="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="xs"
    version="3.0">
    
    <xsl:output method="text" indent="yes"/>
    
    
    <xsl:template match="*">        
        <xsl:for-each select="collection('/home/mparedes/peel/metadata/for_migration/?select=*.xml;recurse=yes')//*:mods">
            <xsl:if test="*:titleInfo[@type]">
                <xsl:value-of select="*:titleInfo/@type"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="*:titleInfo[@type]/*:title"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="*:titleInfo[@type]/*:subTitle"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="*:note/replace(text()[normalize-space()],'\t|\n|&#13;',' ')"/>
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="*:note/@type"/>
                <xsl:text>&#09;</xsl:text>
                <xsl:call-template name="url"/>
                <xsl:text>&#xa;</xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
    
    
    <xsl:template name="url">
        <xsl:variable name="id">
            <xsl:value-of select="*:recordInfo/*:recordIdentifier[not(@source='accession number')]"/>
        </xsl:variable>
        <xsl:variable name="collection">
            <xsl:value-of select="*:recordInfo/*:recordContentSource[not(@authority='local:person')]"/>
        </xsl:variable>
        <xsl:variable name="nid">
            <xsl:value-of select="*:identifier[@type='local:newspaper'][not(parent::*:relatedItem)]"/>
        </xsl:variable>
        <xsl:variable name="genre">
            <xsl:value-of select="*:genre[not(parent::*:relatedItem)]"/>
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
            <xsl:when test="*:recordInfo/*:recordContentSource[@authority='local:project'][contains(.,'mapsproject')]">
                <xsl:value-of select="concat($peelsite,'maps/',$id,'.html')"/>
            </xsl:when>
            <xsl:when test="$genre[contains(.,'newspaper')]">
                <xsl:value-of select="concat($peelsite,'newspapers/',$nid)"/>
            </xsl:when>
            <xsl:when test="$genre[contains(.,'postcard')]">
                <xsl:value-of select="concat($peelsite,'postcards/',$id,'.html')"/>
            </xsl:when>
            <xsl:when test="*:relatedItem//*:title[contains(.,'Magee')]">
                <xsl:value-of select="concat($peelsite,'magee/',$id,'.html')"/>
            </xsl:when>
            <xsl:when test="$id[starts-with(.,'P0')]">
                <xsl:value-of select="concat($peelsite,'bibliography/',$id,'.html')"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    
</xsl:stylesheet>