<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:variable name="doc" select="collection('/home/mparedes/metadata_work/ERA_files/post-migration/20171106/2017-11-06_Transfered/?select=u*.xml;recurse=yes')"/>
    
    <xsl:template match="/">
        
        <xsl:for-each select="$doc//*:datastream[contains(@ID,'DS')]">
            
            <xsl:value-of select="*:datastreamVersion/@LABEL"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="replace(base-uri(), 'file:/home/mparedes/metadata_work/ERA_files/post-migration/20171106/2017-11-06_Transfered/', '')"/>
            <xsl:text>&#xa;</xsl:text>
            
        </xsl:for-each>
        
    </xsl:template>
    
</xsl:stylesheet>