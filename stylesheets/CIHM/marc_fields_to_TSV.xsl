<?xml version="1.0"?>
<!-- Stylesheet to create reports from IA marc xml metadata -->

<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:mods="http://www.loc.gov/mods/v3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <xsl:text>Filename&#09;100a&#09;100*&#09;100-merged&#x9;110a&#09;110*&#09;110-merged&#x9;245a&#09;245*&#09;245-merged&#x9;260a&#x9;260*&#x9;260-merged&#x9;300a&#x9;300*&#x9;300-merged&#x9;500a&#x9;500*&#x9;500-merged&#x9;533a&#x9;533*&#x9;533-merged&#x9;534a&#x9;534*&#x9;534-merged&#x9;546a&#x9;546*&#x9;546-merged&#x9;600a&#x9;600*&#x9;600-merged&#x9;610a&#x9;610*&#x9;610-merged&#x9;611a&#x9;611*&#x9;611-merged&#x9;630a&#x9;630*&#x9;630-merged&#x9;650a&#x9;650*&#x9;650-merged&#x9;651a&#x9;651*&#x9;651-merged&#x9;700a&#x9;700*&#x9;700-merged&#x9;710a&#x9;710*&#x9;710-merged&#x9;711a&#x9;711*&#x9;711-merged&#xa;</xsl:text>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:variable name="docs"
        select="collection('../../metadata-wrangling/internet_archive_coll/university_of_alberta_libraries_microfilm/marc/?select=*marc.xml;recurse=no')"/>

    <xsl:variable name="d">"</xsl:variable>

    <xsl:template match="*">
        <xsl:for-each select="$docs//*:leader">
            <xsl:call-template name="context"/>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="context">
        <xsl:value-of select="subsequence(reverse(tokenize(base-uri(),'/')), 1, 1)"/>
        <xsl:text>&#x9;</xsl:text>
        <xsl:if test="not(//*:datafield[@tag='100'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 100]">
            <xsl:for-each select="//*:datafield[@tag = 100]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 100]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 100]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='110'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 110]">
            <xsl:for-each select="//*:datafield[@tag = 110]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 110]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 110]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='245'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 245]">
            <xsl:for-each select="//*:datafield[@tag = 245]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 245]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 245]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='260'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 260]">
            <xsl:for-each select="//*:datafield[@tag = 260]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 260]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 260]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='300'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 300]">
            <xsl:for-each select="//*:datafield[@tag = 300]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 300]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 300]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='500'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 500]">
            <xsl:for-each select="//*:datafield[@tag = 500]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 500]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 500]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='533'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 533]">
            <xsl:for-each select="//*:datafield[@tag = 533]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 533]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 533]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='534'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 534]">
            <xsl:for-each select="//*:datafield[@tag = 534]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 534]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 534]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='546'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 546]">
            <xsl:for-each select="//*:datafield[@tag = 546]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 546]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 546]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='600'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 600]">
            <xsl:for-each select="//*:datafield[@tag = 600]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 600]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 600]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='610'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 610]">
            <xsl:for-each select="//*:datafield[@tag = 610]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 610]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 610]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='611'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 611]">
            <xsl:for-each select="//*:datafield[@tag = 611]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 611]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 611]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='630'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 630]">
            <xsl:for-each select="//*:datafield[@tag = 630]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 630]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 630]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='650'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 650]">
            <xsl:for-each select="//*:datafield[@tag = 650]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 650]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 650]/*:subfield">
                    <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='651'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 651]">
            <xsl:for-each select="//*:datafield[@tag = 651]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 651]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 651]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='700'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 700]">
            <xsl:for-each select="//*:datafield[@tag = 700]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 700]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 700]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='710'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 710]">
            <xsl:for-each select="//*:datafield[@tag = 710]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 710]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 710]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="not(//*:datafield[@tag='711'])">
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:if test="//*:datafield[@tag = 711]">
            <xsl:for-each select="//*:datafield[@tag = 711]/*:subfield[@code ='a']">
                <xsl:value-of select="replace(concat(node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 711]/*:subfield[not(@* ='a')]">
                <xsl:value-of select="replace(concat(@*, ':', node(), '/ '), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
            <xsl:for-each select="//*:datafield[@tag = 711]/*:subfield">
                <xsl:value-of select="replace(concat(. ,':'), $d, '')"/>
            </xsl:for-each>
            <xsl:text>&#x9;</xsl:text>
        </xsl:if>
        <xsl:text>&#xa;</xsl:text>
    </xsl:template>

</xsl:transform>
