<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:variable name="docs" select="collection('file:///home/ddavoodi/Projects/metadata/Sam_Steel?select=*.xml;recurse=yes')"/>
    
    <xsl:template match="/">
        <xsl:for-each select="$docs">
        <xsl:for-each-group select="//*" group-by="local-name()">
            <xsl:variable name="name">
                <xsl:value-of select="local-name()"/>
            </xsl:variable>
            <xsl:call-template name="print-step"/>
                <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="count(current-group())"/>
                <xsl:text>&#xa;</xsl:text>
        </xsl:for-each-group>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="print-step">
        <xsl:text>/</xsl:text>
        <xsl:value-of select="name()"/>
        <xsl:text>[</xsl:text>
        <xsl:value-of select="1+count(preceding-sibling::*)"/>
        <xsl:text>]</xsl:text>
    </xsl:template>

</xsl:stylesheet>