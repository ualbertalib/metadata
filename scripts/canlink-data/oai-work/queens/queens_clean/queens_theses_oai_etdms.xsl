<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:oai="http://www.openarchives.org/OAI/2.0/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ual="http://terms.library.ualberta.ca/" xmlns:bibo="http://purl.org/ontology/bibo/" xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:schema="https://schema.org/" xmlns:etdms="http://www.ndltd.org/standards/metadata/etdms/1.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
    <xsl:output indent="yes"/>
    <xsl:template match="oai:OAI-PMH">
        <rdf:RDF>
            <!-- // in the Xpath below allows matches for XML of aggregated (oai:ListRecords) and individual (oai:GetRecord) OAI responses -->
            <xsl:apply-templates select="//oai:record"/>
        </rdf:RDF>
    </xsl:template>
    <xsl:template match="oai:record">
        <xsl:choose>
            <xsl:when test="oai:header[@status = 'deleted']"/>
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
                            <xsl:value-of select="etdms:title"/>
                        </dcterms:title>
                        <ual:dissertant>
                            <xsl:value-of select="etdms:creator"/>
                        </ual:dissertant>
                        <xsl:call-template name="supervisor"/>
                        <ual:graduationDate>
                            <xsl:value-of select="etdms:date[1]"/>
                        </ual:graduationDate>
                        <xsl:call-template name="language"/>
                        <xsl:for-each select="etdms:identifier">
                            <xsl:if test="string-length() != 0">
                                <xsl:choose>
                                    <xsl:when test="position()=1">
                                        <ual:fedora3Handle>
                                            <!-- The handle IRI -->
                                            <xsl:attribute name="rdf:resource">
                                                <xsl:value-of select="."/>
                                            </xsl:attribute>
                                        </ual:fedora3Handle>                                    
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <dc:identifier>
                                            <!-- The pdf URL -->
                                            <xsl:attribute name="rdf:resource">
                                                <xsl:value-of select="."/>
                                            </xsl:attribute>
                                        </dc:identifier>                                    
                                    </xsl:otherwise>
                                </xsl:choose>                                
                            </xsl:if>
                        </xsl:for-each>
                        <xsl:for-each select="etdms:description">
                            <xsl:if test="position() = 1">
                                <xsl:call-template name="description"/>
                            </xsl:if>
                        </xsl:for-each>
                        <schema:inSupportOf>
                            <xsl:value-of select="etdms:degree/etdms:name"/>
                        </schema:inSupportOf>
                        <dc:contributor>
                            <xsl:value-of select="etdms:degree/etdms:discipline"/>
                        </dc:contributor>
                        <dcterms:publisher>
                            <xsl:attribute name="rdf:resource">http://dbpedia.org/resource/Queen's_University</xsl:attribute>
                        </dcterms:publisher>
                        <xsl:call-template name="subject"/>
                    </rdf:Description>
                </xsl:for-each>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="supervisor">
        <xsl:for-each select="etdms:contributor">
            <ual:supervisor>
                <xsl:value-of select="."/>
            </ual:supervisor>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="language">
        <xsl:for-each select="etdms:language">
            <dcterms:language>
                <xsl:value-of select="."/>
            </dcterms:language>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="description">
        <xsl:choose>
            <xsl:when test="position() = last()">
                <xsl:choose>
                    <xsl:when test="string-length() = 0"/>
                    <xsl:when test="starts-with(., 'Thesis (')"/>
                    <xsl:otherwise>
                        <dcterms:abstract>
                            <xsl:value-of select="."/>
                        </dcterms:abstract>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
                <dcterms:abstract>
                    <xsl:call-template name="abstract_constructor"/>
                </dcterms:abstract>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="abstract_constructor">
        <xsl:for-each select="../etdms:description">
            <xsl:choose>
                <xsl:when test="string-length() = 0"/>
                <xsl:when test="starts-with(., 'Thesis (')"/>
                <xsl:when test="position() = last()">
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
        <xsl:for-each select="etdms:subject">
            <dc:subject>
                <xsl:value-of select="."/>
            </dc:subject>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
