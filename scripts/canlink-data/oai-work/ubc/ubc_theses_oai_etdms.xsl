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
                        <ual:fedora3Handle>
                            <xsl:attribute name="rdf:resource">
                                <xsl:value-of select="etdms:identifier[1]"/>                                
                            </xsl:attribute>
                        </ual:fedora3Handle>
                        <ual:graduationDate>
                            <xsl:value-of select="etdms:date[1]"/>
                        </ual:graduationDate>
                        <dcterms:language>
                            <xsl:value-of select="etdms:language"/>
                        </dcterms:language>
                        <dcterms:abstract>
                            <xsl:value-of select="etdms:description"/>
                        </dcterms:abstract>
                        <schema:inSupportOf>
                            <xsl:value-of select="etdms:degree/etdms:name"/>
                        </schema:inSupportOf>
                        <bibo:degree>
                            <xsl:value-of select="etdms:degree/etdms:level"/>
                        </bibo:degree>
                        <dcterms:publisher>
                            <xsl:attribute name="rdf:resource">http://dbpedia.org/resource/University_of_British_Columbia</xsl:attribute>
                        </dcterms:publisher>
                        <xsl:call-template name="subject"/>
                    </rdf:Description>
                </xsl:for-each>                
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="subject">
        <xsl:for-each select="etdms:subject">
            <dc:subject>
                <xsl:value-of select="."/>
            </dc:subject>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>