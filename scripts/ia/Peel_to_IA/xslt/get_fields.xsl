<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:mets="http://www.loc.gov/METS/"
    xmlns:mods="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    
    <xsl:template match="mets:mets">
        <xsl:value-of select="mets:dmdSec[@ID = 'MODSMD_PRINT']/mets:mdWrap/mets:xmlData/mods:mods//mods:title"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mets:dmdSec[@ID = 'MODSMD_PRINT']/mets:mdWrap/mets:xmlData/mods:mods//mods:languageTerm"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mets:dmdSec[@ID = 'MODSMD_PRINT']/mets:mdWrap/mets:xmlData/mods:mods//mods:dateIssued"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mets:dmdSec[@ID = 'MODSMD_PRINT']/mets:mdWrap/mets:xmlData/mods:mods//mods:detail[@type = 'volume']/mods:number"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mets:dmdSec[@ID = 'MODSMD_PRINT']/mets:mdWrap/mets:xmlData/mods:mods//mods:detail[@type = 'issue']/mods:number"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mets:dmdSec[@ID = 'MODSMD_PRINT']/mets:mdWrap/mets:xmlData/mods:mods//mods:detail[@type = 'edition']/mods:number"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mets:dmdSec[@ID = 'MODSMD_PRINT']/mets:mdWrap/mets:xmlData/mods:mods//mods:identifier"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
    
</xsl:stylesheet>