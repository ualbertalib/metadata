<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dcterms="http://purl.org/dc/terms/1.1"
	xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
	xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:marc="http://www.loc.gov/MARC21/slim"
	xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/
		http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns="http://www.loc.gov/MARC21/slim"  exclude-result-prefixes="dc dcterms oai_dc">

  <xsl:import href="MARC21slimUtils.xsl"/>
  <xsl:output method="xml" encoding="UTF-8" indent="yes"/>


  <xsl:template match="/">
    <collection xmlns:marc="http://www.loc.gov/MARC21/slim" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd" >
      <xsl:apply-templates />
    </collection>
  </xsl:template>

  <xsl:template name="OLAC">
    <xsl:for-each select = "ldcMetadata/olac:olac">
      <xsl:apply-templates  />
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="text()" />
  <xsl:template match="olac:olac">
    <marc:record>
      <xsl:element name="marc:leader">
        <xsl:variable name="type" select="dc:type"/>
        <xsl:variable name="leader06">
<!-- choose element not required: all records will be m.
          <xsl:choose>
            <xsl:when test="$type='collection'">p</xsl:when>
            <xsl:when test="$type='dataset'">m</xsl:when>
            <xsl:when test="$type='event'">r</xsl:when>
            <xsl:when test="$type='image'">k</xsl:when>
            <xsl:when test="$type='interactive resource'">m</xsl:when>
            <xsl:when test="$type='service'">m</xsl:when>
            <xsl:when test="$type='software'">m</xsl:when>
            <xsl:when test="$type='sound'">i</xsl:when>
            <xsl:when test="$type='text'">a</xsl:when>
            <xsl:otherwise>a</xsl:otherwise>
          </xsl:choose>
-->
          <xsl:text>m</xsl:text>
</xsl:variable>
        <xsl:variable name="leader07">
          <xsl:choose>
            <xsl:when test="$type='collection'">c</xsl:when>
            <xsl:otherwise>m</xsl:otherwise>
          </xsl:choose>
        </xsl:variable>
        <xsl:value-of select="concat('      ',$leader06,$leader07,'         3u     ')"/>
      </xsl:element>
      <marc:datafield tag="042" ind1=" " ind2=" ">
        <marc:subfield code="a">dc</marc:subfield>
      </marc:datafield>
      <xsl:for-each select="dc:creator">
        <xsl:choose>
          <xsl:when test="(.!='') and (position()=1)">
            <xsl:call-template name="persname_template">
              <xsl:with-param name="string" select="." />
              <xsl:with-param name="field" select="'100'" />
              <xsl:with-param name="ind1" select = "'1'" />
              <xsl:with-param name="ind2" select = "'0'" />
              <xsl:with-param name="type" select="'author'" />
            </xsl:call-template>
          </xsl:when>
          <xsl:otherwise>
            <xsl:if test=".!=''">
              <xsl:call-template name="persname_template">
                <xsl:with-param name="string" select="." />
                <xsl:with-param name="field" select="'700'" />
                <xsl:with-param name="ind1" select = "'1'" />
                <xsl:with-param name="ind2" select = "'0'" />
                <xsl:with-param name="type" select="'author'" />
              </xsl:call-template>
            </xsl:if>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>


      <xsl:for-each select="dc:title[1]">
        <marc:datafield tag="245" ind1="0" ind2="0">
          <marc:subfield code="a">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <xsl:for-each select="dc:title[position()>1]">
        <xsl:if test=".!=''">
          <marc:datafield tag="246" ind1="3" ind2="3">
            <marc:subfield code="a">
              <xsl:value-of select="."/>
            </marc:subfield>
          </marc:datafield>
        </xsl:if>
      </xsl:for-each>

      <xsl:choose>
        <xsl:when test="dc:publisher">
          <xsl:if test="translate(dc:publisher/.,'.,:;','')!=''">
            <marc:datafield tag="260" ind1=" " ind2=" ">
              <xsl:choose>
                <xsl:when test="dc:date">
                  <marc:subfield code="b">
                    <xsl:value-of select="dc:publisher[1]"/>
                    <xsl:text>, </xsl:text>
                  </marc:subfield>
                  <xsl:if test="translate(dc:date[1]/., '.,:;','')!=''">
                    <marc:subfield code="c">
                      <xsl:value-of select="dc:date[1]" />
                      <xsl:text>.</xsl:text>
                    </marc:subfield>
                  </xsl:if>
                </xsl:when>
                <xsl:otherwise>
                  <marc:subfield code="b">
                    <xsl:value-of select="dc:publisher[1]"/>
                    <xsl:text>.</xsl:text>
                  </marc:subfield>
                </xsl:otherwise>
              </xsl:choose>
            </marc:datafield>
          </xsl:if>
        </xsl:when>
        <xsl:otherwise>
          <xsl:if test="translate(dc:date[1],'.,:;','')!=''">
            <marc:datafield tag="260" ind1=" " ind2=" ">
              <marc:subfield code="c">
                <xsl:value-of select="dc:date[1]" />
                <xsl:text>.</xsl:text>                
              </marc:subfield>
            </marc:datafield>
          </xsl:if>
        </xsl:otherwise>
      </xsl:choose>

