<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
    xmlns:bflc="http://id.loc.gov/ontologies/bflc/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    xmlns:fn="fn" exclude-result-prefixes="xs xsl rdf rdfs bf bflc madsrdf" version="2.0">

    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:param name="doc" select="'file:///home/mparedes/metadata_work/MARC/viaf-id1.tsv'"/>

    <xsl:param name="rdf"
        select="'file:///home/mparedes/metadata_work/MARC/1985Imprint-BIBFRAME-2/merged-file.xml'"/>

    <xsl:function name="fn:rows" as="xs:string+">
        <xsl:param name="str" as="xs:string"/>
        <xsl:analyze-string select="concat($str, ',')" regex="([^\t][^\t]*)\t?|\t">
            <xsl:matching-substring>
                <xsl:sequence select="regex-group(1)"/>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:function>

    <xsl:template match="@* | node()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>



    <xsl:template match="//rdf:RDF/bf:Work/bf:contribution/bf:Contribution/bf:agent/bf:Agent">

        <xsl:variable name="name-part">
            <xsl:value-of select="normalize-space(rdfs:label)"/>
        </xsl:variable>
        <xsl:variable name="temp" select="."/>
        <xsl:variable name="temp_name" select="tokenize($name-part, ',')"/>
        <xsl:variable name="fname" select="replace($temp_name[2], '\.', '')"/>
        <xsl:variable name="lname" select="replace($temp_name[1], '\.', '')"/>
        <xsl:variable name="p">
            <xsl:value-of
                select="normalize-space(replace(rdf:type/@rdf:resource, 'http://id.loc.gov/ontologies/bibframe/', ''))"
            />
        </xsl:variable>
        <xsl:element name="bf:Agent">
            <xsl:choose>
                <xsl:when test="unparsed-text-available($doc)">
                    <xsl:variable name="tsv" select="unparsed-text($doc)"/>
                    <xsl:variable name="lines" select="tokenize($tsv, '&#xa;')" as="xs:string+"/>
                    <xsl:for-each select="$lines[position() &gt; 1]">
                        <xsl:variable name="lineItems" select="fn:rows(.)" as="xs:string+"/>
                        <xsl:if test="$lineItems[4] != ''">
                            <xsl:variable name="viaf"
                                select="concat('http://viaf.org/viaf/', $lineItems[4])"/>
                            <xsl:if test="$lineItems[3] = $lname and $lineItems[2] = $fname">
                                <xsl:attribute name="rdf:about" select="$viaf"/>
                            </xsl:if>
                        </xsl:if>
                    </xsl:for-each>
                </xsl:when>
            </xsl:choose>
            <xsl:for-each select="*">
                <xsl:copy>
                    <xsl:apply-templates select="@* | node()"/>
                </xsl:copy>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>



</xsl:stylesheet>
