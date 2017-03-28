<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">

    <!-- this for merging all 240 subfields into $a in the IA marc records -->

    <xsl:output indent="yes" media-type="xml"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="*:datafield[@tag = 240]/*:subfield">
        <xsl:element name="subfield" namespace="http://www.loc.gov/MARC21/slim">
            <xsl:attribute name="code">a</xsl:attribute>
            <xsl:apply-templates select="node()"/>
            <xsl:text>/ </xsl:text>
            <xsl:apply-templates select="following-sibling::*/node()"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="*:datafield[@tag = 240]/*[position() > 1]"/>

</xsl:stylesheet>
