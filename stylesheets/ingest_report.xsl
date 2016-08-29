<?xml version="1.0" encoding="UTF-8"?>  
   
 <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  
     xmlns:xs="http://www.w3.org/2001/XMLSchema"  
     exclude-result-prefixes="xs"  
     version="3.0">  
  
   
     <xsl:output method="text" indent="yes"/>  
  
   
     <xsl:template match="*">          
   
         <xsl:for-each select="collection('/home/mparedes/metadata_work/ERA_files/post-migration/audit_reported_items?select=*.xml;recurse=yes')//*:RDF">  
             <xsl:value-of select="//*:Description/@*:about"/>  
             <xsl:text>&#09;</xsl:text>  
             <xsl:value-of select="//*:embargoedDate"/>  
             <xsl:text>&#09;</xsl:text>  
             <xsl:value-of select="//*:isPartOf/@*:resource"/>  
             <xsl:text>&#09;</xsl:text>  
             <xsl:value-of select="//*:isMemberOf/@*:resource"/>  
             <xsl:text>&#09;</xsl:text>  
             <xsl:value-of select="//*:isMemberOfCollection/@*:resource"/>  
             <xsl:text>&#09;</xsl:text>  
             <xsl:value-of select="//*:workflowState"/>  
             <xsl:text>&#xa;</xsl:text>  
         </xsl:for-each>  
     </xsl:template> 
      
  
 </xsl:stylesheet>