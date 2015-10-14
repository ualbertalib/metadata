<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:dcterms="http://purl.org/dc/terms/"
    exclude-result-prefixes="xs xd"
    version="2.0">
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Sep 30, 2015</xd:p>
            <xd:p><xd:b>Author:</xd:b> mparedes</xd:p>
            <xd:p></xd:p>
        </xd:desc>
    </xd:doc>
    
    <xsl:output method="xml" encoding="UTF-8"/>
    
    
    <xsl:template match="node()|@*">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="*[local-name()='subject' or local-name()='spatial' or local-name()='temporal']">
        <xsl:for-each select=".[not(text()=preceding-sibling::*/text())]">
            <xsl:copy-of select="."/>
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>