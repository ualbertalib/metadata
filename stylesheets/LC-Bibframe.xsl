<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
    xmlns:bflc="http://id.loc.gov/ontologies/bflc/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    exclude-result-prefixes="xs xsl rdf rdfs bf bflc madsrdf" version="2.0">

    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:for-each select="root/rdf:RDF/bf:Work">
            <xsl:value-of select="normalize-space(bf:title/bf:Title/rdfs:label)"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="normalize-space(bf:title/bf:Title/bflc:titleSortKey)"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="normalize-space(bf:title/bf:Title/bf:mainTitle)"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="@rdf:about"/>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
