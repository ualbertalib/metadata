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
      
<!-- There are no dc:creator elements in OLAC metadata. for-each template removed -->

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

<!-- For 690: Local Subject Access Fields. But OLAC lacks dc:subject. subj_template removed -->

<!-- dc:coverage Not used in OLAC metadata -->

<!-- dc:type values used in OLAC: Image, MovingImage, Sound, Text -->

      <xsl:for-each select="dc:type[@xsi:type='dcterms:DCMIType']">
        <marc:datafield tag="655" ind1="7" ind2=" ">
          <marc:subfield code="a">
            <xsl:value-of select="."/>
          </marc:subfield>
          <marc:subfield code="2">DCMI Type</marc:subfield>
        </marc:datafield>
      </xsl:for-each>

<!-- All creators are captured in dc:contributor elements. Most names are in reversed order -->

      <xsl:for-each select="dc:contributor">
        <marc:datafield tag="700" ind1="1" ind2="0">
          <marc:subfield code="a">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>

<!-- dc:source Not used in OLAC metadata -->
<!--
      <xsl:for-each select="dc:source">
        <marc:datafield tag="786" ind1="0" ind2=" ">
          <marc:subfield code="n">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>
-->
<!-- dc:relation not used in OLAC metadata -->
<!--
      <xsl:for-each select="dc:relation">
        <marc:datafield tag="787" ind1="0" ind2=" ">
          <marc:subfield code="n">
            <xsl:value-of select="."/>
          </marc:subfield>
        </marc:datafield>
      </xsl:for-each>
-->
    </marc:record>

  </xsl:template>
  
</xsl:stylesheet>