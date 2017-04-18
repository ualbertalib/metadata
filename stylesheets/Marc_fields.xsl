<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output media-type="xml" indent="yes"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="col"
        select="collection('../metadata-wrangling/internet_archive_coll/albertagovernmentpublications/enhanced_marc_merged_240_subfields?select=*marc.xml;recurse=yes')"/>

    <xsl:template match="*">
        <xsl:element name="root">
            <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
        <xsl:for-each select="$col//*:datafield[@tag=336]/*:subfield[@code='a']">
            <xsl:element name="value">
                <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
                <xsl:value-of select="."/>
            </xsl:element>
        </xsl:for-each>
        </xsl:element>
    </xsl:template>




</xsl:transform>
