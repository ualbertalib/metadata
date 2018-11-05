<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:include href="mappings.xsl"/>
    
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
            <xsl:when test="matches(.,'Vasquez, David')">
                <xsl:value-of select="normalize-space(replace(.,'Vasquez, David','Vásquez, David'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Mario Allende')">
                <xsl:value-of select="normalize-space(replace(.,'Mario Allende','Allende, Mario'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Sergio Olivares')">
                <xsl:value-of select="normalize-space(replace(.,'Sergio Olivares','Olivares, Sergio'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Antonin Kubalek')">
                <xsl:value-of select="normalize-space(replace(.,'Antonin Kubalek','Kubalek, Antonin'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'MacIntosh')">
                <xsl:value-of select="normalize-space(replace(.,'MacIntosh','Macintosh'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'University of Alberta and Grant MacEwan College Jazz Bands')">
                <xsl:value-of select="normalize-space(replace(.,'University of Alberta and Grant MacEwan College Jazz Bands','Grant MacEwan College and University of Alberta Jazz Bands'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Dave Trautman')">
                <xsl:value-of select="normalize-space(replace(.,'Dave Trautman','Trautman, Dave'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Carol Chirino')">
                <xsl:value-of select="normalize-space(replace(.,'Carol Chirino','Chirino, Carol'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Ollikkala Debra')">
                <xsl:value-of select="normalize-space(replace(.,'Ollikkala Debra','Ollikkala, Debra'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Jei, Yin')">
                <xsl:value-of select="normalize-space(replace(.,'Jei, Yin','Yin, Jei'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Star, Red')">
                <xsl:value-of select="normalize-space(replace(.,'Star, Red','Red Star'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'De Frece')">
                <xsl:value-of select="normalize-space(replace(.,'De Frece','de Frece'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'van Brabant')">
                <xsl:value-of select="normalize-space(replace(.,'van Brabant','VanBrabant'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Giesbrecht Segger,')">
                <xsl:value-of select="normalize-space(replace(.,'Giesbrecht Segger,','Giesbrecht-Segger,'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Shadick-Talor')">
                <xsl:value-of select="normalize-space(replace(.,'Shadick-Talor,','Shadick-Taylor,'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Aresnault')">
                <xsl:value-of select="normalize-space(replace(.,'Aresnault','Arsenault'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Malcom')">
                <xsl:value-of select="normalize-space(replace(.,'Malcom','Malcolm'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Grella, Piotr$')">
                <xsl:value-of select="normalize-space(replace(.,'Grella, Piotr','Grella, Piotr A.'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Anderson, Jeff$')">
                <xsl:value-of select="normalize-space(replace(.,'Jeff','Jeffrey'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Friesen, Sandra$')">
                <xsl:value-of select="normalize-space(replace(.,'Friesen, Sandra','Friesen, Sandra Joy'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Whitehead, Russel$')">
                <xsl:value-of select="normalize-space(replace(.,'Russel','Russell'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Cook, Larry$')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Cook, Larry D.'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Glenn, Allison')">
                <xsl:value-of select="normalize-space(replace(.,'Glenn','Glen'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Mallany')">
                <xsl:value-of select="normalize-space(replace(.,'Mallany','Mallaney'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Loeween, Judy')">
                <xsl:value-of select="normalize-space(replace(.,'Loeween','Loewen'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Alechine, (l|I)our$')">
                <xsl:value-of select="normalize-space(replace(.,'Iour','Iouri'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Dunjerski')">
                <xsl:value-of select="normalize-space(replace(.,'Dunjerski','Dundjerski'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Zulstra, Robert')">
                <xsl:value-of select="normalize-space(replace(.,'Zulstra','Zylstra'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Au, Alicia')">
                <xsl:value-of select="normalize-space(replace(.,'Au, Alicia','Au, Alycia'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Storochuk, Allison$')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Storochuk, Allison M.'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Way-McClarty, Karen')">
                <xsl:value-of select="normalize-space(replace(.,'Karen','Karyn'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Hackelman, Allene')">
                <xsl:value-of select="normalize-space(replace(.,'Hackelman','Hackleman'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'New, Dianne')">
                <xsl:value-of select="normalize-space(replace(.,'New, Dianne','New, Diane'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Street, Willaim H.')">
                <xsl:value-of select="normalize-space(replace(.,'Willaim','William'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Golosky, Julia')">
                <xsl:value-of select="normalize-space(replace(.,'Julia','Julie'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Roos, Marikje')">
                <xsl:value-of select="normalize-space(replace(.,'Marikje','Marijke'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Curtist, Rob')">
                <xsl:value-of select="normalize-space(replace(.,'Curtist','Curtis'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Wylie, Michele')">
                <xsl:value-of select="normalize-space(replace(.,'Michele','Michelle'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Benhardt, Anthony')">
                <xsl:value-of select="normalize-space(replace(.,'Benhardt','Bernhardt'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Edmonton Wind Sinofnia')">
                <xsl:value-of select="normalize-space(replace(.,'Sinofnia','Sinfonia'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Després, Jacques$')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Després, Jacques C.'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Univerisity')">
                <xsl:value-of select="normalize-space(replace(.,'Univerisity','University'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Bayley, (Johnathan|Johnathon)')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Bayley, Jonathan'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Charleton, Karen')">
                <xsl:value-of select="normalize-space(replace(.,'Charleton','Charlton'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Radosh, Paul$')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Radosh, Paul J.'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Adamek, Magda$')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Adamek, Magdalena'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Neudorf, Juli$')">
                <xsl:value-of select="normalize-space(replace(.,'.+','Neudorf, Julianne'))"/>
            </xsl:when>
            <!--<xsl:when test="matches(.,'')">
                <xsl:value-of select="normalize-space(replace(.,'',''))"/>
            </xsl:when>
            <xsl:when test="matches(.,'')">
                <xsl:value-of select="normalize-space(replace(.,'',''))"/>
            </xsl:when>
            <xsl:when test="matches(.,'')">
                <xsl:value-of select="normalize-space(replace(.,'',''))"/>
            </xsl:when>
            <xsl:when test="matches(.,'')">
                <xsl:value-of select="normalize-space(replace(.,'',''))"/>
            </xsl:when>
            <xsl:when test="matches(.,'')">
                <xsl:value-of select="normalize-space(replace(.,'',''))"/>
            </xsl:when>
            <xsl:when test="matches(.,'')">
                <xsl:value-of select="normalize-space(replace(.,'',''))"/>
            </xsl:when>-->
            <xsl:when test="matches(.,'Wanat, Kim Mattice')">
                <xsl:value-of select="normalize-space(replace(.,'Wanat, Kim Mattice','Mattice Wanat, Kim'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'German Vergara')">
                <xsl:value-of select="normalize-space(replace(.,'German Vergara','Vergara, Germán'))"/>
            </xsl:when>
            <xsl:when test="matches(.,'Kenne?n?son, Claude')">
                <xsl:value-of select="normalize-space(replace(.,'Kenne?n?son','Kenneson'))"/>
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
            <xsl:when test="matches(.,'Tío')">
                <xsl:value-of select="normalize-space(replace(.,'Tío','Tio'))"/>
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
            <xsl:when test="parent::*//*:recordIdentifier[contains(.,$conHallList)]">
                <xsl:element name="accessCondition" namespace="http://www.loc.gov/mods/v3">
                    <xsl:text>University of Alberta Libraries license for educational use and research.</xsl:text>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*//*:recordIdentifier[matches(.,$UALLicensedList)]">
                <xsl:element name="accessCondition" namespace="http://www.loc.gov/mods/v3">
                    <xsl:text>This audiovisual content is being provided solely for educational use and research, pursuant to exceptions in the Canadian Copyright Act. Further reproduction or distribution or other use may require additional permissions.</xsl:text>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*//*:recordIdentifier[matches(.,$sandboxList)]">
                <xsl:element name="accessCondition" namespace="http://www.loc.gov/mods/v3">
                    <xsl:text>Dummy License Text</xsl:text>
                </xsl:element>
            </xsl:when>
            <!--<xsl:when test="*:accessCondition[@type='use and reproduction'][matches(.,'Attribution-NonCommercial 4.0 International')][preceding-sibling::accessCondition[@type='license']]"/>-->
            <xsl:otherwise>
                <xsl:call-template name="licenseURIs"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    
    <xsl:template name="noteCleanup">
        <xsl:element name="accessCondition" namespace="http://www.loc.gov/mods/v3">
            <xsl:attribute name="type">use and reproduction</xsl:attribute>
            <xsl:value-of select="normalize-space()"/>
        </xsl:element>
    </xsl:template>
    
    
</xsl:stylesheet>