<?xml version="1.0"?>

<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    
    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="/">
        <xsl:text>Filename&#09;Title&#09;name&#09;Type of resource&#09;Language&#09;Physical description&#09;Subject&#09;Identifier&#09;Origin Info&#09;Notes&#09;Date Created&#09;Date modified&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:variable name="docs" select="collection('peel_to_TSV?select=*.xml;recurse=yes')"/>
    
    <xsl:template match="*">
        <xsl:for-each select="$docs/mods:mods">
            <xsl:call-template name="context"/>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="context">
        
        <xsl:variable name="title">
            <xsl:value-of select="mods:titleInfo/mods:title"/>
        </xsl:variable>
        <xsl:variable name="subTitle">
            <xsl:value-of select="mods:titleInfo/mods:subTitle"/>
        </xsl:variable>
        <xsl:variable name="subTitle">
            <xsl:value-of select="mods:titleInfo/mods:subTitle"/>
        </xsl:variable>

        <xsl:value-of select="mods:recordInfo/mods:recordIdentifier"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="$title"/>
        <xsl:text> |||| </xsl:text>
        <xsl:value-of select="$subTitle"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="mods:name">
            <xsl:text>name:: </xsl:text>
            <xsl:value-of select="mods:namePart"/>
            <xsl:text> --- role::</xsl:text>
            <xsl:value-of select="mods:role/mods:roleTerm"/>
            <xsl:text> --- description:: </xsl:text>
            <xsl:value-of select="mods:description"/>
            <xsl:text> ||| </xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mods:typeOfResource"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="mods:language">
            <xsl:value-of select="mods:languageTerm"/>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="mods:physicalDescription">
            <xsl:text>extent:: </xsl:text>
            <xsl:value-of select="mods:extent"/>
            <xsl:text> --- </xsl:text>
            <xsl:text>form:: </xsl:text>
            <xsl:value-of select="mods:form"/>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="mods:subject">
            <xsl:text>authority:: </xsl:text>
            <xsl:value-of select="@authority"/>
            <xsl:text> --- </xsl:text>
            <xsl:text>lang:: </xsl:text>
            <xsl:value-of select="@lang"/>
            <xsl:text> --- </xsl:text>
            <xsl:for-each select="./*">
                <xsl:variable name="subType">
                    <xsl:value-of select="name()"/>
                </xsl:variable>
<!--                <xsl:choose>
                    <xsl:when test="$subType='name'">
                        <xsl:value-of select="mods:namePart"/>
                    </xsl:when>
                </xsl:choose>-->
                <xsl:value-of select="$subType"/>
                <xsl:text>:: </xsl:text>
                <xsl:value-of select="."/>
            </xsl:for-each>
            <xsl:text> ||| </xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="mods:identifier">
            <xsl:text>type:: </xsl:text>
            <xsl:value-of select="@type"/>
            <xsl:text> --- </xsl:text>
            <xsl:text>id:: </xsl:text>
            <xsl:value-of select="."/>
            <xsl:text> ||| </xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:for-each select="mods:originInfo">
            <xsl:for-each select="./*">
                <xsl:variable name="subType">
                    <xsl:value-of select="name()"/>
                </xsl:variable>
                <xsl:value-of select="$subType"/>
                <xsl:text>:: </xsl:text>
                <xsl:value-of select="."/>
                <xsl:text> --- </xsl:text>
            </xsl:for-each>
            <xsl:text> ||| </xsl:text>
        </xsl:for-each>
        <xsl:text>&#09;</xsl:text>
        <xsl:text disable-output-escaping="yes">&gt;</xsl:text>
        <xsl:value-of select="mods:note[@type='public']"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mods:recordInfo/mods:recordCreationDate"/>
        <xsl:text>&#09;</xsl:text>
        <xsl:value-of select="mods:recordInfo/mods:recordChangeDate"/>
        <xsl:text>&#xa;</xsl:text>
        
    </xsl:template>
 
</xsl:transform>