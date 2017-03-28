<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">

<!-- this for adding the 240 Tag to the IA marc records -->

    <xsl:output indent="yes" media-type="xml"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="@* | node()"> 
        <xsl:copy>
             <xsl:apply-templates select="@* | node()"/> 
        </xsl:copy>
    </xsl:template> 

    <xsl:template match="*:datafield[@tag=240]">
        <xsl:element name="datafield" namespace="http://www.loc.gov/MARC21/slim">
            <xsl:attribute name="tag">240</xsl:attribute>
            <xsl:attribute name="ind1">0</xsl:attribute>
            <xsl:attribute name="ind2">0</xsl:attribute>
            <!--<xsl:element name="subfield" namespace="http://www.loc.gov/MARC21/slim">
                <xsl:attribute name="code">a</xsl:attribute>
                <xsl:value-of select="*:subfield"/>
            </xsl:element>-->
            <xsl:for-each select="*:subfield">
                <xsl:copy>
                    <xsl:apply-templates select="@*|node()"/>
                </xsl:copy>
            </xsl:for-each>
        </xsl:element>
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/> 
        </xsl:copy>
    </xsl:template>
    
</xsl:stylesheet>
