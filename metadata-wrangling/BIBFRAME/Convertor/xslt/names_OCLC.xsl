<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
    xmlns:bflc="http://id.loc.gov/ontologies/bflc/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    exclude-result-prefixes="xs xsl rdf rdfs bf bflc madsrdf" version="2.0">

    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="*">
        <xsl:for-each select="rdf:RDF/bf:Work[@rdf:about]">
            <xsl:value-of select="bf:title[1]/bf:Title/rdfs:label"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="@rdf:about"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:for-each select=".//bf:Agent[@rdf:about]">
                <xsl:if test="rdfs:label">
                    <xsl:variable name="name" select="rdfs:label"/>
                    <xsl:value-of select="$name"/>
                    <xsl:text>&#09;</xsl:text>
                    <xsl:for-each
                        select="rdf:type[starts-with(@rdf:resource, 'http://id.loc.gov/ontologies/bibframe')]">
                        <xsl:value-of select="@rdf:resource"/>

                        <xsl:text>&#09;</xsl:text>
                        <!--                <xsl:choose>
                    <xsl:when test="$p = 'Person'">
                        <xsl:text>http://www.viaf.org/viaf/search?query=local.personalNames%20all%20%22</xsl:text><xsl:value-of select="$name-part"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>http://www.viaf.org/viaf/search?query=local.corporateNames%20all%20%22</xsl:text><xsl:value-of select="$name-part"/>
                    </xsl:otherwise>
                </xsl:choose>
                -->
                    </xsl:for-each>
                    <xsl:text>&#09;</xsl:text>
                    <xsl:value-of select="@rdf:about"/>
                    <xsl:text>&#09;</xsl:text>
                </xsl:if>
            </xsl:for-each>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
