<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:georss="http://www.georss.org/georss/"
    xpath-default-namespace="http://www.icpsr.umich.edu/DDI" exclude-result-prefixes="xs"
    version="2.0">
    <xsl:output indent="yes"/>
    <xsl:strip-space elements="*"/>
    <xsl:template match="codeBook">
        <xsl:element name="ddi_to_dcterms" inherit-namespaces="no">
            <xsl:namespace name="dcterms">http://purl.org/dc/terms/</xsl:namespace>
            <xsl:namespace name="georss">http://www.georss.org/georss/</xsl:namespace>
            <!-- Title, subtitle and version number are concatenated  -->
            <xsl:element name="dcterms:title">
                <xsl:value-of select="normalize-space(stdyDscr/citation/titlStmt/titl)"/>
                <xsl:if test="stdyDscr/citation/titlStmt/subTitl">
                    <xsl:text> : </xsl:text>
                    <xsl:value-of select="normalize-space(stdyDscr/citation/titlStmt/subTitl)"/>
                </xsl:if>
            </xsl:element>
            <xsl:element name="dcterms:identifier">
                <xsl:value-of select="docDscr/citation/titlStmt/IDNo"/>
            </xsl:element>
            <xsl:for-each select="stdyDscr/citation/rspStmt/AuthEnty">
                <xsl:element name="dcterms:creator">
                    <xsl:value-of select="normalize-space(.)"/>
                </xsl:element>
            </xsl:for-each>
            <!-- producer is a multi-value element in Dataverse -->
            <xsl:for-each select="stdyDscr/citation/prodStmt/producer">
                <xsl:element name="dcterms:publisher">
                    <xsl:value-of select="normalize-space(.)"/>
                </xsl:element>
            </xsl:for-each>
            <xsl:element name="dcterms:created">
                <xsl:value-of select="stdyDscr/citation/prodStmt/prodDate"/>
            </xsl:element>
            <xsl:for-each select="stdyDscr/stdyInfo/subject/keyword">
                <xsl:element name="dcterms:subject">
                    <xsl:value-of select="normalize-space(.)"/>
                </xsl:element>
            </xsl:for-each>
            <xsl:for-each select="stdyDscr/stdyInfo/subject/topcClas">
                <xsl:element name="dcterms:subject">
                    <xsl:value-of select="normalize-space(.)"/>
                </xsl:element>
            </xsl:for-each>
            <!-- dataKind is included in dcterms:description, rather than dcterms:type because it is a free text field -->
            <!-- ddi:abstract, labeled 'description' in the metadata entry form, is a repeatable field in Dataverse -->
            <xsl:element name="dcterms:description">
                    <xsl:text>&lt;div&gt;&lt;p&gt;</xsl:text>
                        <xsl:text>This item is a resource in the University of Alberta Libraries' Dataverse Network. Access this item in Dataverse by clicking on the DOI link.</xsl:text>
                    <xsl:text>&lt;/p&gt;&lt;/div&gt;</xsl:text>
                <xsl:if test="stdyDscr/stdyInfo/sumDscr/dataKind">
                    <xsl:text>&lt;div&gt;&lt;p&gt;</xsl:text>
                    <xsl:text>Kind of data: </xsl:text>
                    <xsl:value-of select="stdyDscr/stdyInfo/sumDscr/dataKind"/>
                    <xsl:text>&lt;/p&gt;&lt;/div&gt;</xsl:text>
                </xsl:if>
                <xsl:for-each select="stdyDscr/stdyInfo/abstract">
                    <xsl:text>&lt;div&gt;</xsl:text>
                    <xsl:apply-templates select="."/>
                    <xsl:text>&lt;/div&gt;</xsl:text>
                </xsl:for-each>
            </xsl:element>
            <!-- Dataverse does not require that an end date be given with a start date or vice-versa -->
            <xsl:if
                test="stdyDscr/stdyInfo/sumDscr/timePrd[@event = 'start'] or stdyDscr/stdyInfo/sumDscr/timePrd[@event = 'end']">
                <xsl:element name="dcterms:temporal">
                    <xsl:choose>
                        <xsl:when test="stdyDscr/stdyInfo/sumDscr/timePrd[@event = 'start']">
                            <xsl:value-of
                                select="stdyDscr/stdyInfo/sumDscr/timePrd[@event = 'start']"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>[date undetermined]</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:text> - </xsl:text>
                    <xsl:choose>
                        <xsl:when test="stdyDscr/stdyInfo/sumDscr/timePrd[@event = 'end']">
                            <xsl:value-of select="stdyDscr/stdyInfo/sumDscr/timePrd[@event = 'end']"
                            />
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>[date undetermined]</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:element>
            </xsl:if>
            <!-- geogCover is a single value field in Dataverse -->
            <xsl:for-each select="stdyDscr/stdyInfo/sumDscr/geogCover">
                <xsl:element name="dcterms:spatial">
                    <xsl:value-of select="normalize-space(.)"/>
                </xsl:element>
            </xsl:for-each>
            <!-- nation is a single value field in Dataverse -->
            <xsl:for-each select="stdyDscr/stdyInfo/sumDscr/nation">
                <xsl:element name="dcterms:spatial">
                    <xsl:value-of select="normalize-space(.)"/>
                </xsl:element>
            </xsl:for-each>
            <xsl:for-each select="stdyDscr/stdyInfo/sumDscr/geoBndBox">
                <xsl:element name="georss:box">
                    <!-- South Latitude -->
                    <xsl:value-of select="southBL"/>
                    <xsl:text> </xsl:text>
                    <!-- West Longitude -->
                    <xsl:value-of select="westBL"/>
                    <xsl:text> </xsl:text>
                    <!-- North Latitude -->
                    <xsl:value-of select="northBL"/>
                    <xsl:text> </xsl:text>
                    <!-- East Longitude -->
                    <xsl:value-of select="eastBL"/>
                </xsl:element>
            </xsl:for-each>
            <!-- Given that the label for dcterms:relation in ERA is 'link to related resource', is it better to leave out these references altogether. These DDI elements are all mapped to dc:relation in the oai_dc flavoured export from Dataverse
            <xsl:for-each select="stdyDscr/othrStdyMat/relStdy">
                <dcterms:relation>
                    <xsl:value-of select="."/>
                </dcterms:relation>
            </xsl:for-each>
            <xsl:for-each select="stdyDscr/othrStdyMat/otherRefs">
                <dcterms:relation>
                    <xsl:value-of select="."/>
                </dcterms:relation>
            </xsl:for-each>
            <xsl:for-each select="stdyDscr/othrStdyMat/relMat">
                <dcterms:relation>
                    <xsl:value-of select="."/>
                </dcterms:relation>
            </xsl:for-each>  -->
            <!-- All resources from Dataverse are assigned the type 'Dataset' in HydraNorth -->
            <xsl:element name="dcterms:type">Dataset</xsl:element>
            <!-- dcterms:dateSubmitted and dcterms:modified are used in HydraNorth to help track new items for users. In Dataverse, the most consistent auto-generated dates are the ones associated with each version of the study. -->
            <xsl:element name="dcterms:dateSubmitted">
                <xsl:value-of select="docDscr/citation/verStmt[version = '1']/version/@date"/>
            </xsl:element>
            <xsl:element name="dcterms:modified">
                <xsl:value-of select="docDscr/citation/verStmt/version[@type = 'RELEASED']/@date"/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <xsl:template match="abstract">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>
</xsl:stylesheet>