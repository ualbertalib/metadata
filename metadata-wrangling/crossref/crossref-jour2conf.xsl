<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:cr="http://www.crossref.org/schema/4.3.6"
    exclude-result-prefixes="xs"
    version="2.0">
    
    <xsl:output indent="yes" method="xml"/>    
    
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    
    <xsl:template match="cr:journal">
        <xsl:element name="conference" namespace="http://www.crossref.org/schema/4.3.6">
            <xsl:apply-templates select="@*|node()"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="cr:journal_metadata">
        <xsl:element name="event_metadata" namespace="http://www.crossref.org/schema/4.3.6">
            <xsl:apply-templates select="@*|cr:full_title"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template name="full_title" match="cr:full_title">
        <xsl:element name="conference_name" namespace="http://www.crossref.org/schema/4.3.6">
            <xsl:apply-templates select="@*"/>
            <xsl:value-of select="replace(.,': Extended Abstracts','')"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="cr:journal_issue">
        <xsl:element name="proceedings_metadata" namespace="http://www.crossref.org/schema/4.3.6">
            <xsl:call-template name="proc_meta"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template name="proc_meta">
        <xsl:element name="proceedings_title" namespace="http://www.crossref.org/schema/4.3.6">
            <xsl:value-of select="concat(replace(../cr:journal_metadata//cr:full_title,':',''),': ',descendant::cr:year)"/>
        </xsl:element>
        <xsl:element name="publisher" namespace="http://www.crossref.org/schema/4.3.6">
            <xsl:element name="publisher_name" namespace="http://www.crossref.org/schema/4.3.6">
                <xsl:text>University of Alberta</xsl:text>
            </xsl:element>
        </xsl:element>
        <xsl:apply-templates select="@*|descendant::cr:publication_date"/>
        <xsl:call-template name="isbn"/>
    </xsl:template>
    
    <xsl:template match="cr:journal_article">
        <xsl:element name="conference_paper" namespace="http://www.crossref.org/schema/4.3.6">
            <xsl:apply-templates select="@*|cr:titles|cr:doi_data"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template name="isbn">
        <xsl:variable name="vol">
            <xsl:value-of select="../cr:journal_issue//cr:volume"/>
        </xsl:variable>
        <xsl:element name="isbn" namespace="http://www.crossref.org/schema/4.3.6">

            <!-- specify ISBNs to be used -->
            <xsl:text>978-1-55195-516-2</xsl:text>
            
            <!-- when using a large number of ISBNs, use template below to apply ISBNs to be used for each volume
                
                <xsl:choose>
                <xsl:when test="$vol='7'">
                    <xsl:text>978-1-55195-420-2</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='6'">
                    <xsl:text>978-1-55195-424-0</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='5'">
                    <xsl:text>978-1-55195-417-2</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='4'">
                    <xsl:text>978-1-55195-419-6</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='3'">
                    <xsl:text>978-1-55195-415-8</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='2'">
                    <xsl:text>978-1-55195-418-9</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='1'">
                    <xsl:text>978-1-55195-416-5</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='8'">
                    <xsl:text>978-1-55195-422-6</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='9'">
                    <xsl:text>978-1-55195-423-3</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='10'">
                    <xsl:text>978-1-55195-421-9</xsl:text>
                </xsl:when>
                <xsl:when test="$vol='11'">
                    <xsl:text>978-1-55195-425-7</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>00000000-X</xsl:text>
                </xsl:otherwise>
            </xsl:choose>-->
        </xsl:element>
    </xsl:template>
    
    
</xsl:stylesheet>

<!-- conference --> <!-- journal -->
<!-- *event_metadata --> <!-- journal_metadata -->
    <!-- *conference_name --> <!-- full_title -->
    <!-- conference_accronym --> <!-- abbrev_title -->
    <!-- conference_sponsor -->
    <!-- conference_number -->
    <!-- conference_location -->
    <!-- conference_date -->

<!-- *proceedings_metadata -->
    <!-- *proceedings_title -->
    <!-- proceedings_subject -->
    <!-- *publisher / publisher_name -->
    <!-- publication_date / month -->
    <!-- publication_date / day -->
    <!-- *publication_date / year -->
    <!-- *isbn --> <!-- from description -->

<!-- *conference_paper -->
<!-- contributors / person_name / given_name-->
<!-- contributors / person_name / surname-->
<!-- contributors / person_name / ORCID-->
<!-- *titles / title -->
<!-- jats:abstract / jats:p -->
<!-- publication_date / month --> <!-- same -->
<!-- publication_date / day --> <!-- same -->
<!-- publication_date / year --> <!-- same -->
<!-- pages / first_page -->
<!-- pages / last_page -->
<!-- ai:program / ai:license_ref -->
<!-- *doi_data / doi -->
<!-- *doi_data / resource -->
<!-- doi_data / collection / item / resource -->


<!-- <person_name contributor_role="author" sequence="first">
            <given_name>Allyson</given_name>
            <surname>Mower</surname>
            <ORCID>https://orcid.org/0000-0002-4078-8088</ORCID>
          </person_name> -->
