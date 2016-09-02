<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:marcrel="http://id.loc.gov/vocabulary/relators"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    version="3.0">
    
    <xsl:output method="text" encoding="UTF-8" indent="no"/>
    <xsl:strip-space elements="yes"/>
    
    <xsl:template match="*">        
        <xsl:for-each select="collection('/home/mparedes/main-metadata.git/metadata-wrangling/alberta_government_publications/marc_xml_ia/?select=*;recurse=yes')/*">
            <xsl:value-of select="normalize-space(//*:controlfield[@tag='001'])"/>        
            <xsl:text>&#09;</xsl:text>
            <xsl:call-template name="catkey"/>        
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="normalize-space(//*:datafield[@tag='245'])"/>        
            <xsl:text>&#09;</xsl:text>
            <xsl:call-template name="subjects"/>        
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
    
    
    <xsl:template name="subjects">
        <xsl:for-each select="//*:datafield[@tag[matches(.,'6\d\d')]]">
            <xsl:for-each select="*:subfield">
                <xsl:value-of select="concat('--',normalize-space())"/>
            </xsl:for-each>
            <xsl:text>;</xsl:text>
        </xsl:for-each>
    </xsl:template>
 
    
    <xsl:template name="catkey">
        <xsl:variable name="filename" select="concat('/home/mparedes/main-metadata.git/metadata-wrangling/alberta_government_publications/marc_xml_ual/',//*:controlfield[@tag='001'][1],'_marc.xml')"/>
        <xsl:value-of select="normalize-space(document($filename)//*:controlfield[@tag='001'])"/>
    </xsl:template>
    
    
</xsl:stylesheet>
