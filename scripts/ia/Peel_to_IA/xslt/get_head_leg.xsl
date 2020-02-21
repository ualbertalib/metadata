<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:mets="http://www.loc.gov/METS/"
    xmlns:mods="http://www.loc.gov/mods/v3" exclude-result-prefixes="xs" version="2.0">

    <xsl:output method="text" encoding="UTF-8"/>

    <xsl:template match="/">
        <xsl:for-each
            select="/mets:mets/mets:structMap[@TYPE = 'LOGICAL']//mets:div[@TYPE = 'Page']">
            <xsl:variable name="page" select="@DMDID"/>
            <xsl:text>Page </xsl:text>
            <xsl:value-of select="$page"/>
            <xsl:text>:</xsl:text>
            <xsl:text>&#x0a;&#x0a;</xsl:text>
            <xsl:for-each select="mets:div[@TYPE = 'Article']">
                <xsl:variable name="art" select="@DMDID"/>
                <xsl:if
                    test="/mets:mets/mets:dmdSec[@ID = $art]/mets:mdWrap/mets:xmlData/mods:mods/mods:classification = 'article'">
                    <xsl:variable name="article"
                        select="/mets:mets/mets:dmdSec[@ID = $art]/mets:mdWrap/mets:xmlData/mods:mods/mods:titleInfo/mods:title"/>
                    <xsl:text> - </xsl:text>
                    <xsl:value-of select="$article"/>
                    <xsl:text>&#x0a;&#x0a;</xsl:text>
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
