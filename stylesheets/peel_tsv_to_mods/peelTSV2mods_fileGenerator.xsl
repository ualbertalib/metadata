<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mods="http://www.loc.gov/mods/v3"
    xmlns:peel="http://peel.library.ualberta.ca/mods-extensions">

    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

    <xsl:template match="//*[not(@* | * | comment() | processing-instruction()) and normalize-space() = '']"/>
    
    <xsl:template match="/">
        <xsl:for-each-group select="root/mods:mods" group-by="identifier">
            <xsl:for-each select="identifier">
                <xsl:variable name="filename">
                    <xsl:value-of select="."/>
                </xsl:variable>
                <xsl:result-document href="peel/{$filename}.xml">  
                    <xsl:copy-of select="current-group()"/>
                </xsl:result-document>
            </xsl:for-each>
        </xsl:for-each-group>
    </xsl:template>
</xsl:stylesheet>
