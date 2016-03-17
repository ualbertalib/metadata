<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:mods="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="xs xd"
    version="2.0">
    
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>


    <xsl:template match="//mods:recordContentSource"/>
    <xsl:template match="//mods:location//mods:physicalLocation"/>
    <xsl:template match="//mods:note[@type[matches(.,'price|imgprobs|notable')]]"/>
    <xsl:template match="//mods:subject[not(child::*[not(self::mods:geographic)])]"/>
    <xsl:template match="//mods:subject//mods:geographic"/>
    
    
</xsl:stylesheet>