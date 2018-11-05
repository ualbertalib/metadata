<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:foxml="info:fedora/fedora-system:def/foxml#"
   xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:dcterms="http://purl.org/dc/terms/"
   exclude-result-prefixes="xs"
   version="2.0">
   
   <xsl:output method="xml" encoding="UTF-8" indent="no"/>
   <xsl:include href="cleanup.xsl"/>
   
   
   <xsl:template match="@*|node()">
      <xsl:copy>
         <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
   </xsl:template>
   
   <xsl:template match="*:mods">
      <xsl:copy>
         <xsl:apply-templates select="@*|node()"/>
         <xsl:if test="//*:recordIdentifier[matches(.,concat($conHallList,'|',$UALLicensedList,'|',$sandboxList))]">
            <xsl:text>&#xa;</xsl:text>
            <xsl:call-template name="addLicense"/>
            <xsl:text>&#xa;</xsl:text>
         </xsl:if>
      </xsl:copy>
   </xsl:template>
   
   <xsl:template match="//*:namePart">
      <xsl:copy copy-namespaces="yes">
         <xsl:call-template name="nameCleanup"/>         
      </xsl:copy>
   </xsl:template>
   
   <xsl:template match="//*:geographic">
      <xsl:copy copy-namespaces="yes">
         <xsl:call-template name="geoCleanup"/>         
      </xsl:copy>
   </xsl:template>
   
   <xsl:template match="//*:temporal">
      <xsl:copy copy-namespaces="yes">
         <xsl:call-template name="tempCleanup"/>         
      </xsl:copy>
   </xsl:template>
   
   <xsl:template name="addLicense">
      <xsl:element name="accessCondition" namespace="http://www.loc.gov/mods/v3">
         <xsl:attribute name="type">use and reproduction</xsl:attribute>
      <xsl:choose>
         <xsl:when test="//*:recordIdentifier[matches(.,$conHallList)]">
            <xsl:text>This audiovisual content is being provided solely for educational use and research, pursuant to exceptions in the Canadian Copyright Act. Further reproduction or distribution or other use may require additional permissions.</xsl:text>
         </xsl:when>
         <xsl:when test="//*:recordIdentifier[matches(.,$UALLicensedList)]">
            <xsl:text>University of Alberta Libraries license for educational use and research.</xsl:text>
         </xsl:when>
         <xsl:when test="//*:recordIdentifier[matches(.,$sandboxList)]">
            <xsl:text>Dummy License Text</xsl:text>
         </xsl:when>
      </xsl:choose>
      </xsl:element>
   </xsl:template>
   
   <xsl:template match="//*:accessCondition">
      <xsl:call-template name="licenseCleanup"/>            
   </xsl:template>
   
   <xsl:template match="//*:physicalDescription[not(*)]"/>
   
   
   <xsl:template match="//*:note[matches(.,'(content is being provided solely for educational use and research)|(terms of use)','i')]" priority="5">
      <xsl:call-template name="noteCleanup"/>
   </xsl:template>
   
   
   <!--<xsl:template match="//*:genre">
      <xsl:copy copy-namespaces="yes">
         <xsl:call-template name="genreCleanup"/>
      </xsl:copy>
   </xsl:template>-->
   

   
</xsl:stylesheet>