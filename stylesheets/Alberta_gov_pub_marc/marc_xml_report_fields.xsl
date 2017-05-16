<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:text>Title&#09;110b&#09;710b&#x9;700b&#x9;100b&#x9;111b&#x9;711b&#x9;110a&#x9;710a&#x9;700a&#x9;100a&#x9;111a&#x9;711a&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="docs"     select="collection('../../metadata-wrangling/internet_archive_coll/albertagovernmentpublications/enhanced_marc_serials_monographs/enhanced_marc_serials_monographs_4?select=*marc.xml;recurse=yes')"/>

     <xsl:template match="*">
        <xsl:for-each select="$docs//*:leader">
            <xsl:call-template name="context"/>
        </xsl:for-each>
    </xsl:template>
    
    
    <xsl:template name="context">
        <xsl:for-each select="//*:datafield[@tag='245']/*:subfield[@code='a']">
            <xsl:variable name="d">"</xsl:variable>
            <xsl:variable name="title">
                <xsl:value-of select="replace(., $d, '')"/>
            </xsl:variable>
        

        <xsl:value-of select="/$title"/>
        </xsl:for-each>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='110']/*:subfield[@code='b']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='710']/*:subfield[@code='b']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='700']/*:subfield[@code='b']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='100']/*:subfield[@code='b']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='111']/*:subfield[@code='b']"/>
        <xsl:text>&#x9;</xsl:text> 
                <xsl:value-of select="//*:datafield[@tag='711']/*:subfield[@code='b']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='110']/*:subfield[@code='a']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='710']/*:subfield[@code='a']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='700']/*:subfield[@code='a']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='100']/*:subfield[@code='a']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='111']/*:subfield[@code='a']"/>
        <xsl:text>&#x9;</xsl:text>
                <xsl:value-of select="//*:datafield[@tag='711']/*:subfield[@code='a']"/>
        <xsl:text>&#xa;</xsl:text>
        

    </xsl:template>
    

    
    
</xsl:transform>