<!-- OLAC doesn't use dc:coverage -->

      <xsl:for-each select="dc:coverage">
        <xsl:choose>
          <xsl:when test="translate(., '0123456789-.?','')=''">
            <!--Likely;this is a date-->
            <marc:datafield tag="500" ind1=" " ind2=" ">
              <marc:subfield code="a">
                <xsl:value-of select="."/>
              </marc:subfield>
            </marc:datafield>
          </xsl:when>
          <xsl:otherwise>
            <!--likely a geographic subject, we will print this later-->
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>

      <xsl:for-each select="dc:identifier">
        <xsl:if test="position()!=last()">
          <marc:datafield tag="500" ind1=" " ind2=" ">
            <marc:subfield code="a">
              <xsl:value-of select="." />
            </marc:subfield>
          </marc:datafield>
        </xsl:if>
      </xsl:for-each>

      <xsl:for-each select="dc:description">
        <marc:datafield tag="520" ind1=" " ind2=" ">
          <marc:subfield code="a">
            <xsl:value-of select="normalize-space(.)"/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

<!-- I don't think any of the license information is relevant to the end user. -->

      <xsl:for-each select="dc:rights">
        <marc:datafield tag="540" ind1=" " ind2=" ">
          <marc:subfield code="a">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <!-- For 546: Language Note. Coded language information is contained in fields 008/35-37 (Language) and/or 041 (Language code) -->
      
      <xsl:for-each select="dc:language">
        <marc:datafield tag="546" ind1=" " ind2=" ">
          <marc:subfield code="a">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <!-- For 690: Local Subject Access Fields. But OLAC lacks dc:subject -->

      <xsl:for-each select="dc:subject">
        <xsl:call-template name="subj_template">
          <xsl:with-param name="field" select="'690'" />
          <xsl:with-param name="ind1" select="' '" />
          <xsl:with-param name="ind2" select="' '" />
          <xsl:with-param name="string" select="." />
          <xsl:with-param name="delimiter" select="';'" />
        </xsl:call-template>
      </xsl:for-each>

<!-- dc:coverage Not used in OLAC metadata -->

      <xsl:for-each select="dc:coverage">
        <xsl:choose>
          <xsl:when test="translate(., '0123456789-.?','')=''">
            <!--Likely; this is a date-->
          </xsl:when>
          <xsl:otherwise>
            <!--likely a geographic subject-->
            <marc:datafield tag="691" ind1=" " ind2=" ">
              <marc:subfield code="a">
                <xsl:value-of select="." />
              </marc:subfield>
            </marc:datafield>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>

<!-- dc:type values used in OLAC: Image, MovingImage, Sound, Text -->

      <xsl:for-each select="dc:type">
        <marc:datafield tag="655" ind1="7" ind2=" ">
          <marc:subfield code="a">
            <xsl:value-of select="."/>
          </marc:subfield>
          <marc:subfield code="2">local</marc:subfield>
        </marc:datafield>
      </xsl:for-each>

