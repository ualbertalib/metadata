<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
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
    <xsl:variable name="year" select="dc:date"/>
    <xsl:variable name="ldcNum" select="dc:identifier[starts-with(., 'LDC')]"/>
    <marc:record>
      <marc:leader>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text>n</xsl:text>
        <xsl:text>m</xsl:text>
        <xsl:text>m</xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text>a</xsl:text>
        <xsl:text>2</xsl:text>
        <xsl:text>2</xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text>3</xsl:text>
        <xsl:text>i</xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text>4</xsl:text>
        <xsl:text>5</xsl:text>
        <xsl:text>0</xsl:text>
        <xsl:text>0</xsl:text>
      </marc:leader>
      <marc:controlfield tag="006">
          <xsl:text>m</xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text>o</xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text>u</xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text> </xsl:text>
      </marc:controlfield>
      <marc:controlfield tag="007">
          <xsl:text>c</xsl:text>
          <xsl:text>u</xsl:text>
          <xsl:text> </xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>u</xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>|</xsl:text>
          <xsl:text>|</xsl:text>
      </marc:controlfield>
      <xsl:element name="marc:controlfield">
        <xsl:attribute name="tag">008</xsl:attribute>
        <xsl:text>      </xsl:text>
        <xsl:text>s</xsl:text>
        <xsl:value-of select="$year"/>
        <xsl:text>    </xsl:text>
        <xsl:text>pau</xsl:text>
        <xsl:text>    </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text>  </xsl:text>
        <xsl:text>u</xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text>      </xsl:text>
        <xsl:text>mul</xsl:text>
        <xsl:text> </xsl:text>
        <xsl:text>d</xsl:text>
      </xsl:element>

      <xsl:for-each select="dc:identifier[contains(., 'ISBN: ')]">
        <xsl:analyze-string select="substring-after(., 'ISBN: ')" regex="(\d)[-](\d{{5}})[-](\d{{3}})[-](\d)">
          <xsl:matching-substring>
            <marc:datafield tag="020" ind1=" " ind2=" ">
              <marc:subfield code="a">
                <xsl:value-of select="regex-group(1)"/>
                <xsl:value-of select="regex-group(2)"/>
                <xsl:value-of select="regex-group(3)"/>
                <xsl:value-of select="regex-group(4)"/>
              </marc:subfield>
            </marc:datafield>
          </xsl:matching-substring>
        </xsl:analyze-string>        
      </xsl:for-each>

      <marc:datafield tag="024" ind1="8" ind2=" ">
        <marc:subfield code="a">
          <xsl:value-of select="$ldcNum" />
        </marc:subfield>
      </marc:datafield>

      <xsl:for-each select="dc:identifier[contains(., 'ISLRN: ')]">
        <marc:datafield tag="024" ind1="8" ind2=" ">
          <marc:subfield code="a">
            <xsl:value-of select="." />
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <marc:datafield tag="042" ind1=" " ind2=" ">
        <marc:subfield code="a">dc</marc:subfield>
      </marc:datafield>
      
      <xsl:for-each select="dc:title[1]">
        <marc:datafield tag="245" ind1="0" ind2="0">
          <marc:subfield code="a">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <xsl:for-each select="dc:publisher[contains(., 'Linguistic')]">
        <marc:datafield tag="264" ind1=" " ind2=" ">
          <marc:subfield code="a">
            <xsl:text>[Philadelphia, Pennsylvania]: </xsl:text>
          </marc:subfield>
          <marc:subfield code="b">
            <xsl:text>Linguistic Data Consortium, </xsl:text>
          </marc:subfield>
          <marc:subfield code="c">
            <xsl:text>[</xsl:text>
            <xsl:value-of select="$year" />
            <xsl:text>]</xsl:text>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <marc:datafield tag="336" ind1=" " ind2=" ">
        <marc:subfield code="a">
          <xsl:text>computer dataset</xsl:text>
        </marc:subfield>
        <marc:subfield code="b">
          <xsl:text>cod</xsl:text>
        </marc:subfield>
        <marc:subfield code="2">
          <xsl:text>rdacontent</xsl:text>
        </marc:subfield>
      </marc:datafield>

      <xsl:for-each select="dc:type[@xsi:type='dcterms:DCMIType']">
        <marc:datafield tag="336" ind1=" " ind2=" ">          
          <marc:subfield code="a">
            <xsl:choose>
              <xsl:when test=".='Image'">still image</xsl:when>
              <xsl:when test=".='MovingImage'">two-dimensional moving image</xsl:when>
              <xsl:when test=".='Software'">computer program</xsl:when>
              <xsl:when test=".='Sound'">spoken word</xsl:when>
              <xsl:when test=".='StillImage'">still image</xsl:when>
              <xsl:when test=".='Text'">text</xsl:when>
            </xsl:choose>            
          </marc:subfield>
          <marc:subfield code="b">
            <xsl:choose>
              <xsl:when test=".='Image'">sti</xsl:when>
              <xsl:when test=".='MovingImage'">tdi</xsl:when>
              <xsl:when test=".='Software'">cop</xsl:when>
              <xsl:when test=".='Sound'">spw</xsl:when>
              <xsl:when test=".='StillImage'">sti</xsl:when>
              <xsl:when test=".='Text'">txt</xsl:when>
            </xsl:choose>
          </marc:subfield>
          <marc:subfield code="2">
            <xsl:text>rdacontent</xsl:text>
          </marc:subfield>
        </marc:datafield>        
      </xsl:for-each>

      <marc:datafield tag="337" ind1=" " ind2=" ">
        <marc:subfield code="a">
          <xsl:text>computer</xsl:text>
        </marc:subfield>
        <marc:subfield code="b">
          <xsl:text>c</xsl:text>
        </marc:subfield>
        <marc:subfield code="2">
          <xsl:text>rdamedia</xsl:text>
        </marc:subfield>
      </marc:datafield>

      <marc:datafield tag="338" ind1=" " ind2=" ">
        <marc:subfield code="a">
          <xsl:text>unspecified</xsl:text>
        </marc:subfield>
        <marc:subfield code="b">
          <xsl:text>zu</xsl:text>
        </marc:subfield>
        <marc:subfield code="2">
          <xsl:text>rdacarrier</xsl:text>
        </marc:subfield>
      </marc:datafield>

      <marc:datafield tag="500" ind1=" " ind2=" ">
        <marc:subfield code="a">
          <xsl:value-of select="$ldcNum" />
        </marc:subfield>
      </marc:datafield>

      <xsl:for-each select="dc:identifier[contains(., 'https:')]">
        <marc:datafield tag="500" ind1=" " ind2=" ">
          <marc:subfield code="a">
            <xsl:value-of select="." />
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <marc:datafield tag="506" ind1="1" ind2=" ">
        <marc:subfield code="a">
          <xsl:text>Available to University of Alberta users only.</xsl:text>
        </marc:subfield>
      </marc:datafield>

      <xsl:for-each select="dc:description">
        <marc:datafield tag="520" ind1=" " ind2=" ">
          <marc:subfield code="a">
            <xsl:value-of select="normalize-space(.)"/>
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

      <xsl:for-each select="dc:type[@xsi:type='dcterms:DCMIType']">
        <marc:datafield tag="655" ind1="7" ind2=" ">
          <marc:subfield code="a">
            <xsl:choose>
              <xsl:when test=".='Image'">Pictures</xsl:when>
              <xsl:when test=".='MovingImage'">Video recordings</xsl:when>
              <xsl:when test=".='Software'">computer program</xsl:when>
              <xsl:when test=".='Sound'">Sound recordings</xsl:when>
              <xsl:when test=".='StillImage'">Pictures</xsl:when>
              <xsl:when test=".='Text'">Excerpts</xsl:when>
            </xsl:choose>            
          </marc:subfield>
          <marc:subfield code="2">lcgft</marc:subfield>
        </marc:datafield>
      </xsl:for-each>

      <xsl:for-each select="dc:contributor">
        <marc:datafield tag="700" ind1="1" ind2="0">
          <marc:subfield code="a">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>
      
      <marc:datafield tag="856" ind1="4" ind2="0">
        <marc:subfield code="3">
          <xsl:text>University of Alberta Access (Request Form)</xsl:text>
        </marc:subfield>
        <marc:subfield code="u">
          <xsl:text>https://docs.google.com/forms/d/e/1FAIpQLSd4VsEYOWoubQww-01W7IV2qDaAr4ctBJUhrJvfyN0GwoMuFQ/viewform</xsl:text>
        </marc:subfield>
      </marc:datafield>

      <marc:datafield tag="856" ind1="4" ind2="2">
        <marc:subfield code="3">
          <xsl:text>Dataset documentation</xsl:text>
        </marc:subfield>
        <marc:subfield code="u">
          <xsl:text>https://catalog.ldc.upenn.edu/</xsl:text>
          <xsl:value-of select="$ldcNum"/>
        </marc:subfield>
      </marc:datafield>

    </marc:record>
  </xsl:template>
</xsl:stylesheet>