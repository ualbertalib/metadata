<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:text>Field/subfield&#09;Indicators&#09;Content&#09;Full marc&#09;Resource URL&#09;Bib level&#09;Content type&#09;Occurrence&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="docs"
        select="collection('../metadata-wrangling/internet_archive_coll?select=*archive_marc.xml;recurse=yes')"/>


    <xsl:template match="*">
        <xsl:for-each select="$docs//*:leader | $docs//*:controlfield | $docs//*:subfield">
            <xsl:choose>
                <xsl:when test="self::*:leader">
                    <xsl:text>leader</xsl:text>                
                </xsl:when>
                <xsl:when test="self::*:controlfield">
                    <xsl:value-of select="@tag"/>                
                </xsl:when>
                <xsl:when test="self::*:subfield">
                    <xsl:value-of select="concat(../@tag,'$',./@code)"/>                    
                </xsl:when>
            </xsl:choose>
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="replace(concat(../@ind1,../@ind2),'\s','-')"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:value-of select="./text()[normalize-space()]"/>
            <xsl:text>&#09;</xsl:text>
            <xsl:call-template name="context"/>
        </xsl:for-each>
    </xsl:template>
    
    
    <xsl:template name="context">
        
        <xsl:variable name="id">
            <xsl:value-of select="ancestor-or-self::*:record/*:controlfield[@tag='001']"/>
        </xsl:variable>
        <xsl:variable name="typerec">
            <xsl:value-of select="substring(ancestor-or-self::*:record/*:leader,6,1)"/>
        </xsl:variable>
        <xsl:variable name="biblevel">
            <xsl:value-of select="substring(ancestor-or-self::*:record/*:leader,7,1)"/>
        </xsl:variable>
        <!--<xsl:variable name="namesake">
            <xsl:if test="ancestor-or-self::*:controlfield">
                <xsl:value-of select="ancestor-or-self::*:controlfield/@tag"/>
            </xsl:if>
            <xsl:if test="ancestor-or-self::*:datafield">
                <xsl:value-of select="concat(ancestor-or-self::*:datafield/@tag,'$',ancestor-or-self::*:subfield/@code)"/>
            </xsl:if>
        </xsl:variable>-->
        
        <!-- Link to full marc record -->
        <xsl:value-of select="concat('https://archive.org/download/',$id,'/',$id,'_marc.xml')"/>
        <xsl:text>&#09;</xsl:text>
        
        <!-- Link to IA landing page -->
        <xsl:value-of select="ancestor-or-self::*:record/*:datafield[@tag='856' and @ind2='1']/*:subfield[@code='u']"/>
        <xsl:text>&#09;</xsl:text>
        
        <!-- Link to Open Library -->
        <!--<xsl:value-of select="ancestor-or-self::*:record/*:datafield[@tag='856' and @ind2='2']/*:subfield[@code='u']"/>-->
        
        <!-- Type of record -->
        <xsl:value-of select="$typerec"/>
        <xsl:text>&#09;</xsl:text>
        
        <!-- Bibliographic level -->
        <xsl:value-of select="$biblevel"/>
        <xsl:text>&#09;</xsl:text>
        
        <!-- Content type -->
        <xsl:value-of select="//*:datafield[@tag='336']/*:subfield[@code='a']"/>
        <xsl:text>&#09;</xsl:text>
        
        <!-- Ocurrence -->
        <!--<xsl:value-of select="count(preceding-sibling::*[last() and local-name()=$namesake])+1+count(following-sibling::*[last() and local-name()=$namesake])"/>-->        
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>
    
    
    <!-- leader 06 -type of record 169 not a-->
    <!-- leader 07 -bibliographic level -->
    <!-- 336$a / 336$b - content type //*:datafield[@tag='336'] = 9788a 9788b-->
    
    <!-- 007 pos 0 - physical desc category of material - all[pos 1] electronic resource 90943, 7 additional cases not ^c -->
    <!-- //*:datafield[@tag='655']/*:subfield[@code='a'] 2 overall ocurrences -->
    
    
</xsl:transform>
