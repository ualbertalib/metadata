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
            <xsl:call-template name="rights"/>
            <xsl:call-template name="type"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="dc:*">
        <xsl:choose>
            <!-- This test excludes dc:rights from processing so element instances are only processed once through the 'rights' template. -->
            <xsl:when test="name() = 'dc:rights'">                
            </xsl:when>
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
<!-- Instances of dc:description that contain a formatted citation for the resource are excluded from the output. -->
<!-- Other instances of dc:description are drawn from the 'Abstract' field in Dataverse and so are mapped to dcterms:abstract. -->    
    <xsl:template match="dc:description">
        <xsl:choose>
            <xsl:when test="starts-with(., 'Citation')"/>
            <xsl:otherwise>
                <xsl:element name="dcterms:abstract">
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- value in dc:type comes from a free text field describing the kind of data, so it is mapped to an instance of the description field. -->
    <xsl:template match="dc:type">
        <xsl:element name="dcterms:description">
            <xsl:value-of select="."/>
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
                <xsl:analyze-string select="substring-before(substring-after(normalize-space(.), 'Geographic Bounding: '), ' South Latitude')" regex="^(\-?\d{{0,3}}\.\d*?)(\s[A-Za-z]+\s[A-Za-z]+,)(\-?\d{{0,3}}\.\d*?)(\s[A-Za-z]+\s[A-Za-z]+,\s)(\-?\d{{0,2}}\.\d*?)(\s[A-Za-z]+\s[A-Za-z]+,\s)(\-?\d{{0,2}}\.\d*?)$">
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
    <!-- Dataverse maps several rights and access fields to dc:rights. In order to conform to the HydraNorth model, these statements are concatenated into a single instance of the dcterms:rights field, separated by ' / '. -->
    <xsl:template name="rights">
        <xsl:if test="dc:rights">
        <xsl:element name="dcterms:rights">
            <xsl:for-each select="dc:rights">
                <xsl:value-of select="."/>
                <xsl:choose>
                    <xsl:when test="position() = last()"/>
                    <xsl:otherwise>
                        <xsl:text> / </xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:element>            
        </xsl:if>
    </xsl:template>
    <!-- All resources from Dataverse are assigned the controlled type value of Dataset -->
    <xsl:template name="type">
        <xsl:element name="dcterms:type" inherit-namespaces="no">Dataset</xsl:element>
    </xsl:template>
</xsl:stylesheet>