<!-- All creators are captured in dc:contributor elements. Most names are in reversed order -->

      <xsl:for-each select="dc:contributor">
        <xsl:call-template name="persname_template">
          <xsl:with-param name="string" select="." />
          <xsl:with-param name="field" select="'100'" />
          <xsl:with-param name="ind1" select = "'1'" />
          <xsl:with-param name="ind2" select = "'0'" />
          <xsl:with-param name="type" select="'contributor'" />
        </xsl:call-template>
      </xsl:for-each>

      <!-- dc:source Not used in OLAC metadata -->
      
      <xsl:for-each select="dc:source">
        <marc:datafield tag="786" ind1="0" ind2=" ">
          <marc:subfield code="n">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <!-- dc:source Not used in OLAC metadata -->
      
      <xsl:for-each select="dc:relation">
        <marc:datafield tag="787" ind1="0" ind2=" ">
          <marc:subfield code="n">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

<!-- We don't want this behaviour.
      <xsl:if test="dc:identifier">
        <marc:datafield tag="856" ind1="4" ind2="1">
          <marc:subfield code="u">
            <xsl:value-of select="dc:identifier[last()]" />
          </subfield>
          <marc:subfield code="z">Connect to this object online.</subfield>
        </datafield>
      </xsl:if>
    </record>
