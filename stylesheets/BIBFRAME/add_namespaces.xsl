<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes" />
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="*" priority="1">
        <xsl:element name="{local-name()}" namespace="http://www.loc.gov/MARC21/slim">
            <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>