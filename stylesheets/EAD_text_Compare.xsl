<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:variable name="docs" select="collection('file:///home/ddavoodi/Projects/metadata/Sam_Steel?select=*.xml;recurse=yes')"/>
    
    <xsl:template match="/">
        <xsl:for-each select="//p">
            <xsl:value-of select="normalize-space(.)"/>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>