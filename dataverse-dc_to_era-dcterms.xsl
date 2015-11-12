<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/" xmlns:georss="http://www.georss.org/georss/"
    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="oai_dc:dc">
        <xsl:element name="oai_dc:dcterms" inherit-namespaces="no">
            <xsl:namespace name="dcterms" xpath-default-namespace="http://purl.org/dc/terms/"
                >http://purl.org/dc/terms/</xsl:namespace>
            <xsl:namespace name="georss">http://www.georss.org/georss/</xsl:namespace>
            <xsl:apply-templates/>
            <xsl:call-template name="description"/>
            <xsl:call-template name="type"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="dc:*">
        <!-- This test excludes elements that are processed through named templates or omitted. -->
        <xsl:choose>
            <xsl:when test="name() = 'dc:rights'"/>
            <xsl:when test="name() = 'dc:description'"/>
            <xsl:when test="name() = 'dc:type'"/>
            <xsl:otherwise>
                <xsl:element name="dcterms:{local-name()}">
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="dc:date">
        <xsl:element name="dcterms:created">
            <xsl:apply-templates select="@* | node()"/>
        </xsl:element>
    </xsl:template>
    <!-- Several Dataverse fields are mapped to coverage. This template processes the ones selected for output. All others are excluded. -->
    <xsl:template match="dc:coverage">
        <xsl:choose>
            <xsl:when test="starts-with(., 'Time Period Covered')">
                <xsl:element name="dcterms:temporal">
                    <xsl:value-of select="substring-after(., 'Time Period Covered: ')"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="starts-with(., 'Country/Nation')">
                <xsl:element name="dcterms:spatial">
                    <xsl:value-of select="substring-after(., 'Country/Nation: ')"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="starts-with(., 'Geographic Coverage')">
                <xsl:element name="dcterms:spatial">
                    <xsl:value-of select="substring-after(., 'Geographic Coverage: ')"/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="starts-with(., 'Geographic Bounding')">
                <xsl:analyze-string
                    select="substring-before(substring-after(normalize-space(.), 'Geographic Bounding: '), ' South Latitude')"
                    regex="^(\-?\d{{0,3}}\.\d*?)(\s[A-Za-z]+\s[A-Za-z]+,)(\-?\d{{0,3}}\.\d*?)(\s[A-Za-z]+\s[A-Za-z]+,\s)(\-?\d{{0,2}}\.\d*?)(\s[A-Za-z]+\s[A-Za-z]+,\s)(\-?\d{{0,2}}\.\d*?)$">
                    <xsl:matching-substring>
                        <xsl:element name="georss:box">
                            <!-- South Latitude -->
                            <xsl:value-of select="regex-group(7)"/>
                            <xsl:text> </xsl:text>
                            <!-- West Longitude -->
                            <xsl:value-of select="regex-group(3)"/>
                            <xsl:text> </xsl:text>
                            <!-- North Latitude -->
                            <xsl:value-of select="regex-group(5)"/>
                            <xsl:text> </xsl:text>
                            <!-- East Longitude -->
                            <xsl:value-of select="regex-group(1)"/>
                        </xsl:element>
                    </xsl:matching-substring>
                    <xsl:non-matching-substring>
                        <xsl:element name="dcterms:spatial">
                            <xsl:value-of select="."/>
                        </xsl:element>
                    </xsl:non-matching-substring>
                </xsl:analyze-string>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <!-- Each Dataverse record includes an instance of dc:description that contains a formatted citation for the resource, and which is excluded from the output. -->
    <!-- The value of dc:type comes from a free text field that describes the kind of data. -->
    <xsl:template match="dc:type" mode="description">                
        <xsl:text>Kind of data: </xsl:text>
        <xsl:value-of select="."/>
    </xsl:template>
    <xsl:template match="dc:description[starts-with(., 'Citation')]" mode="description"/>
    <xsl:template match="dc:description" mode="description">
        <xsl:apply-templates select="@* | node()"/>
    </xsl:template>
    <xsl:template name="description">
        <xsl:element name="dcterms:description">
            <xsl:text>This item is a resource in the University of Alberta Libraries' Dataverse Network. Access this item in Dataverse by clicking on the DOI link.</xsl:text>
            <xsl:if test="dc:type or dc:description[2]">
                <xsl:text> | </xsl:text>
            </xsl:if>
            <xsl:apply-templates select="dc:type" mode="description"/>
            <xsl:if test="dc:type and dc:description[2]">
                <xsl:text> | </xsl:text>
            </xsl:if>
            <xsl:apply-templates select="dc:description" mode="description"/>
        </xsl:element>
    </xsl:template>
    <!-- All resources from Dataverse are assigned the controlled value 'Dataset'-->
    <xsl:template name="type">
        <xsl:element name="dcterms:type" inherit-namespaces="no">Dataset</xsl:element>
    </xsl:template>
</xsl:stylesheet>
