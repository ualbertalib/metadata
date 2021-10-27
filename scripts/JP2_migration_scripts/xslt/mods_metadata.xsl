<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:mods="http://www.loc.gov/mods/v3"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xpath-default-namespace="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    
    <xsl:template match="mods:mods">
        <xsl:value-of select="//mods:titleInfo/mods:nonSort"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo/mods:title"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo/mods:subTitle"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo/mods:partNumber"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo[@type]/mods:nonSort"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo[@type]/mods:title"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo[@type]/mods:subTitle"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo[@type]/mods:partNumber"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:typeOfResource"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:genre"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:language/ mods:languageTerm"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:originInfo/ mods:edition"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:dateIssued"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:dateIssued[@qualifier]"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//namePart"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//roleTerm"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//country"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//province"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//city"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//extent"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//publisher"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//issuance"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="//topic">
            <xsl:value-of select="."/><xsl:text>_--_--_</xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="//note">
            <xsl:value-of select="@type"/><xsl:text>::</xsl:text><xsl:value-of select="."/><xsl:text>_--_--_</xsl:text>            
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//nonSort"/>
        
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>