<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:bf="http://id.loc.gov/ontologies/bibframe/"
    xmlns:bflc="http://id.loc.gov/ontologies/bflc/"
    xmlns:madsrdf="http://www.loc.gov/mads/rdf/v1#"
    exclude-result-prefixes="xs xsl rdf rdfs bf bflc madsrdf"
    version="2.0">
    
    <xsl:output indent="yes" media-type="xml"/>
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="*">
        <xsl:element name="rdf:RDF">
            <xsl:namespace name="rdfs">http://www.w3.org/2000/01/rdf-schema#</xsl:namespace>
            <xsl:namespace name="bf">http://id.loc.gov/ontologies/bibframe/</xsl:namespace>
            <xsl:namespace name="bflc">http://id.loc.gov/ontologies/bflc/</xsl:namespace>
            <xsl:namespace name="madsrdf">http://www.loc.gov/mads/rdf/v1#</xsl:namespace>
        <xsl:for-each select="rdf:RDF">
            <xsl:copy-of select="@*|node()"/>
        </xsl:for-each>
        </xsl:element>
    </xsl:template>
    
</xsl:stylesheet>