<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:mods="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="xs" version="2.0"
    xpath-default-namespace="http://www.ualberta.ca/~jhuck">
    <xsl:output indent="yes"/>

    <!-- Apply this stylsheet to an XML document consisting of a single element <index>, containing a set of <doc> elements, each containing a filename (minus the file extension), which collectively represent all possible sequential filenames in a particular Peel collection. This document can be created by autopopulating the sequence of letter-prefixed numbers in a spreadsheet program (e.g., P000001 to the highest number in the filenames), copying the result to a simple text file, and running a find-replace task to replace each line break with '</doc>[line-break]<doc>' (with manual cleanup for first and last lines), saving the result as an .xml file.
            
            The stylesheet breaks each filename down to derive the folder structure that contains the file, and uses it to create a complete filepath value to use with the document() function. Because the particular configuration of containing folders and filename character length vary from collection to collection (e.g., P/[00-01]/[00-99]/[file] vs. PC/[000-032]/[file]), it is necessary to adapt the stylesheet for each collection. This stylesheet is configured for the main Peel collection. The first part of the filepath will naturally need to be adapted to the particulars of the local copy of the fileset being queried. -->

    <xsl:template match="/">
        <xsl:element name="modsCollection" namespace="http://www.loc.gov/mods/v3">
            <xsl:apply-templates select="index/doc"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="index/doc">
        <xsl:variable name="folder1">
            <xsl:analyze-string select="." regex="^\w(\w\w)(\w\w)\w\w$">
                <xsl:matching-substring>
                    <xsl:value-of select="regex-group(1)"/>
                </xsl:matching-substring>
            </xsl:analyze-string>
        </xsl:variable>
        <xsl:variable name="folder2">
            <xsl:analyze-string select="." regex="^\w(\w\w)(\w\w)\w\w$">
                <xsl:matching-substring>
                    <xsl:value-of select="regex-group(2)"/>
                </xsl:matching-substring>
            </xsl:analyze-string>
        </xsl:variable>
        <xsl:apply-templates
            select="document(concat('file:///Users/johnhuck/Desktop/Libraries/Peel/Peel Metadata 2016-07-29/P/', $folder1, '/', $folder2, '/', ., '.xml'))/mods:mods/mods:name"
        />
    </xsl:template>

    <xsl:template match="mods:name">
        <xsl:element name="mods" namespace="http://www.loc.gov/mods/v3">
            <xsl:attribute name="ID">
                <xsl:value-of select="following-sibling::mods:recordInfo/mods:recordIdentifier"/>
            </xsl:attribute>
            <xsl:copy-of select="."/>
        </xsl:element>
    </xsl:template>
    
</xsl:stylesheet>
