<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="marc:collection">
        <xsl:element name="ldcMetadata">
            <xsl:namespace name="marc">http://www.loc.gov/MARC21/slim</xsl:namespace>
            <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
            <xsl:apply-templates select="marc:record"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="marc:record">
        <xsl:copy>
            <!-- 
            <xsl:for-each select="marc:controlfield[@tag='001']">
                <xsl:copy-of select="."/>
            </xsl:for-each>
            <xsl:for-each select="marc:datafield[@tag='090']">
                <xsl:copy-of select="."/>
            </xsl:for-each>
            <xsl:for-each select="marc:datafield[@tag='245']">
                <xsl:copy-of select="."/>
            </xsl:for-each>-->
            <xsl:choose>
                <xsl:when test="marc:datafield[@tag='490']">
                    <marc:datafield tag="490" ind1="1" ind2=" ">
                        <xsl:copy-of select="marc:datafield[@tag='490']/marc:subfield[@code='v']"/>
                    </marc:datafield>
                </xsl:when>
                <xsl:otherwise>
                    <marc:datafield tag="490" ind1="1" ind2=" ">
                        <marc:subfield code="v">MISSING</marc:subfield>
                    </marc:datafield>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:for-each select="marc:datafield[@tag='650']">
                <xsl:copy-of select="."/>
            </xsl:for-each>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>