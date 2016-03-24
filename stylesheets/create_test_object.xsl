<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dcterms="http://purl.org/dc/terms/"
    exclude-result-prefixes="xs"
    version="2.0">
    
    
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="dc/*">
        <xsl:variable name="namesake">
            <xsl:value-of select="local-name()"/>
        </xsl:variable>
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:value-of select="concat(local-name(),../dcterms:type/substring(text(),1,3),count(preceding-sibling::*[local-name()=$namesake])+1)"/>
            <!-- Turn on to include text node -->
            <!--<xsl:value-of select="concat(local-name(),../dcterms:type/substring(text(),1,3),'$',./text())"/>-->            
        </xsl:copy>
    </xsl:template>
    
    
    
</xsl:stylesheet>