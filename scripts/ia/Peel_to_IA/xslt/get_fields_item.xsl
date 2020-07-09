<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xpath-default-namespace="http://www.loc.gov/mods/v3"
    xmlns="http://www.loc.gov/mods/v3"
    xmlns:mods="http://www.loc.gov/mods/v3"
    version="2.0">
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>

    <xsl:template match="mods:mods">
        <xsl:value-of select="//mods:titleInfo/mods:nonSort"/>
        <xsl:value-of select="//mods:title"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:languageTerm"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:dateIssued"/>
        <xsl:text>&#09;</xsl:text>
        
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
</xsl:stylesheet>