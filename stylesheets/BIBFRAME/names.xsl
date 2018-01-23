<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
    xmlns:bflc="http://id.loc.gov/ontologies/bflc/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    exclude-result-prefixes="xs xsl rdf rdfs bf bflc madsrdf" version="2.0">

    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:variable name="doc"
        select="collection('../../metadata-wrangling/BIBFRAME/CompData/?select=merged-file.xml;recurse=yes')"/>

    <xsl:template match="/">
        <xsl:for-each select="$doc">
            <xsl:for-each select="root/rdf:RDF/bf:Work">
                <xsl:variable name="CN" select="bf:adminMetadata/bf:AdminMetadata/bf:identifiedBy/bf:Local/rdf:value"/>
                <xsl:for-each select="//bf:Agent[@rdf:about]">
                    <xsl:variable name="c">"</xsl:variable>
                    <xsl:variable name="name" select="replace(normalize-space(rdfs:label), $c, '')"/>
                    <xsl:value-of select="$name"/>
                    <xsl:variable name="name-part">
                        <xsl:value-of select="normalize-space(replace(rdfs:label, ' ', '%20'))"/>
                    </xsl:variable>
                    <xsl:text>&#09;</xsl:text>
                    <xsl:for-each
                        select="rdf:type[starts-with(@rdf:resource, 'http://id.loc.gov/ontologies/bibframe')]">
                        <xsl:value-of
                            select="normalize-space(replace(@rdf:resource, 'http://id.loc.gov/ontologies/bibframe/', ''))"/>
                        <xsl:variable name="p">
                            <xsl:value-of
                                select="normalize-space(replace(@rdf:resource, 'http://id.loc.gov/ontologies/bibframe/', ''))"
                            />
                        </xsl:variable>
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
                    <xsl:value-of select="bf:adminMetadata/bf:AdminMetadata/bf:identifiedBy/bf:Local/rdf:value"/>
                    <xsl:text>&#xa;</xsl:text>
                </xsl:for-each>
            </xsl:for-each>
            <!--            <xsl:value-of select="//bf:identifiedBy/bf:Local/rdf:value"/>
            <xsl:text>&#xa;</xsl:text>-->
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
