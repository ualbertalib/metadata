<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:mets="http://www.loc.gov/METS/"
    xmlns:mods="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="xs"
    version="1.0">
    
    <xsl:output method="text" encoding="UTF-8"/>
    
    <xsl:variable name="pages" select="/mets:mets/mets:structMap[@TYPE='PHYSICAL']//mets:div[@TYPE='PAGE']"/>
    <xsl:variable name="articles" select="/mets:mets/mets:dmdSec"/>
    <xsl:variable name="logicalmap" select="/mets:mets/mets:structMap[@TYPE='LOGICAL']//mets:div[@TYPE='CONTENT']"/>

    <xsl:template match="/">
        <xsl:apply-templates select="$pages"/>        
    </xsl:template>
    
    <xsl:template match="mets:div[@TYPE='PAGE']">
        <!-- page-level div -->
        <xsl:variable name="pageid" select=".//mets:area[@BETYPE='IDREF']/@FILEID"/>
        
        <xsl:text>Page </xsl:text>
        <xsl:value-of select="@ORDERLABEL"/>
        <xsl:text>&#x0a;&#x0a;</xsl:text>
        
        <xsl:apply-templates select="$logicalmap/mets:div[@TYPE='ARTICLE'][.//mets:fptr[1]/mets:area[@FILEID = $pageid]]"/>
        <xsl:text>&#x0a;</xsl:text>
    </xsl:template>
    
    <xsl:template match="mets:div[@TYPE='ARTICLE']">
        <xsl:variable name="articleid" select="@DMDID"/>
        <xsl:apply-templates select="$articles[@ID = $articleid]/mets:mdWrap/mets:xmlData/mods:mods/mods:titleInfo"/>
    </xsl:template>
    
    <xsl:template match="mods:titleInfo">
        <xsl:text>- </xsl:text>
        <xsl:if test="mods:nonSort">
            <xsl:value-of select="mods:nonSort"/>
            <xsl:text> </xsl:text>
        </xsl:if>
        <xsl:value-of select="mods:title"/>
        <xsl:if test="mods:subTitle">
            <xsl:text>: </xsl:text>
            <xsl:value-of select="mods:subTitle"/>
        </xsl:if>
        <xsl:text>&#x0a;</xsl:text>
    </xsl:template>

</xsl:stylesheet>