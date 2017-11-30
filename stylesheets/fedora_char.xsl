<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template match="/">
        <xsl:for-each select="//incident">
            <xsl:value-of select="description"/>
            <xsl:text>------</xsl:text>
            <xsl:value-of select="replace(systemID, '/home/mparedes/metadata/scripts/jupiter_migration/char/', '')"/>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
        
    </xsl:template>
    
    
</xsl:stylesheet>