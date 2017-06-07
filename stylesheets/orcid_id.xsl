<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:common="http://www.orcid.org/ns/common"
    exclude-result-prefixes="xs xsl common" version="2.0">
    
    <xsl:output method="text"/>

    <xsl:template match="/">      
            <xsl:for-each select="//common:path">
                <xsl:value-of select="."/>
                <xsl:text>&#xa;</xsl:text>
            </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
