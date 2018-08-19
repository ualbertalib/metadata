<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:oai="http://www.openarchives.org/OAI/2.0/"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
    version="2.0">
    <xsl:output indent="yes"></xsl:output>
    <xsl:strip-space elements="*"/>
    <!-- This version of the stylsheet copies the records into the output without the oai record wrapper and header around each metadata record. -->
    <xsl:template match="oai:OAI-PMH">
        <xsl:element name="ldcMetadata">
            <xsl:apply-templates select="oai:ListRecords/oai:record[contains(oai:header/oai:identifier, 'oai:www.ldc.upenn.edu')]"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="oai:record">
        <xsl:apply-templates select="oai:metadata/olac:olac"/>
    </xsl:template>
    <xsl:template match="oai:metadata/olac:olac">
        <xsl:copy copy-namespaces="no">
            <xsl:namespace name="dc">http://purl.org/dc/elements/1.1/</xsl:namespace>
            <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
            <xsl:namespace name="olac">http://www.language-archives.org/OLAC/1.1/</xsl:namespace>
            <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
            <xsl:apply-templates mode="copy"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="node()" mode="copy">
        <xsl:copy copy-namespaces="no">
            <xsl:copy-of select="@*"/>
            <xsl:copy-of select="normalize-space(text())"/>
            <xsl:apply-templates select="*" mode="copy"/>
        </xsl:copy>        
    </xsl:template>
</xsl:stylesheet>