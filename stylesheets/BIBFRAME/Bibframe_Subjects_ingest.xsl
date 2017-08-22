<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
    xmlns:bflc="http://id.loc.gov/ontologies/bflc/" xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    xmlns:fn="fn" exclude-result-prefixes="xs xsl rdf rdfs bf bflc madsrdf" version="2.0">
    
    <xsl:output indent="yes" media-type="xml" omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:param name="doc" select="'file:///home/mparedes/metadata_work/MARC/1985_imprints_subjects_LCSH.tsv'"/>
    
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
    
    
    
    <xsl:template match="//rdf:RDF/bf:Work/bf:subject/bf:Topic">
        <xsl:variable name="te" select="@rdf:about"/>
        <xsl:element name="bf:Topic">
            <xsl:attribute name="rdf:about" select="@rdf:about"/>
            <xsl:choose>
                <xsl:when test="unparsed-text-available($doc)">
                    <xsl:variable name="tsv" select="unparsed-text($doc)"/>
                    <xsl:variable name="lines" select="tokenize($tsv, '&#xa;')" as="xs:string+"/>
                    <xsl:for-each select="$lines[position() &gt; 1]">
                        <xsl:variable name="lineItems" select="fn:rows(.)" as="xs:string+"/>
                        <xsl:if test="$lineItems[2] != ''">
                            <xsl:variable name="viaf"
                                select="$lineItems[2]"/>
                            <xsl:if test="$lineItems[4] = $te">
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
