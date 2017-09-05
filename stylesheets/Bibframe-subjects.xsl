<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
    xmlns:bflc="http://id.loc.gov/ontologies/bflc/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    exclude-result-prefixes="xs xsl rdf rdfs bf bflc madsrdf" version="2.0">
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:variable name="doc" select="collection('../../metadata-wrangling/BIBFRAME/UADATA-BIBFRAME-Segmented?select=*.xml;recurse=yes')"/>
    
    <xsl:template match="/">
        <xsl:for-each select="//bf:subject/bf:Topic[@rdf:about]">
            <xsl:value-of select="normalize-space(rdfs:label)"/>
            <xsl:text>&#09;</xsl:text>
<!--            <xsl:for-each select="bf:source/bf:Source/bf:code">
           <xsl:value-of select="normalize-space(.)"/>
            <xsl:text>&#09;</xsl:text>
            </xsl:for-each>-->
            <xsl:value-of select="@rdf:about"/>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
    
</xsl:stylesheet>
