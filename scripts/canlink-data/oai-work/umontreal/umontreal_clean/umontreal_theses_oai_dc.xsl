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
    xmlns:ns2="http://dbpedia.org/ontology/"
    xmlns:etdms="http://www.ndltd.org/standards/metadata/etdms/1.1/"
    xmlns:doc="http://www.lyncode.com/xoai"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <xsl:output indent="yes"/>
    <xsl:template match="oai:OAI-PMH">
        <rdf:RDF>
            <xsl:apply-templates select="oai:ListRecords/oai:record"/>
        </rdf:RDF>
    </xsl:template>
    <xsl:template match="oai:record">
        <xsl:choose>
            <xsl:when test="oai:header[@status='deleted']"/>
            <xsl:otherwise>
                <xsl:for-each select="oai:metadata/etdms:thesis">
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
                        <xsl:call-template name="contributor"/>  
                        <ual:graduationDate>
                            <!-- date format YYYY-MM - take the first 4 digits -->
                            <xsl:value-of select="substring(dc:date[1], 1, 4)"/>
                        </ual:graduationDate>
                        <xsl:call-template name="language"/>
                        <ual:fedora3Handle>
                            <xsl:attribute name="rdf:resource">
                                <xsl:value-of select="dc:identifier[contains(., 'handle')]"/>
                            </xsl:attribute>
                        </ual:fedora3Handle>
                        <xsl:for-each select="dc:identifier">
                            <!-- This will result in a few items that have more than one pdf, generally music composition works that include score(s) in addition to a text. Note that a few dozen items are embodied in html and have no pdf. -->
                            <xsl:if test="contains(lower-case(.), '.pdf')">
                                <xsl:element name="dc:identifier">
                                    <xsl:value-of select="."/>
                                </xsl:element>
                            </xsl:if>
                        </xsl:for-each>
                        <xsl:for-each select="dc:description[@role='abstract']">
                            <xsl:if test="not(preceding-sibling::dc:description[@role='abstract'])">
                                <dcterms:abstract>
                                    <xsl:call-template name="abstract_constructor"/>
                                </dcterms:abstract>
                            </xsl:if>
                        </xsl:for-each>
                        <schema:inSupportOf>
                            <xsl:value-of select="etdms:degree/etdms:name"/>
                        </schema:inSupportOf>
                        <xsl:for-each select="etdms:degree/etdms:discipline">
                            <ns2:academicDiscipline>
                                <xsl:value-of select="."/>
                            </ns2:academicDiscipline>                            
                        </xsl:for-each>
                        <dcterms:publisher>
                            <xsl:attribute name="rdf:resource">http://dbpedia.org/resource/Université_de_Montréal</xsl:attribute>
                        </dcterms:publisher>
                        <xsl:call-template name="subject"/>
                    </rdf:Description>
                </xsl:for-each>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="contributor">
        <xsl:for-each select="dc:contributor">
            <ual:supervisor>
                <xsl:value-of select="normalize-space(.)"/>
            </ual:supervisor>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="language">
        <xsl:for-each select="dc:language">
            <xsl:choose>
                <xsl:when test=".[text()]">
                    <dcterms:language>
                        <xsl:choose>
                            <xsl:when test=".[@xsi:type='dcterms:ISO639-3']">
                                <xsl:attribute name="rdf:resource">
                                    <xsl:text>https://iso639-3.sil.org/code/</xsl:text>
                                    <xsl:value-of select="."/>
                                </xsl:attribute>                                
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="."/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </dcterms:language>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="abstract_constructor">
        <!-- All descriptions are typed with the @role attribute as 'abstract' or 'note'. The stylesheet excludes 'note' descriptions and combines multiple 'abstract' descriptions into one dcterms:abstract element  -->
        <xsl:for-each select="../dc:description[@role='abstract']">
            <xsl:choose>
                <xsl:when test="not(following-sibling::dc:description[@role='abstract'])">
                    <xsl:value-of select="."/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="."/>
                    <xsl:text> -- </xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="subject">
        <xsl:for-each select="dc:subject">
            <dc:subject>
                <xsl:value-of select="normalize-space(.)"/>
            </dc:subject>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>