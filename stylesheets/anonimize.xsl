<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
    xmlns:foxml="info:fedora/fedora-system:def/foxml#"
    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:ualterms="http://terms.library.ualberta.ca"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:eraterms="http://era.library.ualberta.ca/eraterms"
    xmlns:thesis="http://www.ndltd.org/standards/metadata/etdms/1.0/"
    xmlns:vivo="http://vivoweb.org/ontology/core"
    xmlns:marcrel="http://id.loc.gov/vocabulary/relators"
    xmlns:bibo="http://purl.org/ontology/bibo/"
    exclude-result-prefixes="xs xd"
    version="3.0"> 
    
    
    <xsl:output method="xml" encoding="UTF-8" indent="yes"/>

    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="//*:abstract">
        <xsl:copy><xsl:text>Some Abstract</xsl:text></xsl:copy>
    </xsl:template>
    
    <xsl:template match="//*:alternative">
        <xsl:copy><xsl:text>Some Alternative Title</xsl:text></xsl:copy>
    </xsl:template>
    
    <xsl:template match="*:contributor">
        <xsl:copy><xsl:text>Some Contributor Name</xsl:text></xsl:copy>
    </xsl:template>
    
    <xsl:template match="//*:creator">
        <xsl:copy><xsl:text>Some Creator Name</xsl:text></xsl:copy>
    </xsl:template>
    
    <xsl:template match="//*:description">
        <xsl:copy><xsl:text>Some Descriptive Note</xsl:text></xsl:copy>
    </xsl:template>
    
    <xsl:template match="//marcrel:ths">
        <xsl:copy><xsl:text>Some Thesis Supervisor Name</xsl:text></xsl:copy>
    </xsl:template>
    
    <xsl:template match="//ualterms:thesiscommitteemember">
        <xsl:copy><xsl:text>Some Thesis Committee Member Name</xsl:text></xsl:copy>
    </xsl:template>    
    
    <xsl:template match="//*:title">
        <xsl:copy><xsl:text>Some Title</xsl:text></xsl:copy>
    </xsl:template>
    
    
</xsl:stylesheet>