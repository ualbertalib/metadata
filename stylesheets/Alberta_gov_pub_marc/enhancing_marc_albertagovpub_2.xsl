<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">

    <!-- this for enhancing the IA marc records; adding tag 240 which includes tag 245$a and tag 245$b, adding "date" or "vol" (from meta.xml files downloaded from Internet Archives) to tag 245$a  for serials, adding tag 250$a to tag 245$a for monographs-->

    <xsl:output indent="yes" media-type="xml"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:variable name="file_name">
        <xsl:value-of select="replace(base-uri(), 'marc', 'meta')"/>
    </xsl:variable>

    <xsl:variable name="doc_name">
        <xsl:value-of select="subsequence(reverse(tokenize(base-uri(), '/')), 1, 1)"/>
    </xsl:variable>

    <xsl:variable name="meta_file">
        <xsl:value-of select="replace($file_name, '_marc', '_meta')"/>
    </xsl:variable>

    <xsl:template match="*:datafield[@tag = 245]">
        <xsl:element name="datafield" namespace="http://www.loc.gov/MARC21/slim">
            <xsl:attribute name="tag">240</xsl:attribute>
            <xsl:attribute name="ind1">
                <xsl:value-of select="@ind1"/>
            </xsl:attribute>
            <xsl:attribute name="ind2">
                <xsl:value-of select="@ind2"/>
            </xsl:attribute>
            <xsl:element name="subfield" namespace="http://www.loc.gov/MARC21/slim">
                <xsl:attribute name="code">a</xsl:attribute>
                <xsl:variable name="sub_a">
                    <xsl:value-of select="*:subfield[@code = 'a']"/>
                </xsl:variable>
                <xsl:variable name="sub_b">
                    <xsl:value-of select="*:subfield[@code = 'b']"/>
                </xsl:variable>
                <xsl:choose>
                    <xsl:when test="$sub_b = ''">
                        <xsl:value-of select="$sub_a"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="concat($sub_a, ' / ', $sub_b)"/>
                    </xsl:otherwise>
                </xsl:choose>         
            </xsl:element>
        </xsl:element>
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="*:datafield[@tag = 245]/*:subfield[@code = 'a']">

        <xsl:variable name="bib">
            <xsl:value-of select="substring(ancestor-or-self::*:record/*:leader, 8, 1)"/>
        </xsl:variable>

        <xsl:variable name="edition">
            <xsl:value-of
                select="ancestor-or-self::*:record/*:datafield[@tag = 250]/*:subfield[@code = 'a']"
            />
        </xsl:variable>
        
        <xsl:variable name="frequency">
            <xsl:value-of
                select="ancestor-or-self::*:record/*:datafield[@tag = 310]/*:subfield[@code = 'a']"
            />
        </xsl:variable>

        <xsl:choose>
            <xsl:when test="$bib = 's'">
                <xsl:copy>
                    <xsl:apply-templates select="@*"/>
                    <xsl:for-each select="document($meta_file)/metadata">
                        <xsl:variable name="volume">
                            <xsl:value-of select="//volume"/>
                        </xsl:variable>
                        <xsl:variable name="year">
                            <xsl:value-of select="//year"/>
                        </xsl:variable>
                        <xsl:variable name="date">
                            <xsl:value-of select="//date"/>
                        </xsl:variable>
                        <xsl:variable name="title">
                            <xsl:value-of select="//title"/>
                        </xsl:variable>
                        <xsl:choose>
                            <xsl:when test="$frequency = '' and $date = '' and $year = '' and $volume = ''">
                                <xsl:value-of select="//title"/>
                            </xsl:when>
                            <xsl:when test="$frequency = 'Annual' or $frequency = 'Annual.' or $frequency = 'Annuel' or $frequency = 'Annual,' or $frequency = 'Annuel.' or $frequency = 'annual' or $frequency = 'Annual (irregular)'">  
                                <xsl:choose>
                                    <xsl:when test="$date != ''">
                                        <xsl:value-of select="concat($title, ' / ', $date)"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="concat($title, ' / ', $volume)"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:choose>
                                    <xsl:when test="$volume != ''">
                                        <xsl:value-of select="concat($title, ' / ', $volume)"/>
                                    </xsl:when>
                                    <xsl:when test="$year != ''">
                                        <xsl:value-of select="concat($title, ' / ', $year)"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="concat($title, ' / ', $date)"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </xsl:copy>
            </xsl:when>

            <xsl:when test="$bib = 'm'">
                <xsl:copy>
                    <xsl:apply-templates select="@*"/>
                    <xsl:for-each select="document($meta_file)/metadata">
                        <xsl:variable name="title">
                            <xsl:value-of select="//title"/>
                        </xsl:variable>
                        <xsl:choose>
                            <xsl:when test="$edition = ''">
                                <xsl:value-of select="$title"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="concat($title, ' / ', $edition)"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </xsl:copy>
            </xsl:when>

        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
