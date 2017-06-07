<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:common="http://www.orcid.org/ns/common"
    xmlns:personal-details="http://www.orcid.org/ns/personal-details"
    version="3.0">
    
    <xsl:output method="text" encoding="UTF-8" indent="no"/>
    <xsl:strip-space elements="yes"/>
    
    
    
    <xsl:template match="*">   
        <xsl:variable name="file">
            <xsl:value-of select="subsequence(reverse(tokenize(base-uri(),'/')), 2, 1)"/>
        </xsl:variable>
        <xsl:result-document href="test_orcid/{$file}.tsv">  
        <xsl:text>Search_results_order&#09;ORCID-ID&#09;Family-name&#09;Given-name&#09;NAME_frim_ERA&#xa;</xsl:text>
            <xsl:for-each select="collection('/../../home/mparedes/Documents/ORCID-search_api-test/nursing/search-results_no-spaces/IDs/?select=*.xml;recurse=yes')/*">
            <xsl:value-of select="subsequence(tokenize(subsequence(reverse(tokenize(base-uri(),'/')), 1, 1), '_'), 1, 1)"/>
            <xsl:text>&#x9;</xsl:text>
            <xsl:value-of select="(//common:path)[1]"/>        
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="//personal-details:family-name"/>         
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="//personal-details:given-names"/>               
            <xsl:text>&#x9;</xsl:text>
            <xsl:value-of select="subsequence(reverse(tokenize(base-uri(),'/')), 2, 1)"/>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
        </xsl:result-document>    
    </xsl:template>
    
    
    
</xsl:stylesheet>
