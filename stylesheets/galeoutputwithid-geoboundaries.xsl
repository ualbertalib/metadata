<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:mods="http://www.loc.gov/mods/v3"
    xmlns:dc="http://purl.org/dc/elements/1.1/" version="3.0">

    <xsl:output method="text"/>

    <xsl:template match="*">
        <xsl:text>Subjects</xsl:text>
        <xsl:text>&#9;</xsl:text>
        <xsl:text>Coverage</xsl:text>
        <xsl:text>&#9;</xsl:text>
        <xsl:text>Description</xsl:text>
        <xsl:text>&#9;</xsl:text>
        <xsl:text>Language</xsl:text>
        <xsl:text>&#9;</xsl:text>
        <xsl:text>Color</xsl:text>
        <xsl:text>&#9;</xsl:text>
        <xsl:text>imagecount</xsl:text>
        <xsl:text>&#9;</xsl:text>
        <xsl:text>PSMID</xsl:text>
        <xsl:text>&#9;</xsl:text>
        <xsl:text>IDnumber</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:for-each select="collection('/home/mariana/Downloads/Gale_test?select=*.xml;recurse=yes')//*:manuscript">
            <xsl:apply-templates select="//*:geoBoundary/*" mode="subjects"/>
            <xsl:text>&#9;</xsl:text>
            <xsl:apply-templates select="//*:geoBoundary"/>
            <xsl:text>&#9;</xsl:text>
            <xsl:apply-templates select="//*:para"/>
            <xsl:text>&#9;</xsl:text>
            <xsl:apply-templates select="//*:msLanguage/@ocr"/>
            <xsl:text>&#9;</xsl:text>
            <xsl:apply-templates select="//*:msImage/@colorimage"/>
            <xsl:text>&#9;</xsl:text>
            <xsl:apply-templates select="//*:totalImages"/>
            <xsl:text>&#9;</xsl:text>
            <xsl:apply-templates select="//*:PSMID"/>            
            <xsl:text>&#9;</xsl:text>
            <xsl:apply-templates select="//*:msNumber"/>            
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="//*:geoBoundary/*" mode="subjects">
        <xsl:value-of select="normalize-space(.)"/>
        <xsl:call-template name="separator"/>
    </xsl:template>
    
    <xsl:template match="*:geoBoundary">
        <xsl:variable name="position">
            <xsl:value-of select="position()"/>
        </xsl:variable>
        <!--<xsl:value-of select="text()"/>-->
        <xsl:value-of select="concat('Geoboundary ',$position, ': ')"/>
        <xsl:apply-templates select="descendant::*" mode="geoboundaries"/>
    </xsl:template>
    
    
    <xsl:template match="//*:geoBoundary/*" mode="geoboundaries">
        <xsl:choose>
            <xsl:when test="self::*:northwestPoint">
                <xsl:text>Northwest Point: </xsl:text>
                <xsl:call-template name="value"/>
            </xsl:when>
            <xsl:when test="self::*:northeastPoint">
                <xsl:text>Northeast Point: </xsl:text>
                <xsl:call-template name="value"/>
            </xsl:when>
            <xsl:when test="self::*:southwestPoint">
                <xsl:text>Southwest Point: </xsl:text>
                <xsl:call-template name="value"/>
            </xsl:when>
            <xsl:when test="self::*:southeastPoint">
                <xsl:text>Southeast Point: </xsl:text>
                <xsl:call-template name="value"/>
            </xsl:when>
        </xsl:choose>
        <!--<xsl:value-of select="normalize-space(.)"/>-->
        <!--<xsl:text>. Coordinates: </xsl:text>
        <xsl:value-of select="*:northwestPoint/@latitude"/>
        <xsl:text>:</xsl:text>
        <xsl:value-of select="*:northwestPoint/@longitude"/>-->
    </xsl:template>

    
    <!--<xsl:template match="//*:southeastPoint/@longitude">
        <xsl:value-of select="."/>
        <xsl:call-template name="separator"/>
    </xsl:template>-->
    
    
    <xsl:template match="//*:para">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="//*:msLanguage/@ocr">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="//*:msImage/@colorimage">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="//*:totalImages">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="//*:PSMID">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template match="//*:msNumber">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <xsl:template name="separator">
        <xsl:if test="position() != last()">
            <xsl:text> | </xsl:text>
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="value">
        <xsl:value-of select="normalize-space(.)"/>
        <xsl:value-of select="concat(' (',./@latitude, ':', ./@longitude, ')')"/>
        <xsl:choose>
            <xsl:when test="position() != last()">
                <xsl:text>; </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>.</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
