
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:ns2="http://www.w3.org/1999/xlink"
    exclude-result-prefixes="xs" version="2.0">

    <xsl:variable name="doc1" select="document('../metadata-wrangling/BIBFRAME/da/samsteele1.xml')"/>
    <xsl:variable name="doc2"
        select="document('../metadata-wrangling/BIBFRAME/da/ead_0000024914_sir-samuel-steele-collection.xml')"/>

    <xsl:template match="/">

        <xsl:variable name="nod" as="xs:string+">
            <!--            <Item>p</Item>
            <Item>ead</Item>-->
            <Item>persname</Item>
        </xsl:variable>
        <xsl:for-each select="$nod">
            <xsl:for-each select="$doc1//node()[local-name() = $nod]">
                <xsl:variable name="text">
                    <xsl:value-of select="(text())"/>
                </xsl:variable>
                <xsl:variable name="path">
                    <xsl:value-of select="ancestor::node()/name()"/>
                </xsl:variable>
                <xsl:variable name="num">
                    <xsl:value-of
                        select="concat('[', (count(preceding-sibling::*[name() = parent::node()/name()]) + 1), ']', '/', name(), '[', (count(preceding-sibling::node()/name()) + 1), ']', '[', position(), ']')"
                    />
                </xsl:variable>
                <xsl:choose>
                    <xsl:when
                        test="$doc2//node()[local-name() = $nod]/(text()) = normalize-space($text)"> </xsl:when>
                    <xsl:otherwise>
                        <xsl:result-document href="peel/{$nod}.xml">
                            <xsl:element name="root">
                                <xsl:element name="address">
                                    <xsl:value-of select="concat($path, $num)"/>
                                </xsl:element>
                                <xsl:element name="text">
                                    <xsl:value-of select="$text"/>
                                </xsl:element>
                            </xsl:element>
                        </xsl:result-document>
                        <xsl:value-of select="concat($path, $num)"/>
                        <xsl:text>&#xa;</xsl:text>
                        <xsl:value-of select="$text"/>
                        <xsl:text>&#xa;</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
