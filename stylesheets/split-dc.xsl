<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:ualterms="http://terms.library.ualberta.ca"
    exclude-result-prefixes="xs xd"
    version="2.0">
    <xd:doc scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Sep 28, 2015</xd:p>
            <xd:p><xd:b>Author:</xd:b> mparedes</xd:p>
        </xd:desc>
    </xd:doc>
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    
    <xsl:template match="theses">
        <xsl:for-each select="dc">
            <xsl:result-document method="xml" href="file:/C:/Users/mparedes/Documents/metadata-transforms/metadata-wrangling/theses_to_2009-split/{replace(ualterms:fedora3uuid,':','_')}.xml">
                <xsl:copy-of select="."/>
            </xsl:result-document>
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>