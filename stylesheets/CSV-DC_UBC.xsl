<xsl:stylesheet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fn="fn" xmlns:xs="http://www.w3.org/2001/XMLSchema" version="2.0"
    exclude-result-prefixes="fn xsl xs">

    <!-- stylesheet to transform UBC-Theses TSV to DC.xml -->
    <xsl:output indent="yes" encoding="UTF-8"/>

    <!-- location of the tsv/csv file -->
    <xsl:param name="doc"
        select="'file:///home/mparedes/UBC_thises/LinkedDataThesesWithURIsJuly13.tsv'"/>

    <xsl:function name="fn:rows" as="xs:string+">
        <xsl:param name="str" as="xs:string"/>
        <xsl:analyze-string select="concat($str, ',')" regex="([^\t][^\t]*)\t?|\t">
            <xsl:matching-substring>
                <xsl:sequence select="regex-group(1)"/>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:function>

    <xsl:template match="/">
        <xsl:param name="index" select="4"/>
        <xsl:choose>
            <xsl:when test="unparsed-text-available($doc)">
                <xsl:variable name="tsv" select="unparsed-text($doc)"/>
                <xsl:variable name="tsv1" select="replace($tsv, '_x000D_', '')"/>
                <xsl:variable name="lines" select="tokenize($tsv1, '&#xa;')" as="xs:string+"/>
                <xsl:variable name="cell"
                    select="tokenize(translate($lines[1], '?)''(,/=:;', ''), '&#x9;')"
                    as="xs:string+"/>
                <xsl:element name="dc_root">
                    <xsl:for-each select="$lines[position() &gt; 1]">
                        <xsl:element name="dublin_core">
                            <xsl:attribute name="schema">dc</xsl:attribute>
                            <xsl:variable name="lineItems" select="fn:rows(.)" as="xs:string+"/>
                            <xsl:for-each select="$cell">
                                <xsl:variable name="pos" select="position()"/>
                                <xsl:variable name="cellValue">
                                    <xsl:value-of select="$cell[$pos]"/>
                                </xsl:variable>
                                <xsl:variable name="cellname" select="tokenize($cellValue, '\.')"/>
                                <xsl:variable name="lang">
                                    <xsl:value-of
                                        select="substring-before(substring-after($cellname[last()], '['), ']')"
                                    />
                                </xsl:variable>
                                <xsl:if test="$pos &gt; 2">
                                    <xsl:if test="$lineItems[$pos] != ''">
                                        <xsl:element name="dcvalue">
                                            <xsl:attribute name="element"
                                                select="replace($cellname[2], '\[*en\]', '')"/>
                                            <xsl:choose>
                                                <xsl:when test="$cellname[3] != ''">
                                                  <xsl:attribute name="qualifier"
                                                  select="replace($cellname[3], '\[\w*\]', '')"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                  <xsl:attribute name="qualifier"
                                                  >none</xsl:attribute>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                            <xsl:if test="$lang != ''">
                                                <xsl:attribute name="lang" select="$lang"/>
                                            </xsl:if>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:if>
                                </xsl:if>
                            </xsl:for-each>
                        </xsl:element>
                    </xsl:for-each>
                </xsl:element>
            </xsl:when>
        </xsl:choose>

    </xsl:template>

</xsl:stylesheet>
