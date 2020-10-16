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
    <xsl:template match="oai:OAI-PMH">
        <identifiers>            
            <xsl:apply-templates select="oai:ListRecords/oai:record/oai:header/oai:identifier"/>
        </identifiers>
    </xsl:template>
    <xsl:template match="oai:identifier">
        <identifier>
            <xsl:value-of select="."/>
        </identifier>
    </xsl:template>
</xsl:stylesheet>