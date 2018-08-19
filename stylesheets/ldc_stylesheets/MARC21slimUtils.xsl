<?xml version='1.0'?>
<xsl:stylesheet version="1.0" xmlns:marc="http://www.loc.gov/MARC21/slim" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!-- 8/19/04: ntra added "marc:" prefix to datafield element -->
	<xsl:template name="datafield">
		<xsl:param name="tag"/>
		<xsl:param name="ind1"><xsl:text> </xsl:text></xsl:param>
		<xsl:param name="ind2"><xsl:text> </xsl:text></xsl:param>
		<xsl:param name="subfields"/>
		<xsl:element name="marc:datafield">
			<xsl:attribute name="tag">
				<xsl:value-of select="$tag"/>
			</xsl:attribute>
			<xsl:attribute name="ind1">
				<xsl:value-of select="$ind1"/>
			</xsl:attribute>
			<xsl:attribute name="ind2">
				<xsl:value-of select="$ind2"/>
			</xsl:attribute>
			<xsl:copy-of select="$subfields"/>
		</xsl:element>
	</xsl:template>

	<xsl:template name="subfieldSelect">
		<xsl:param name="codes"/>
		<xsl:param name="delimeter"><xsl:text> </xsl:text></xsl:param>
		<xsl:variable name="str">
			<xsl:for-each select="marc:subfield">
				<xsl:if test="contains($codes, @code)">
					<xsl:value-of select="text()"/><xsl:value-of select="$delimeter"/>
				</xsl:if>
			</xsl:for-each>
		</xsl:variable>
		<xsl:value-of select="substring($str,1,string-length($str)-string-length($delimeter))"/>
	</xsl:template>

	<xsl:template name="buildSpaces">
		<xsl:param name="spaces"/>
		<xsl:param name="char"><xsl:text> </xsl:text></xsl:param>
		<xsl:if test="$spaces>0">
			<xsl:value-of select="$char"/>
			<xsl:call-template name="buildSpaces">
				<xsl:with-param name="spaces" select="$spaces - 1"/>
				<xsl:with-param name="char" select="$char"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>

	<xsl:template name="chopPunctuation">
		<xsl:param name="chopString"/>
		<xsl:param name="punctuation"><xsl:text>.:,;/ </xsl:text></xsl:param>
		<xsl:variable name="length" select="string-length($chopString)"/>
		<xsl:choose>
			<xsl:when test="$length=0"/>
			<xsl:when test="contains($punctuation, substring($chopString,$length,1))">
				<xsl:call-template name="chopPunctuation">
					<xsl:with-param name="chopString" select="substring($chopString,1,$length - 1)"/>
					<xsl:with-param name="punctuation" select="$punctuation"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="not($chopString)"/>
			<xsl:otherwise><xsl:value-of select="$chopString"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="chopPunctuationFront">
		<xsl:param name="chopString"/>
		<xsl:variable name="length" select="string-length($chopString)"/>
		<xsl:choose>
			<xsl:when test="$length=0"/>
			<xsl:when test="contains('.:,;/[ ', substring($chopString,1,1))">
				<xsl:call-template name="chopPunctuationFront">
					<xsl:with-param name="chopString" select="substring($chopString,2,$length - 1)"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="not($chopString)"/>
			<xsl:otherwise><xsl:value-of select="$chopString"/></xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template name="CheckPunctuationBack">
		<xsl:param name="Source" />
		<xsl:param name="find_punct" />
		<xsl:param name="insert_punct" />
		<xsl:variable name="length" select="string-length($Source)" />
		<xsl:if test="contains($find_punct, substring($Source, $length, 1))=false()">
		    <xsl:value-of select="$insert_punct" />
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="replaceText">
	   <xsl:param name="tstring" />
	   <xsl:param name="text1" />
	   <xsl:param name="text2" />
	   <xsl:choose>
	      <xsl:when test="contains($tstring, $text1)">
	         <xsl:value-of 
	          select="concat(substring-before($tstring,$text1),
	                         $text2)" />
	         <xsl:call-template name="replaceText">
	            <xsl:with-param name="tstring"
	                 select="substring-after($tstring,$text1)" />
      	      <xsl:with-param name="text1" select="$text1" />
            	<xsl:with-param name="text2" select="$text2" />
	         </xsl:call-template>
      	</xsl:when>
	      <xsl:otherwise>
      	   <xsl:value-of select="$tstring" />
	      </xsl:otherwise>
	   </xsl:choose>
	</xsl:template>
	
		<xsl:template name="Tokenize">
		<xsl:param name="string" />
		<xsl:param name="delim" />
		<xsl:param name="tag" />
		<xsl:param name="ind1" />
		<xsl:param name="ind2" />
		<xsl:param name="subfield" />

		<!-- only copy the data while the string isn't null -->
		<xsl:if test="string-length($string)!=0">
		<!-- if the string doesn't contain a comma (the last item in the list), then output it "as is" -->
			<xsl:choose>
				<xsl:when test="contains($string, $delim)=0">
					<marc:datafield>
					<xsl:attribute name="tag"><xsl:value-of select="$tag" /></xsl:attribute>
					<xsl:attribute name="ind1"><xsl:value-of select="$ind1" /></xsl:attribute>
					<xsl:attribute name="ind2"><xsl:value-of select="$ind2" /></xsl:attribute>
					<marc:subfield>
						<xsl:attribute name="code"><xsl:value-of select="$subfield" /></xsl:attribute>
							<xsl:value-of select="$string" />
						</marc:subfield>
					</marc:datafield>
				</xsl:when>
				<xsl:when test="contains($string, $delim)&gt;0">
					<!-- otherwise output the string before the comma (no comma, then the string is blank) -->	
					<marc:datafield>
						<xsl:attribute name="tag"><xsl:value-of select="$tag" /></xsl:attribute>
						<xsl:attribute name="ind1"><xsl:value-of select="$ind1" /></xsl:attribute>
						<xsl:attribute name="ind2"><xsl:value-of select="$ind2" /></xsl:attribute>
						<marc:subfield>
							<xsl:attribute name="code"><xsl:value-of select="$subfield" /></xsl:attribute>
							<xsl:value-of select="substring-before($string, $delim)" />
						</marc:subfield>
					</marc:datafield>
					<xsl:if test = "string-length(substring-after($string, $delim))!=0">
						<xsl:call-template name="Tokenize">
							<xsl:with-param name="string" select="substring-after($string, $delim)" />
							<xsl:with-param name="delim" select="$delim" />
							<xsl:with-param name="tag" select="$tag" />
							<xsl:with-param name="ind1" select="$ind1" />
							<xsl:with-param name="ind2" select="$ind2" />
							<xsl:with-param name="subfield" select="$subfield" />
						</xsl:call-template>
					</xsl:if>
				</xsl:when>
				<xsl:otherwise />
			</xsl:choose>
		</xsl:if>	


	</xsl:template>

</xsl:stylesheet><!-- Stylus Studio meta-information - (c)1998-2003 Copyright Sonic Software Corporation. All rights reserved.-->
<!--Modified 8/21/2003 by Terry Reese -->