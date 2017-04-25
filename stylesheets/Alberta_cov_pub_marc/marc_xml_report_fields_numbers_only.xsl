<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="docs"
        select="collection('../metadata-wrangling/internet_archive_coll/albertagovernmentpublications/enhanced_marc_merged_240_subfields?select=*marc.xml;recurse=yes')"/>

    <xsl:template match="*">
        <xsl:for-each select="$docs//*:subfield">      
            <xsl:choose>
                <xsl:when test="self::*:subfield">
                    <xsl:variable name="sub">
                        <xsl:value-of select="concat(../@tag,'$',./@code)"/>
                    </xsl:variable>
                    <xsl:value-of select="$sub"/>
                </xsl:when>
            </xsl:choose>
            
            <xsl:call-template name="context"/>
        </xsl:for-each>
    </xsl:template>


    <xsl:template name="context">


        <xsl:text>&#xa;</xsl:text>
        
        <!-- Ocurrence -->
        <!--<xsl:value-of select="count(preceding-sibling::*[last() and local-name()=$namesake])+1+count(following-sibling::*[last() and local-name()=$namesake])"/>-->        
        <!--<xsl:text>&#xa;</xsl:text>-->
    </xsl:template>


    <!-- leader 06 -type of record 169 not a-->
    <!-- leader 07 -bibliographic level -->
    <!-- 336$a / 336$b - content type //*:datafield[@tag='336'] = 9788a 9788b-->

    <!-- 007 pos 0 - physical desc category of material - all[pos 1] electronic resource 90943, 7 additional cases not ^c -->
    <!-- //*:datafield[@tag='655']/*:subfield[@code='a'] 2 overall ocurrences -->


</xsl:transform>
