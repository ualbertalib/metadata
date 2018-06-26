<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template name="nameCleanup">
        <xsl:choose>
            <xsl:when test="matches(.,',$')">
                <xsl:value-of select="normalize-space(replace(.,',$',''))"/>
            </xsl:when>
            <xsl:when test="matches(.,'[A-Za-z]+,[A-Za-z]+')">
                <xsl:value-of select="normalize-space(replace(.,'([A-Za-z]+,)([A-Za-z]+)','$1 $2'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'^The ')">
                <xsl:value-of select="normalize-space(replace(.,'^(The )(.*)','$2'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'^St\s')">
                <xsl:value-of select="normalize-space(replace(.,'St\s','St. '))"/>
            </xsl:when>
            <xsl:when test="matches(.,'^\s*([A-Za-z]+,\s*[A-Za-z]+\s*[A-Z])([^.\w]|$)')">
                <xsl:value-of select="normalize-space(replace(.,'(.+)','$1.'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'^\s*unknown\s*$')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Unknown'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Kennson, Claude')">
                <xsl:value-of select="normalize-space(replace(.,'Kennson','Kenneson'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Clarke, Al.*')">
                <xsl:value-of select="normalize-space(replace(.,'(Clarke, A).*','$1lan'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Krapf Gerhard')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Krapf, Gerhard'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Judu')">
                <xsl:value-of select="normalize-space(replace(.,'Judu','Judy'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Tsurta|Tsurata')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Tsuruta, Ayako'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Robinson, Zac')">
                <xsl:value-of select="normalize-space(replace(.,'Zac','Zak'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'LeRose')">
                <xsl:value-of select="normalize-space(replace(.,'LeRose','Le Rose'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'AlbertaMadrigal')">
                <xsl:value-of select="normalize-space(replace(.,'AlbertaMadrigal','Alberta Madrigal'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Hyo Young')">
                <xsl:value-of select="normalize-space(replace(.,'Hyo Young','Hyo-Young'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'(Scott Hoyt, Janet)|(Scott-Hoyt,Janet)|(Hoyt, Janet Scott)')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Scott-Hoyt, Janet'))"/>
            </xsl:when>
            <xsl:when test="text()='McNally, Michael'">
                <xsl:value-of select="normalize-space(replace(.,'(.+)','$1 B.'))"/>
            </xsl:when>
            <xsl:when test="text()='Martin, Gayle'">
                <xsl:value-of select="normalize-space(replace(.,'(.+)','$1 H.'))"/>
            </xsl:when>
            <xsl:when test="contains(.,'University of Alberta Stage Bands')">
                <xsl:value-of select="normalize-space(replace(.,'Bands','Band'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'(Ariel Calderon)|(Kathie Leitch)|(Libby Smith)|(Lisa Andrews)|(Lito Azocar)|(Marianne Elder)|(Muriel Affleck)|(Peter Mallaney)|(Sergio Contreras)|(Tomonori Sugiyama)|(Uday Ramdas)|(Janet Scott)')">
                <xsl:value-of select="normalize-space(replace(.,'(\w+)\s(\w+)','$2, $1'))"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="normalize-space()"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template name="geoCleanup">
        <xsl:choose>
            <xsl:when test="contains(.,'Convocation Hall')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Convocation Hall, University of Alberta'))"/>
            </xsl:when>
            <xsl:when test="contains(.,'Studio 27')">
                <xsl:text>Studio 27, Edmonton</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="normalize-space()"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template name="tempCleanup">
        <xsl:choose>
            <xsl:when test="matches(.,'\d+\s*\d+')">
                <xsl:value-of select="normalize-space(replace(.,'\s',''))"/>
            </xsl:when>
            
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template name="licenseCleanup">
        <xsl:choose>
            <xsl:when test="contains(.,'Access restricted to authorized users and institutions.')"/>
            <xsl:when test="contains(.,'User_Defined_Rights_Statement')"/>
            <xsl:when test="matches(.,'.ustom .ext')"/>
            <xsl:otherwise>
                <xsl:copy-of select="normalize-space(text())"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template name="noteCleanup">
        <xsl:choose>
            <xsl:when test="//*:note[not(//*:accessCondition)]">
                <xsl:element name="accessCondition">
                    <xsl:attribute name="type">use and reproduction</xsl:attribute>
                    <xsl:copy-of select="*:note/text()[matches(.,'(for educational use and research)|(terms of use)','ix')]"/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:copy copy-namespaces="yes"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
</xsl:stylesheet>