<?xml version="1.0" encoding="UTF-8"?> 
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0"
     xmlns:mods="http://www.loc.gov/mods/v3"
     xmlns:peel="http://peel.library.ualberta.ca/mods-extensions"> 
    
    <xsl:output media-type="xml" indent="yes"/>
    <xsl:strip-space elements="*"/>
      
     <!-- Identity transform --> 
     <xsl:template match="@* | node()"> 
         <xsl:copy copy-namespaces="no"> 
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
    
    
    <!-- Validation issues -->
    
    <xsl:template match="//*:nonsort">
        <xsl:element name="nonSort" namespace="http://www.loc.gov/mods/v3">
                <xsl:apply-templates select="@*"/>
                <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="@tyep">
        <xsl:attribute name="type">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>
    
    <xsl:template match="@Lang | @xml-lang">
        <xsl:attribute name="lang">
            <xsl:choose>
                <xsl:when test=".='en'">
                    <xsl:text>eng</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>           
    </xsl:template>
    
    <xsl:template match="//*:subject/*:cartographics">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:apply-templates select="*:scale"/>
            <xsl:apply-templates select="*:coordinates"/>
        </xsl:copy>
    </xsl:template>
    
    <!-- //location/url/@access[matches(.,'raw object\d')] -->
    
    <xsl:template match="//*:subject/*:name">
        <xsl:copy>
            <xsl:apply-templates select="@*"/>
            <xsl:element name="namePart" namespace="http://www.loc.gov/mods/v3">
                <xsl:value-of select="."/>
            </xsl:element>
        </xsl:copy>
    </xsl:template>
    
    
   <xsl:template match="//*:originInfo/*:originInfo">
       <xsl:apply-templates select="./node()|./@*"></xsl:apply-templates>
   </xsl:template>
    
    <xsl:template match="//*:mods/*:url">
        <xsl:element name="location" namespace="http://www.loc.gov/mods/v3">
            <xsl:element name="{local-name()}" namespace="http://www.loc.gov/mods/v3">
                <xsl:apply-templates select="@* | node()"/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    
    
   <!-- Remove -->
    
    <xsl:template match="//*[not(@*|*|comment()|processing-instruction()) and normalize-space()='']"/>
    
    <xsl:template match="//*:part/*:detail[normalize-space()='']"/>
    
    <!-- Remove extensions namespace -->
    <xsl:template match="//*[@peel:qualifier]">
        <xsl:element name="{local-name()}" namespace="http://www.loc.gov/mods/v3">
            <xsl:apply-templates select="@* | node()"/>
        </xsl:element>
    </xsl:template>
    
    <!-- Relocate peel attributes -->
    <xsl:template match="//*:place/@peel:qualifier"/>
    
    <xsl:template match="//*:place[@*:qualifier]/*:placeTerm">
        <xsl:copy copy-namespaces="no">
            <xsl:attribute name="script">
                <xsl:value-of select="../../*:place/@*:qualifier"/>
            </xsl:attribute>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="//*:publisher/@peel:qualifier">
        <xsl:attribute name="supplied">yes</xsl:attribute>
    </xsl:template>
    
     <!-- Ordering -->   
    <xsl:template match="//*:location/*:url/@access[matches(.,'\d')]">
        <xsl:attribute name="access">
            <xsl:value-of select="replace(.,'([a-z\s]+)\d+','$1')"/>
        </xsl:attribute>
        <xsl:attribute name="displayLabel">
            <xsl:value-of select="replace(.,'[a-z\s]+(\d+)','$1')"/>
        </xsl:attribute>
    </xsl:template>
    

<!-- @ID
1139 Q (1 title) (relateditem.\d*, t\d*)
142 PCX (\d*)
858 PC (\d*, verso, PC013011, PC014592, PC014593, PC014594)
2641 P (t\d*, relateditem.\d*, host)
12726 N (t\d* and relateditem.\d*)
 -->
    <xsl:template match="//*:relatedItem/@ID[matches(.,'^\d+$')]">
        <xsl:attribute name="ID">
            <xsl:value-of select="concat('p',.)"/>
        </xsl:attribute>
    </xsl:template>
    
 </xsl:stylesheet>