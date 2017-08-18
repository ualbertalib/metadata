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
        <xsl:for-each select="root/rdf:RDF//bf:Work">
            <xsl:variable name="c">"</xsl:variable>
            <xsl:variable name="title" select="replace(normalize-space(bf:title/bf:Title/rdfs:label), $c, '' )"/>
            <xsl:value-of select="$title"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:choose>
                <xsl:when test="parent::bf:hasSeries">
                    <xsl:variable name="agent" select="normalize-space(../../bf:contribution[1]/bf:Contribution/bf:agent/bf:Agent/rdfs:label)"/>
                    <xsl:value-of select="$agent"/>
                    <xsl:text>&#09;</xsl:text>
                    <xsl:value-of select="concat($agent,' | ', $title)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:variable name="agent" select="normalize-space(bf:contribution[1]/bf:Contribution/bf:agent/bf:Agent/rdfs:label)"/>
                <xsl:value-of select="$agent"/>
                    <xsl:text>&#09;</xsl:text>
                    <xsl:value-of select="concat($agent,' | ', $title)"/>
                </xsl:otherwise>
            </xsl:choose>

            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="@rdf:about"/>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
