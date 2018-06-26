<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:include href="cleanup.xsl"/>

    
    <xsl:template name="licenseURIs">
        <xsl:choose>
            <xsl:when test="contains(.,'Attribution_4.0_International')">
                <xsl:text>http://creativecommons.org/licenses/by/4.0/</xsl:text>
            </xsl:when>
            <xsl:when test="matches(.,'Attribution-NonCommercial.4\.0.International')">
                <xsl:text>http://creativecommons.org/licenses/by-nc/4.0/</xsl:text>
            </xsl:when>
            <xsl:when test="contains(.,'Attribution-NonCommercial-NoDerivs_4.0_International')">
                <xsl:text>http://creativecommons.org/licenses/by-nc-nd/4.0/</xsl:text>
            </xsl:when>
            <xsl:when test="contains(.,'Attribution-NonCommercial-ShareAlike_4.0_International')">
                <xsl:text>http://creativecommons.org/licenses/by-nc-sa/4.0/</xsl:text>
            </xsl:when>
            <xsl:when test="contains(.,'Attribution-ShareAlike_4.0_International')">
                <xsl:text>http://creativecommons.org/licenses/by-sa/4.0/</xsl:text>
            </xsl:when>
            <xsl:when test="contains(.,'Attribution-Non-Commercial-No Derivatives 3.0 Unported')">
                <xsl:text>http://creativecommons.org/licenses/by-nc-nd/3.0/</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="licenseCleanup"/>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
    
    
    
</xsl:stylesheet>