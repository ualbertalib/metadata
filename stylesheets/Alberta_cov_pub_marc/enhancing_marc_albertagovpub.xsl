<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">

    <xsl:output indent="yes" media-type="xml"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:variable name="file_name">
        <xsl:value-of select="replace(base-uri(), 'revised_marc_titles', 'meta')"/>
    </xsl:variable>

    <xsl:variable name="meta_file">
        <xsl:value-of select="replace($file_name, '_marc', '_meta')"/>
    </xsl:variable>

    <xsl:template match="*:datafield[@tag = 245]/*:subfield[@code = 'a']">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:for-each select="document($meta_file)/metadata">
                <xsl:variable name="title">
                    <xsl:value-of select="//title"/>
                </xsl:variable>
                <xsl:choose>
                    <xsl:when test="*:date">
                        <xsl:variable name="date">
                            <xsl:value-of select="//date"/>
                        </xsl:variable>
                        <xsl:value-of select="concat($title, ' ', $date)"/>
                    </xsl:when>
                    <xsl:when test="*:volume">
                        <xsl:variable name="volume">
                            <xsl:value-of select="//volume"/>
                        </xsl:variable>
                        <xsl:value-of select="concat($title, ' ', $volume)"/>
                    </xsl:when>
                    <xsl:when test="*:title">
                        <xsl:value-of select="//title"/>
                    </xsl:when>
                </xsl:choose>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>

</xsl:stylesheet>
