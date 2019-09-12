<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:mods="http://www.loc.gov/mods/v3"
    xmlns:peel="http://peel.library.ualberta.ca/mods-extensions"
    xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd"
    version="3.6">

    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    
    <xsl:template match="/">
               
        <xsl:for-each-group select="root/mods:mods" group-by="identifier">
            <xsl:for-each select="identifier">
                <xsl:variable name="filename">
                    <xsl:value-of select="."/>
                </xsl:variable>
                <xsl:variable name="folder">
                    <xsl:value-of select="substring($filename, 3, 3)"/>
                </xsl:variable>
                <xsl:result-document href="peel/{$filename}.xml">  
                    <xsl:copy-of select="current-group()"/>
                </xsl:result-document>
            </xsl:for-each>
        </xsl:for-each-group>
    </xsl:template>
   
</xsl:stylesheet>
