<xsl:stylesheet xmlns:mods="http://www.loc.gov/mods/v3" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:peel="http://peel.library.ualberta.ca/mods-extensions"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fn="fn" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="3.6"
    exclude-result-prefixes="fn xsl xs">
    
    <!-- stylesheet to transform peel postcard csv/tsv template to MODS/XML -->
    <xsl:output indent="yes" encoding="UTF-8"/>
    
    <!-- location of the tsv/csv file -->
    <xsl:param name="doc"
        select="'file:///home/mparedes/local-peel.git/Calgary%20Stampede%20Postcard%20metadata%20-%20Stampede%20Postcards.tsv'"/>

    <xsl:function name="fn:rows" as="xs:string+">
        <xsl:param name="str" as="xs:string"/>
        <xsl:analyze-string select="concat($str, ',')" regex="([^\t][^\t]*)\t?|\t">
            <xsl:matching-substring>
                <xsl:sequence select="regex-group(1)"/>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:function>

    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="unparsed-text-available($doc)">
                <xsl:variable name="tsv" select="unparsed-text($doc)"/>
                <xsl:variable name="lines" select="tokenize($tsv, '&#xa;')" as="xs:string+"/>
                <xsl:variable name="cell" select="tokenize($lines[1], '&#x9;')" as="xs:string+"/>

                <root>
                    <xsl:for-each select="$lines[position() &gt; 1]">
                        <xsl:variable name="lineItems" select="fn:rows(.)" as="xs:string+"/>
                        <xsl:element name="mods:mods">
                            <xsl:namespace name="mods">http://www.loc.gov/mods/v3</xsl:namespace>
                            <xsl:attribute name="version">3.6</xsl:attribute>
                            <xsl:for-each select="$cell">
                                <xsl:variable name="pos" select="position()"/>
                                <xsl:variable name="cellValue">
                                    <xsl:value-of select="$cell[$pos]"/>
                                </xsl:variable>
                                <xsl:if test="$lineItems[$pos] != ''">
                                <xsl:choose>
                                    <xsl:when test="$cellValue = 'Title'">
                                        <xsl:element name="titleInfo" xmlns="http://www.loc.gov/mods/v3">
                                            <!-- this attribute should be maaped to the language field -->
                                            <xsl:attribute name="lang">
                                                <xsl:value-of select="lower-case($lineItems[$pos + 5])"/>
                                            </xsl:attribute>
                                            <xsl:element name="title">
                                                <xsl:value-of select="$lineItems[$pos]"/>
                                            </xsl:element>
                                        </xsl:element>
                                        <xsl:element name="typeOfResource" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:text>still image</xsl:text>
                                        </xsl:element>
                                        <xsl:element name="genre" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="authority">gmgpc</xsl:attribute>
                                            <xsl:text>Postcards</xsl:text>
                                        </xsl:element> 
                                    </xsl:when>
                                    <!-- a new field is to be created in the csv template that can be mapped to this element --> 
                                    <xsl:when test="$cellValue = 'Language'">
                                        <xsl:element name="language" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:element name="languageTerm">
                                                <xsl:attribute name="type">text</xsl:attribute>
                                                <xsl:value-of select="$lineItems[$pos]"/>
                                            </xsl:element>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Name'">
                                        <xsl:element name="name" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:choose>
                                                <xsl:when
                                                  test="contains($lineItems[$pos + 1], 'Publisher') or contains($lineItems[$pos + 1], 'publisher')">
                                                  <xsl:attribute name="type">corporate</xsl:attribute>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                  <xsl:attribute name="type">personal</xsl:attribute>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                            <xsl:element name="namePart">
                                                <xsl:value-of select="$lineItems[$pos]"/>
                                            </xsl:element>
                                            <xsl:element name="role">
                                                <xsl:element name="roleTerm">
                                                  <xsl:attribute name="type">text</xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos + 1]"/>
                                                </xsl:element>
                                            </xsl:element>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Place'">
                                        <xsl:variable name="location"
                                            select="tokenize(replace($lineItems[$pos], '^ +,', ''), '\s')"/>
                                        <xsl:element name="subject" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:element name="hierarchicalGeographic">
                                                <xsl:element name="country">
                                                  <xsl:value-of select="$location[1]"/>
                                                </xsl:element>
                                                <xsl:element name="province">
                                                  <xsl:value-of select="$location[2]"/>
                                                </xsl:element>
                                                <xsl:element name="city">
                                                  <xsl:value-of select="$location[3]"/>
                                                </xsl:element>
                                            </xsl:element>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Extent'">
                                        <xsl:element name="physicalDescription" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:element name="extent">
                                                <xsl:value-of select="$lineItems[$pos]"/>
                                            </xsl:element>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Subject'">
                                        <xsl:element name="subject" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:variable name="topic"
                                                select="tokenize($lineItems[$pos], ';')"/>
                                            <xsl:for-each select="$topic">
                                                <xsl:element name="topic">
                                                  <xsl:value-of select="."/>
                                                </xsl:element>
                                            </xsl:for-each>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Date_Issued'">
                                        <xsl:element name="originInfo" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:element name="issuance">
                                                <xsl:text>monographic</xsl:text>
                                            </xsl:element>
                                            <xsl:if
                                                test="contains($lineItems[$pos - 2], 'Publisher') or contains($lineItems[$pos - 2], 'publisher')">
                                                <xsl:element name="publisher">
                                                  <xsl:value-of select="$lineItems[$pos - 3]"/>
                                                </xsl:element>
                                            </xsl:if>
                                            <xsl:choose>
                                                <xsl:when
                                                  test="matches($lineItems[$pos], '\[[A-Z]\]')">
                                                  <xsl:element name="dateIssued">
                                                  <xsl:attribute name="qualifier">exact</xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                  <xsl:element name="dateIssued">
                                                  <xsl:attribute name="qualifier">approximate</xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'To'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="type">public_to</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Description'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="type">public_description</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'From'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                           <xsl:attribute name="type">public_from</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Address'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="type">public_address</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Message'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="type">public_message</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Postmark_Date'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="type"
                                                >public_postmark_date</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'On_Back'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="type">public_on_back</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'On_Front'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="type">public_on_front</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'General_Note'">
                                        <xsl:element name="note" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:attribute name="type">public_other</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Identifier'">
                                        <xsl:element name="identifier" >
                                            <xsl:attribute name="type">local</xsl:attribute>
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Publication_Statement'">
                                        <!-- deleting Publication_Statement -->
                                        <!-- add an element for this field once a proper mapping to MODS is specified --> 
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'General_Note'">
                                        <!-- deleting Note -->
                                    </xsl:when>
                                    <xsl:when test="$cellValue = 'Role'">
                                        <!-- deleting Role -->
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:element name="{.}" xmlns="http://www.loc.gov/mods/v3">
                                            <xsl:value-of select="$lineItems[$pos]"/>
                                        </xsl:element>
                                    </xsl:otherwise>
                                </xsl:choose>
                                </xsl:if>
                            </xsl:for-each>
                            <xsl:element name="location" xmlns="http://www.loc.gov/mods/v3">
                                <xsl:element name="url">
                                    <xsl:attribute name="access">object in context</xsl:attribute>
                                    <xsl:attribute name="usage">primary display</xsl:attribute>
                                    <xsl:text>http://peel.library.ualberta.ca/postcards/</xsl:text>
                                    <xsl:value-of select="$lineItems[1]"/>
                                    <xsl:text>.html</xsl:text>
                                </xsl:element>
                                <xsl:element name="url">
                                    <xsl:attribute name="access">raw object</xsl:attribute>
                                    <xsl:attribute name="note"/>
                                    <xsl:text>http://peel.library.ualberta.ca/pcimages/</xsl:text>
                                    <xsl:value-of select="substring($lineItems[1], 1, 2)"/>
                                    <xsl:text>/</xsl:text>
                                    <xsl:value-of select="substring($lineItems[1], 3, 3)"/>
                                    <xsl:text>/web/</xsl:text>
                                    <xsl:value-of select="$lineItems[1]"/>
                                    <xsl:text>.jpg</xsl:text>
                                </xsl:element>
                                <xsl:element name="url">
                                    <xsl:attribute name="access">preview</xsl:attribute>
                                    <xsl:attribute name="note"/>
                                    <xsl:text>http://peel.library.ualberta.ca/pcimages/</xsl:text>
                                    <xsl:value-of select="substring($lineItems[1], 1, 2)"/>
                                    <xsl:text>/</xsl:text>
                                    <xsl:value-of select="substring($lineItems[1], 3, 3)"/>
                                    <xsl:text>/thumbs/</xsl:text>
                                    <xsl:value-of select="$lineItems[1]"/>
                                    <xsl:text>.jpg</xsl:text>
                                </xsl:element>
                            </xsl:element>
                        </xsl:element>
                    </xsl:for-each>
                </root>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>Cannot locate : </xsl:text>
                <xsl:value-of select="$doc"/>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>
    
</xsl:stylesheet>
