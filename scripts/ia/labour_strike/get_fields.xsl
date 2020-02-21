<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:mods="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    
    <xsl:template match="mods:mods">
        <xsl:value-of select="//mods:identifier"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:title"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:typeOfResource"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:namePart"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:roleTerm"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:country"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:province"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:city"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:extent"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:issuance"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:dateIssued"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:languageTerm"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="//mods:topic">
            <xsl:value-of select="."/><xsl:text>_--_--_</xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="//mods:note">
            <xsl:value-of select="@type"/><xsl:text>::</xsl:text><xsl:value-of select="."/><xsl:text>_--_--_</xsl:text>            
        </xsl:for-each>
        
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>