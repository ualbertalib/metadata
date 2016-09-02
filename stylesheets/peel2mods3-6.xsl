<?xml version="1.0" encoding="UTF-8"?> 
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0"
     xmlns:mods="http://www.loc.gov/mods/v3"> 
      
     <!-- Identity transform --> 
     <xsl:template match="@* | node()"> 
         <xsl:copy> 
             <xsl:apply-templates select="@* | node()"/> 
         </xsl:copy> 
     </xsl:template> 
      
     <!-- replace namespace of elements in old namespace --> 
     <!--<xsl:template match="old:*"> 
         <xsl:element name="{local-name()}" namespace="http://someurl2"> 
             <xsl:apply-templates select="@* | node()"/> 
         </xsl:element> 
     </xsl:template>--> 
      
     <!-- replace xsi:schemaLocation attribute --> 
     <!--<xsl:template match="@xsi:schemaLocation"> 
         <xsl:attribute name="xsi:schemaLocation">http://www.loc.gov/standards/mods/v3/mods-3-6.xsd</xsl:attribute> 
     </xsl:template>--> 
      
     <xsl:template match="*:mods"> 
         <xsl:element name="mods" namespace="http://www.loc.gov/mods/v3"> 
             <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace> 
             <xsl:attribute name="xsi:schemaLocation">http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd</xsl:attribute> 
             <xsl:attribute name="version">3.6</xsl:attribute> 
             <xsl:apply-templates select="node()"/> 
         </xsl:element> 
     </xsl:template>
    
    
    <xsl:template match="@tyep">
        <xsl:attribute name="type">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>
    
    <xsl:template match="@Lang | @xml-lang">
        <xsl:attribute name="lang">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>
    
    <xsl:template match="*:subject/*:cartographics">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="*:scale"/>
            <xsl:apply-templates select="*:coordinates"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- //location/url/@access[matches(.,'raw object\d')] -->
    
    <xsl:template match="*:subject/*:name">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:element name="namePart" namespace="http://www.loc.gov/mods/v3">
                <xsl:value-of select="."/>
            </xsl:element>
        </xsl:copy>
    </xsl:template>
    
 </xsl:stylesheet>