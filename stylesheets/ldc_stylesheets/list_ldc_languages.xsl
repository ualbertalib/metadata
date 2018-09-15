<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:oai="http://www.openarchives.org/OAI/2.0/"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/" version="2.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">    
    <xsl:output indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="ldcMetadata">
        <xsl:copy copy-namespaces="no">
            <xsl:namespace name="dc">http://purl.org/dc/elements/1.1/</xsl:namespace>
            <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
            <xsl:apply-templates select="olac:olac/dc:language"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="olac:olac/dc:language">
        <xsl:element name="olac">
            <xsl:call-template name="brief"/>
        </xsl:element>
    </xsl:template>
    <xsl:template name="brief">
        <xsl:element name="dc:language">
            <xsl:value-of select="."/>            
        </xsl:element>
        <xsl:element name="dcterms:language">
            <xsl:value-of select="./@olac:code"/>            
        </xsl:element>
        <xsl:element name="dc:identifier">
            <xsl:value-of select="../dc:identifier[starts-with(., 'LDC')]"/>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
