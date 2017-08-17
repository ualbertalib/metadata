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
        <xsl:for-each select="root/rdf:RDF/bf:Work/bf:contribution/bf:Contribution/bf:agent/bf:Agent">
            <xsl:value-of select="normalize-space(rdfs:label)"/>
            <xsl:variable name="name-part">
                <xsl:value-of select="normalize-space(replace(rdfs:label, ' ', '%20'))"/>
            </xsl:variable>
            <xsl:text>&#09;</xsl:text>
            <xsl:for-each select="rdf:type">
                <xsl:value-of select="normalize-space(replace(@rdf:resource, 'http://id.loc.gov/ontologies/bibframe/', ''))"/>
                <xsl:variable name="p">
                    <xsl:value-of select="normalize-space(replace(@rdf:resource, 'http://id.loc.gov/ontologies/bibframe/', ''))"/>
                </xsl:variable>
                <xsl:text>&#09;</xsl:text>
                <xsl:choose>
                    <xsl:when test="$p = 'Person'">
                        <xsl:text>http://www.viaf.org/viaf/search?query=local.personalNames%20all%20%22</xsl:text><xsl:value-of select="$name-part"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>http://www.viaf.org/viaf/search?query=local.corporateNames%20all%20%22</xsl:text><xsl:value-of select="$name-part"/>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="@rdf:about"/>
            </xsl:for-each>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
