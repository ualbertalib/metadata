<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl">
    
    <!-- V.01: June 2013. Bibliographic Services, University of Alberta Libraries -->
    <!-- Extracts all *seed* metadata from Archive-It feed -->
    <!-- Outputs data as delimiter-separated values text file -->
    
    <xsl:import href="SAMCC_variables.xsl"/>
    
    <xsl:output method="text" encoding="UTF-8" />
    
    <!--<xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>-->
    
    <xsl:template match="*:Workbook">
        <xsl:apply-templates select="//*:Worksheet[2]//*:Row"/>
    </xsl:template>
    
    <xsl:template name="row" match="//*:Worksheet[2]//*:Row">
        <xsl:value-of select="$newline"/>
        <xsl:apply-templates select="descendant::*:Cell"/>
    </xsl:template>
    
    <xsl:template name="data" match="descendant::*:Cell">
        <xsl:value-of select="replace(*:Data[normalize-space()],'\t|\n|&#13;',' ')"/>
        <xsl:value-of select="$tab"/>
    </xsl:template>

</xsl:stylesheet>