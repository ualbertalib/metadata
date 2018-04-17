<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
    xmlns:bflc="http://id.loc.gov/ontologies/bflc/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    xmlns:fn="fn" exclude-result-prefixes="fn xs xsl rdf rdfs bf bflc madsrdf" version="2.0">
    
    <!--- this style sheet ingests URIs (for name ,bf:Agent) into a single bibframe.xml file by substituting example.org (key) -->
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:param name="doc" select="'file:///home/ddavoodi/git/remote/metadata/metadata-wrangling/BIBFRAME/CompData/2015eresOrigbf_LC.tsv'"/>
    
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
    
    
    
    <xsl:template match="rdf:RDF//bf:Agent[@rdf:about]">
        <xsl:variable name="te" select="@rdf:about"/>
        <!--        <xsl:variable name="p">
            <xsl:value-of
                select="normalize-space(replace(rdf:type/@rdf:resource, 'http://id.loc.gov/ontologies/bibframe/', ''))"
            />-->
        <!--</xsl:variable>-->
        <xsl:element name="bf:Agent">
            <xsl:attribute name="rdf:about" select="@rdf:about"/>
            <xsl:choose>
                <xsl:when test="unparsed-text-available($doc)">
                    <xsl:variable name="tsv" select="unparsed-text($doc)"/>
                    <xsl:variable name="lines" select="tokenize($tsv, '&#xa;')" as="xs:string+"/>
                    <xsl:for-each select="$lines[position() &gt; 1]">
                        <xsl:variable name="lineItems" select="fn:rows(.)" as="xs:string+"/>
                        <xsl:if test="$lineItems[2] != ''">
                            <xsl:variable name="LC"
                                select="concat('http://id.loc.gov/authorities/names/', $lineItems[2])"/>
                            <xsl:if test="$lineItems[13] = $te">
                                <xsl:attribute name="rdf:about" select="$LC"/>
                            </xsl:if>
                        </xsl:if>
                        <xsl:if test="$lineItems[14] != ''">
                            <xsl:variable name="viaf"
                                select="concat('http://viaf.org/viaf/', $lineItems[14])"/>
                            <xsl:if test="$lineItems[13] = $te">
                                <bf:identifiedBy>
                                    <bf:Identifier>
                                        <rdf:value>
                                            <xsl:attribute name="rdf:about" select="replace($viaf, ',', '')"/>
                                        </rdf:value>
                                    </bf:Identifier>
                                </bf:identifiedBy>
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
