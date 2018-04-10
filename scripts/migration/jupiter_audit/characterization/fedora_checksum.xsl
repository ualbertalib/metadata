<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xpath-default-namespace="http://hul.harvard.edu/ois/xml/ns/fits/fits_output"
    xsi:schemaLocation="http://hul.harvard.edu/ois/xml/ns/fits/fits_output http://hul.harvard.edu/ois/xml/xsd/fits/fits_output.xsd"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:variable name="docs" select="collection('xmls?select=*.xml;recurse=yes')"/>
    
    <xsl:template match="/">
        <xsl:for-each select="$docs">
        <xsl:value-of select="//md5checksum"/>
            <xsl:text>------</xsl:text>
        <xsl:value-of select="replace(base-uri(), 'file:/home/ddavoodi/git/remote/metadata/scripts/migration/jupiter_audit/Char/xmls/', '')"/>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
        
    </xsl:template>
    
</xsl:stylesheet>