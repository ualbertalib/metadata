<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output indent="yes"></xsl:output>
    <xsl:strip-space elements="*"/>
    <xsl:variable name="ldc650" select="document('../../metadata-wrangling/ldc_metadata/ual_ldc_marc_650s_corrected_marcxml.xml')"/>
    
    <xsl:template match="marc:collection">
        <xsl:copy>
            <xsl:apply-templates select="marc:record"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="marc:record">
        <xsl:variable name="ldcNum" select="marc:datafield[@tag='024']/marc:subfield[@code='a'][starts-with(., 'LDC')]"/>
        <marc:record>
            <xsl:copy-of select="marc:leader"/>
            <xsl:copy-of select="marc:controlfield"/>
            <xsl:copy-of select="marc:datafield[number(@tag)&lt;650]"/>
            <xsl:if test="$ldc650/collection/marc:record/marc:datafield[@tag='490']/marc:subfield[@code='v']=$ldcNum">
                <xsl:copy-of select="$ldc650/collection/marc:record[marc:datafield[@tag='490']/marc:subfield[@code='v']=$ldcNum]/marc:datafield[@tag='650']"/>
            </xsl:if>
            <xsl:copy-of select="marc:datafield[number(@tag)&gt;650]"/>
        </marc:record>
    </xsl:template>
</xsl:stylesheet>