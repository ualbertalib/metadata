<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output indent="yes"></xsl:output>
    <xsl:strip-space elements="*"/>
    <xsl:variable name="LDC650" select="document('../../metadata-wrangling/ldc_metadata/ual_ldc_marc_650s_corrected_marcxml.xml')"/>
    
    <xsl:template match="marc:collection">
        <xsl:copy>
            <xsl:apply-templates select="marc:record"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="marc:record">
        <xsl:variable name="LDCnum" select="marc:datafield[@tag='500']/marc:subfield[@code='a'][starts-with(., 'LDC')]"/>
        <marc:record>
            <xsl:copy-of select="child::node()"/>
            <xsl:if test="$LDC650/collection/marc:record/marc:datafield[@tag='490']/marc:subfield[@code='v']=$LDCnum">
                <xsl:copy-of select="$LDC650/collection/marc:record[marc:datafield[@tag='490']/marc:subfield[@code='v']=$LDCnum]/marc:datafield[@tag='650']"/>
                <!-- 
                <marc:datafield tag='999'>meep morp</marc:datafield>
                -->
            </xsl:if>
        </marc:record>
    </xsl:template>
</xsl:stylesheet>