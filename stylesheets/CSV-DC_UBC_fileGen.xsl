<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    
    <xsl:template match="/">
        
        <xsl:for-each-group select="dc_root/dublin_core" group-by="dcvalue[@element ='identifier']">
            <xsl:for-each select="dcvalue[@element ='identifier']">
                <xsl:variable name="name" select="replace(replace(., 'http://hdl.handle.net/', ''), '/', '-')"/>
                <xsl:result-document href="UBC/{$name}.xml">  
                    <xsl:copy-of select="current-group()"/>
                </xsl:result-document>
            </xsl:for-each>
        </xsl:for-each-group>
    </xsl:template>
    
    
</xsl:stylesheet>