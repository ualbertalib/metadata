<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">

    <xsl:output indent="yes" media-type="xml"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="@* | node()">
   
            <xsl:apply-templates select="@* | node()"/>
        
    </xsl:template>

    <xsl:variable name="file_name">
        <xsl:value-of
            select="replace(base-uri(), 'enhanced_marc_serials_monographs/enhanced_marc_serials_monographs_4', 'meta')"
        />
    </xsl:variable>

    <xsl:variable name="meta_file">
        <xsl:value-of select="replace($file_name, '_marc', '_meta')"/>
    </xsl:variable>

    <xsl:template match="*:datafield[@tag = 245]/*:subfield[@code = 'a'][1]">
        <root>
        <xsl:element name="title">
            <xsl:value-of select="."/>
        </xsl:element>
        <xsl:for-each select="document($meta_file)/metadata">
            <xsl:element name="publisher">
                <xsl:value-of select="//publisher"/>
            </xsl:element>
            <xsl:element name="creator">
                <xsl:value-of select="//creator"/>
            </xsl:element>
        </xsl:for-each>
        </root> 
    </xsl:template>

</xsl:stylesheet>
