<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:mods="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    
    <xsl:template match="mods:mods">
        <xsl:value-of select="//mods:titleInfo/mods:title"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo/mods:subTitle"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:titleInfo[@type='alternative']/mods:title"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:typeOfResource"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select= "//mods:namePart">
            <xsl:value-of select="."/>
            <xsl:text>_--_--_</xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:placeTerm[@type='text']"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="//mods:genre">
            <xsl:value-of select="."/><xsl:text>_--_--_</xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="//mods:subject">
            <xsl:choose>
                <xsl:when test="mods:topic">
                    <xsl:value-of select="mods:topic"/>
                    <xsl:text>--</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text></xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="mods:geographic">
                    <xsl:value-of select="mods:geographic"/>
                    <xsl:text>--</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text></xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            <!--<xsl:choose>
                <xsl:when test="mods:temporal">
                    <xsl:value-of select="mods:temporal"/>
                </xsl:when>>
            </xsl:choose>-->
            <xsl:text>_--_--_</xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:publisher"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:extent"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:issuance"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:dateIssued"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:languageTerm"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:scale"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="//mods:note[@type='public']">
            <xsl:value-of select="."/><xsl:text>_--_--_</xsl:text>            
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="//mods:coordinates"/>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>