-->
    </marc:record>

  </xsl:template>

  <!--Subject template-->
  <!-- There are no subjects in the OLAC metadata -->

  <xsl:template name="subj_template">
    <xsl:param name="field" />
    <xsl:param name="ind1" />
    <xsl:param name="ind2" />
    <xsl:param name="string" />
    <xsl:param name="delimiter" />


    <xsl:choose>
      <!-- IF A PAREN, STOP AT AN OPENING semicolon -->
      <xsl:when test="contains($string, $delimiter)!=0">
        <xsl:variable name="newstem" select="substring-after($string, $delimiter)" />
        <marc:datafield>
          <xsl:attribute name="tag">
            <xsl:value-of select="$field" />
          </xsl:attribute>

          <xsl:attribute name="ind1">
            <xsl:value-of select="$ind1" />
          </xsl:attribute>

          <xsl:attribute name="ind2">
            <xsl:value-of select="$ind2" />
          </xsl:attribute>
          <marc:subfield code="a">
            <xsl:value-of select="substring-before($string, $delimiter)" />
          </marc:subfield>
        </marc:datafield>
        <!--Need to do recursion-->
        <xsl:call-template name="subj_template">
          <xsl:with-param name="field" select="'690'" />
          <xsl:with-param name="ind1" select="' '" />
          <xsl:with-param name="ind2" select="' '" />
          <xsl:with-param name="string" select="$newstem" />
          <xsl:with-param name="delimiter" select="';'" />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <marc:datafield>
          <xsl:attribute name="tag">
            <xsl:value-of select="$field" />
          </xsl:attribute>

          <xsl:attribute name="ind1">
            <xsl:value-of select="$ind1" />
          </xsl:attribute>

          <xsl:attribute name="ind2">
            <xsl:value-of select="$ind2" />
          </xsl:attribute>
          <marc:subfield code="a">
            <xsl:value-of select="$string" />
          </marc:subfield>
        </marc:datafield>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="persname_template">
    <xsl:param name="string" />
    <xsl:param name="field" />
    <xsl:param name="ind1" />
    <xsl:param name="ind2" />
    <xsl:param name="type" />
    <marc:datafield>
      <xsl:attribute name="tag">
        <xsl:value-of select="$field" />
      </xsl:attribute>
      <xsl:attribute name="ind1">
        <xsl:value-of select="$ind1" />
      </xsl:attribute>
      <xsl:attribute name="ind2">
        <xsl:value-of select="$ind2" />
      </xsl:attribute>

      <!-- Sample input: Brightman, Samuel C. (Samuel Charles), 1911-1992 -->
      <!-- Sample output: $aBrightman, Samuel C. $q(Samuel Charles), $d1911-. -->
      <!-- will handle names with dashes e.g. Bourke-White, Margaret -->

      <!-- CAPTURE PRIMARY NAME BY LOOKING FOR A PAREN OR A DASH OR NEITHER -->
      <xsl:choose>
        <!-- IF A PAREN, STOP AT AN OPENING PAREN -->
        <xsl:when test="contains($string, '(')!=0">
          <marc:subfield code="a">
            <xsl:value-of select="substring-before($string, '(')" />
          </marc:subfield>
        </xsl:when>
        <!-- IF A DASH, CHECK IF IT'S A DATE OR PART OF THE NAME -->
        <xsl:when test="contains($string, '-')!=0">
          <xsl:variable name="name_1" select="substring-before($string, '-')" />
          <xsl:choose>
            <!-- IF IT'S A DATE REMOVE IT -->
            <xsl:when test="translate(substring($name_1, (string-length($name_1)), 1), '0123456789', '9999999999') = '9'">
              <xsl:variable name="name" select="substring($name_1, 1, (string-length($name_1)-6))" />
              <marc:subfield code="a">
                <xsl:value-of select="$name" />
              </marc:subfield>
            </xsl:when>
            <!-- IF IT'S NOT A DATE, CHECK WHETHER THERE IS A DATE LATER -->
            <xsl:otherwise>
              <xsl:variable name="remainder" select="substring-after($string, '-')" />
              <xsl:choose>
                <!-- IF THERE'S A DASH, ASSUME IT'S A DATE AND REMOVE IT -->
                <xsl:when test="contains($remainder, '-')!=0">
                  <xsl:variable name="tmp" select="substring-before($remainder, '-')" />
                  <xsl:variable name="name_2" select="substring($tmp, 1, (string-length($tmp)-6))" />
                  <marc:subfield code="a">
                    <xsl:value-of select="$name_1" />-<xsl:value-of select="$name_2" />
                  </marc:subfield>
                </xsl:when>
                <!-- IF THERE'S NO DASH IN THE REMAINDER, OUTPUT IT -->
                <xsl:otherwise>
                  <marc:subfield code="a">
                    <xsl:value-of select="$string" />
                  </marc:subfield>
                </xsl:otherwise>
              </xsl:choose>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:when>
        <!-- NO DASHES, NO PARENS, JUST OUTPUT THE NAME -->
        <xsl:otherwise>
          <marc:subfield code="a">
            <xsl:value-of select="$string" />
          </marc:subfield>
        </xsl:otherwise>
      </xsl:choose>

      <!-- CAPTURE SECONDARY NAME IN PARENS FOR SUBFIELD Q -->
      <xsl:if test="contains($string, '(')!=0">
        <xsl:variable name="subq_tmp" select="substring-after($string, '(')" />
        <xsl:variable name="subq" select="substring-before($subq_tmp, ')')" />
        <marc:subfield code="q">
          (<xsl:value-of select="$subq" />)
        </marc:subfield>
      </xsl:if>

      <!-- CAPTURE DATE FOR SUBFIELD D, ASSUME DATE IS LAST ITEM IN FIELD -->
      <!-- Note: does not work if name has a dash in it -->
      <xsl:if test="contains($string, '-')!=0">
        <xsl:variable name="date_tmp" select="substring-before($string, '-')" />
        <xsl:variable name="remainder" select="substring-after($string, '-')" />
        <xsl:choose>
          <!-- CHECK SECOND HALF FOR ANOTHER DASH; IF PRESENT, ASSUME THAT IS DATE -->
          <xsl:when test="contains($remainder, '-')!=0">
            <xsl:variable name="tmp" select="substring-before($remainder, '-')" />
            <xsl:variable name="date_1" select="substring($remainder, (string-length($tmp)-3))" />
            <!-- CHECK WHETHER IT HAS A NUMBER BEFORE IT AND IF SO, OUTPUT IT AS DATE -->
            <xsl:if test="translate(substring($date_1, 1, 1), '0123456789', '9999999999') = '9'">
              <marc:subfield code="d">
                <xsl:value-of select="$date_1" />
                <xsl:text>.</xsl:text>                
              </marc:subfield>
            </xsl:if>
          </xsl:when>
          <!-- OTHERWISE THIS IS THE ONLY DASH SO TAKE IT -->
          <xsl:otherwise>
            <xsl:variable name="date_2" select="substring($string, (string-length($date_tmp)-3))" />
            <!-- CHECK WHETHER IT HAS A NUMBER BEFORE IT AND IF SO, OUTPUT IT AS DATE -->
            <xsl:if test="translate(substring($date_2, 1, 1), '0123456789', '9999999999') = '9'">
              <marc:subfield code="d">
                <xsl:value-of select="$date_2" />
                <xsl:text>.</xsl:text>
              </marc:subfield>
            </xsl:if>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
      <marc:subfield code="e">
        <xsl:value-of select="$type" />
      </marc:subfield>
    </marc:datafield>
  </xsl:template>

</xsl:stylesheet>