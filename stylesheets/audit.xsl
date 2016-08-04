<?xml version="1.0" encoding="UTF-8"?> 
 
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    exclude-result-prefixes="xs" 
    version="3.0"> 

 
    <xsl:output method="text" indent="yes"/> 

 
    <xsl:template match="*">         
 
        <xsl:for-each select="collection('/home/mparedes/metadata_work/ERA_files/post-migration/20160603/2016?select=*.xml;recurse=yes')//*:digitalObject"> 
             <xsl:value-of select="@PID"/> 
            <xsl:text>&#09;</xsl:text> 
            <xsl:value-of select="//*:property[@NAME='info:fedora/fedora-system:def/model#state']/@VALUE"/> 
            <xsl:text>&#09;</xsl:text> 
            <xsl:value-of select="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//*:embargoedDate"/> 
            <xsl:text>&#09;</xsl:text> 
            <xsl:value-of select="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//*:isPartOf/@*:resource"/> 
            <xsl:text>&#09;</xsl:text> 
            <xsl:value-of select="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//*:isMemberOf/@*:resource"/> 
            <xsl:text>&#09;</xsl:text> 
            <xsl:value-of select="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//*:isMemberOfCollection/@*:resource"/> 
            <xsl:text>&#09;</xsl:text> 
            <xsl:value-of select="//*:datastream[@ID='RELS-EXT']/*:datastreamVersion[last()]//*:workflowState"/> 
            <xsl:text>&#xa;</xsl:text> 
        </xsl:for-each> 
    </xsl:template>
    

</xsl:stylesheet>