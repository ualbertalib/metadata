<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>
    
    <xsl:template match="/">
        
        <xsl:for-each-group select="root/codeBook" group-by="docDscr/citation/titlStmt/titl">
            <xsl:for-each select="docDscr/citation/titlStmt/titl">

                <xsl:result-document href="peel/{.}.xml">  
                    <xsl:copy-of select="current-group()"/>
                </xsl:result-document>
            </xsl:for-each>
        </xsl:for-each-group>
    </xsl:template>
    
    
</xsl:stylesheet>