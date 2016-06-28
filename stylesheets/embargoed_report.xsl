<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="3.0">
    
    <xsl:output method="text" indent="yes"/>
    
    <!--<xsl:template match="*" name="main">
        <xsl:apply-templates select="collection('/home/mparedes/metadata_work/ERA_files/post-migration/unembargo_20160615_original/?select=*.xml')/*"/>
    </xsl:template>-->
    
    
    <xsl:template match="*">        
        <xsl:for-each select="collection('/home/mparedes/metadata_work/ERA_files/post-migration/unembargo_20160615_transformed/?select=*.xml;recurse=yes')//*:digitalObject">
            <xsl:if test="//*:datastream[@ID='RELS-EXT']//*:embargoedDate">
                <xsl:value-of select="(//*:datastream[@ID='RELS-EXT']//*:embargoedDate)[last()]"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="(//*:datastream[@ID='DCQ']//*:graduationdate)[last()]"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="(//*:datastream[@ID='DCQ']//*:title)[last()]"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="(//*:datastream[@ID='DCQ']//*:dis)[last()]"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="(//*:datastream[@ID='RELS-EXT']//*:isMemberOfCollection/@*:resource)[last()]"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="(//*:datastream[@ID='RELS-EXT']//*:workflowState)[last()]"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="(//*:datastream[@ID='DCQ']//*:fedora3handle)[last()]"/>        
                <xsl:text>&#09;</xsl:text>
                <xsl:value-of select="concat('https://thesisdeposit.library.ualberta.ca/public/view/item/',@PID)"/>
                <xsl:text>&#xa;</xsl:text>
<!--                <xsl:value-of select="(//*:datastream[@ID='DCQ']//*:identifier[contains(.,'handle')])[last()]"/>
                <xsl:text>&#xa;</xsl:text>-->
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
    
    
</xsl:stylesheet>