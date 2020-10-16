<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:oai="http://www.openarchives.org/OAI/2.0/"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:ual="http://terms.library.ualberta.ca/"
    xmlns:bibo="http://purl.org/ontology/bibo/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:schema="https://schema.org/"
    xmlns:etdms="http://www.ndltd.org/standards/metadata/etdms/1.0/"
    xmlns:doc="http://www.lyncode.com/xoai"
    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <xsl:template match="wrapper">
        <rdf:RDF>
            <xsl:apply-templates select="oai:OAI-PMH/oai:ListRecords/oai:record"/>
        </rdf:RDF>
    </xsl:template>
    <xsl:template match="oai:record">
        <xsl:choose>
            <xsl:when test="oai:header[@status='deleted']"/>            
            <xsl:otherwise>
                <xsl:for-each select="oai:metadata/oai_dc:dc">
                    <xsl:variable name="thesisID">
                        <xsl:value-of select="concat('http://example.org/', encode-for-uri(../../oai:header/oai:identifier))"/>
                    </xsl:variable>
                    <rdf:Description>
                        <xsl:attribute name="rdf:about">
                            <xsl:value-of select="$thesisID"/>
                        </xsl:attribute>
                        <dcterms:title>
                            <xsl:value-of select="dc:title"/>
                        </dcterms:title>
                        <ual:dissertant>
                            <!-- names of creators and contributor individuals sometimes have a trailing whitespace -->
                            <xsl:value-of select="normalize-space(dc:creator)"/>
                        </ual:dissertant>
                        <ual:fedora3Handle>
                            <xsl:attribute name="rdf:resource">
                                <xsl:value-of select="dc:identifier[contains(., 'handle')]"/>                                
                            </xsl:attribute>
                        </ual:fedora3Handle>
                        <ual:graduationDate>
                            <!-- date format YYYY-MM - take the first 4 digits -->
                            <xsl:value-of select="substring(dc:date[1], 1, 4)"/>
                        </ual:graduationDate>
                        <dcterms:publisher>
                            <xsl:attribute name="rdf:resource">http://dbpedia.org/resource/University_of_Toronto</xsl:attribute>
                        </dcterms:publisher>
                        <xsl:call-template name="contributor"/>
                        <xsl:call-template name="description"/>
                        <xsl:call-template name="language"/>
                        <xsl:call-template name="subject"/>
                    </rdf:Description>
                </xsl:for-each>                
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="contributor">
        <!-- dc:contributor is used for both the names of supervisors and the department. When there are multiple supervisors, the department is always the last contributor element. 3 instances were found in the data where there was a supervisor but no department. The otherwise clause handles those cases. -->
        <xsl:for-each select="dc:contributor">
            <xsl:choose>
                <xsl:when test="following-sibling::dc:contributor[1]">
                    <ual:supervisor>
                        <xsl:value-of select="normalize-space(.)"/>
                    </ual:supervisor>                    
                </xsl:when>
                <xsl:when test="preceding-sibling::dc:contributor[1]">
                    <dc:contributor>
                        <xsl:value-of select="normalize-space(.)"/>
                    </dc:contributor>                    
                </xsl:when>
                <xsl:otherwise>
                    <ual:supervisor>
                        <xsl:value-of select="normalize-space(.)"/>
                    </ual:supervisor>                    
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="description">
        <xsl:for-each select="dc:description">
            <xsl:if test=".[text()]">
                <!-- the first two when clauses eliminates dc:description elements that state the name of the granting institution or that contain only a date value, respectively -->
                <xsl:choose>
                    <xsl:when test="matches(., '^[g][r][a][n][t][o][r]')"/>                    
                    <xsl:when test="matches(., '^\d\d\d\d[-]')"/>                                                            
                    <xsl:when test="string-length(.) lt 10">
                        <bibo:degree>
                            <xsl:value-of select="."/>
                        </bibo:degree>                        
                    </xsl:when>
                    <xsl:otherwise>
                        <dcterms:abstract>
                            <xsl:value-of select="."/>
                        </dcterms:abstract>                        
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>                       
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="subject">
        <xsl:for-each select="dc:subject">
            <xsl:choose>
                <!-- There is usually one subject value in the U of T data that is a 4 digit classification code. Often it's the final subject element, but not always. This test ensures it is not included in the output document -->
                <xsl:when test="matches((normalize-space(.)), '^\d\d\d\d$')">
                    <schema:genre>
                        <xsl:value-of select="normalize-space(.)"/>
                    </schema:genre>                    
                </xsl:when>
                <xsl:otherwise>
                    <dc:subject>
                        <xsl:value-of select="normalize-space(.)"/>
                    </dc:subject>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="language">
        <xsl:for-each select="dc:language">
            <xsl:choose>
                <xsl:when test=".[text()]">
                    <dcterms:language>
                        <xsl:value-of select="."/>
                    </dcterms:language>                
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>            
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>