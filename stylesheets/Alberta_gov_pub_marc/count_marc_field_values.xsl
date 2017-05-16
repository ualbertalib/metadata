<?xml version="1.0"?>

<!-- Stylesheet to count the values in marc fields -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="docs"
        select="document('../../metadata-wrangling/internet_archive_coll/albertagovernmentpublications/test.xml?select=*marc.xml;recurse=yes')"/>

    <xsl:variable name="docs1"
        select="document('../../metadata-wrangling/internet_archive_coll/albertagovernmentpublications/list.xml?select=*marc.xml;recurse=yes')"/>

    <xsl:template match="*">
        <xsl:for-each select="$docs1//*:description[text()]">   
            <xsl:value-of select="."/>
            <xsl:call-template name="context"/>
        </xsl:for-each>
    </xsl:template>


    <xsl:template name="context">
        <xsl:variable name="sub">
            <xsl:value-of select="."/>
        </xsl:variable>
        <xsl:text>&#09;</xsl:text>  
        <xsl:value-of select="count($docs//*:description[text()=$sub])"/>
        <xsl:text>&#xa;</xsl:text>
        
    </xsl:template>

</xsl:transform>
