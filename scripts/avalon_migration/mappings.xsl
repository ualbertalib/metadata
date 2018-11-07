<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:template name="licenseURIs">
        <xsl:element name="accessCondition" namespace="http://www.loc.gov/mods/v3">
            <xsl:attribute name="type">use and reproduction</xsl:attribute>
            <xsl:choose>
                <xsl:when test="matches(.,'Attribution.4.0.International')">
                    <xsl:text>http://creativecommons.org/licenses/by/4.0/</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'Attribution-NonCommercial.4.0.International')">
                    <xsl:text>http://creativecommons.org/licenses/by-nc/4.0/</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'Attribution-NonCommercial-NoDerivs.4.0.International')">
                    <xsl:text>http://creativecommons.org/licenses/by-nc-nd/4.0/</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'Attribution-NonCommercial-ShareAlike.4.0.International')">
                    <xsl:text>http://creativecommons.org/licenses/by-nc-sa/4.0/</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'Attribution-ShareAlike.4.0.International')">
                    <xsl:text>http://creativecommons.org/licenses/by-sa/4.0/</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'Attribution-Non-Commercial-No.Derivatives.3.0.Unported')">
                    <xsl:text>http://creativecommons.org/licenses/by-nc-nd/3.0/</xsl:text>
                </xsl:when>
                <xsl:when test="matches(.,'Attribution.NoDerivs.4.0.International')">
                    <xsl:text>https://creativecommons.org/licenses/by-nd/4.0/</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="normalize-space()"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:element>        
    </xsl:template>

    <!--http://localhost:3603/solr/development/select?fl=id,identifier_ssim&indent=on&q=has_model_ssim:%22MediaObject%22%20AND%20collection_ssim:%22Convocation%20Hall%20%22&rows=1000000&wt=csv -->
    <xsl:variable name="conHallList">
        <xsl:text>(avalon:27449)|(avalon:27480)|(avalon:27492)|(avalon:27510)|(avalon:27588)|(avalon:27602)|(avalon:27661)|(avalon:27735)|(avalon:27739)|(avalon:27741)|(avalon:27810)|(avalon:27817)|(avalon:27825)</xsl:text>
    </xsl:variable>
    
    <xsl:variable name="UALLicensedList">
        <xsl:text>(avalon:16977)|(avalon:16740)|(avalon:21435)</xsl:text>
    </xsl:variable>

    <xsl:variable name="sandboxList">
        <xsl:text>(avalon:13443)</xsl:text>
    </xsl:variable>

    
</xsl:stylesheet>