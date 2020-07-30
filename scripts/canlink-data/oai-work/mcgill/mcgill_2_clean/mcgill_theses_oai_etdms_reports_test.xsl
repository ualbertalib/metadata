<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:oai="http://www.openarchives.org/OAI/2.0/" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:dcterms="http://purl.org/dc/terms/" xmlns:etdms="http://www.ndltd.org/standards/metadata/etdms/1.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd" exclude-result-prefixes="#all">
    <xsl:template match="fileIndex">
        <xsl:element name="wrapper">
            <xsl:call-template name="items"/>
        </xsl:element>
    </xsl:template>
    <xsl:template name="items">
        <xsl:for-each select="item">
            <xsl:variable name="fileName">
                <xsl:value-of select="."/>
            </xsl:variable>
            <xsl:for-each select="document($fileName)/oai:OAI-PMH/oai:ListRecords/oai:record/oai:metadata/etdms:thesis/etdms:contributor">
                <xsl:choose>
                    <!-- this removes the various role qualifying statements that occur in most values. -->
                    <xsl:when test="ends-with(normalize-space(.), '(advisor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(advisor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Co-Supervisor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Co-Supervisor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Co-supervisor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Co-supervisor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Contributor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Contributor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Cosupervisor2)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Cosupervisor2)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Internal/Cosupervisor2)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Internal/Cosupervisor2)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Internal/Cosupervisor3)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Internal/Cosupervisor3)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Internal/Supervisor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Internal/Supervisor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(project coordinator)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(project coordinator)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Supervisor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Supervisor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(supervisor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(supervisor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Supervisor>')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Supervisor>'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Supervisor1)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Supervisor1)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Supervisor2)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Supervisor2)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Supervisor3)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Supervisor3)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Supervisors)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Supervisors)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Thesis Advisor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Thesis Advisor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), '(Thesis Director)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), '(Thesis Director)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:when test="ends-with(normalize-space(.), 'Internal/Supervisor)')">
                        <xsl:variable name="supervisor2" select="normalize-space(substring-before(normalize-space(.), 'Internal/Supervisor)'))"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:variable name="supervisor2" select="normalize-space(.)"/>
                        <xsl:call-template name="superchop2">
                            <xsl:with-param name="supervisor2" select="$supervisor2"/>
                        </xsl:call-template>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="superchop2">
        <xsl:param name="supervisor2"/>
        <xsl:choose>
            <xsl:when test="starts-with($supervisor2, 'Dr.')">
                <xsl:variable name="supervisor3" select="normalize-space(substring-after($supervisor2, 'Dr.'))"/>
                <xsl:call-template name="superchop3">
                    <xsl:with-param name="supervisor3" select="$supervisor3"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="starts-with($supervisor2, 'Dr')">
                <xsl:variable name="supervisor3" select="normalize-space(substring-after($supervisor2, 'Dr'))"/>
                <xsl:call-template name="superchop3">
                    <xsl:with-param name="supervisor3" select="$supervisor3"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="starts-with($supervisor2, 'Prof.')">
                <xsl:variable name="supervisor3" select="normalize-space(substring-after($supervisor2, 'Prof.'))"/>
                <xsl:call-template name="superchop3">
                    <xsl:with-param name="supervisor3" select="$supervisor3"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="starts-with($supervisor2, 'Professeur')">
                <xsl:variable name="supervisor3" select="normalize-space(substring-after($supervisor2, 'Professeur'))"/>
                <xsl:call-template name="superchop3">
                    <xsl:with-param name="supervisor3" select="$supervisor3"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="starts-with($supervisor2, 'Professor')">
                <xsl:variable name="supervisor3" select="normalize-space(substring-after($supervisor2, 'Professor'))"/>
                <xsl:call-template name="superchop3">
                    <xsl:with-param name="supervisor3" select="$supervisor3"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:variable name="supervisor3" select="$supervisor2"/>
                <xsl:call-template name="superchop3">
                    <xsl:with-param name="supervisor3" select="$supervisor3"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="superchop3">
        <xsl:param name="supervisor3"/>
        <xsl:choose>
            <xsl:when test="matches($supervisor3, '\s[a][n][d]\s')">
                <xsl:analyze-string select="$supervisor3" regex="(.*)\s[a][n][d]\s(.*)">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="regex-group(1)"/>
                        </xsl:call-template>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="regex-group(2)"/>
                        </xsl:call-template>
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:when test="matches($supervisor3, '&amp;.*&amp;')">
                <xsl:analyze-string select="$supervisor3" regex="(.*)&amp;(.*)&amp;(.*)">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="normalize-space(regex-group(1))"/>
                        </xsl:call-template>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="normalize-space(regex-group(2))"/>
                        </xsl:call-template>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="normalize-space(regex-group(3))"/>
                        </xsl:call-template>
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:when test="matches($supervisor3, '&amp;')">
                <xsl:analyze-string select="$supervisor3" regex="(.*)&amp;(.*)">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="normalize-space(regex-group(1))"/>
                        </xsl:call-template>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="normalize-space(regex-group(2))"/>
                        </xsl:call-template>
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="superchop4">
                    <xsl:with-param name="superchop4" select="$supervisor3"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="superchop4">
        <xsl:param name="superchop4"/>
        <xsl:choose>
            <xsl:when test="matches($superchop4, '\s\w\s')">
                <xsl:analyze-string select="$superchop4" regex="(.*\s\w)(\s.*)">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="concat(regex-group(1), '.', regex-group(2))"/>
                        </xsl:call-template>
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:when test="matches($superchop4, '^\w\s')">
                <xsl:analyze-string select="$superchop4" regex="(^\w)(\s.*)">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop4">
                            <xsl:with-param name="superchop4" select="concat(regex-group(1), '.', regex-group(2))"/>
                        </xsl:call-template>                        
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:when test="matches($superchop4, '\s\w$')">
                <xsl:call-template name="superchop4">
                    <xsl:with-param name="superchop4" select="concat($superchop4, '.')"/>
                </xsl:call-template>                        
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="superchop5">
                    <xsl:with-param name="superchop5" select="$superchop4"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="superchop5">
        <xsl:param name="superchop5"/>
        <xsl:choose>
            <xsl:when test="matches($superchop5, '\w[.]\w')">
                <xsl:analyze-string select="$superchop5" regex="(.*\w[.])(\w.*)">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop5">
                            <xsl:with-param name="superchop5" select="concat(regex-group(1), ' ', regex-group(2))"/>
                        </xsl:call-template>        
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="superchop6">
                    <xsl:with-param name="superchop6" select="$superchop5"/>
                </xsl:call-template>                
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="superchop6">
        <xsl:param name="superchop6"/>
        <xsl:choose>
            <xsl:when test="matches($superchop6, '\w{3}[.]$')">
                <xsl:analyze-string select="$superchop6" regex="(.*\w{{3}})([.])$">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop7">
                            <xsl:with-param name="superchop7" select="regex-group(1)"/>
                        </xsl:call-template>                        
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="superchop7">
                    <xsl:with-param name="superchop7" select="$superchop6"/>
                </xsl:call-template>                
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
    <xsl:template name="superchop7">
        <xsl:param name="superchop7"/>
        <xsl:choose>
            <xsl:when test="matches($superchop7, '\s,')">
                <xsl:analyze-string select="$superchop7" regex="(.*)(\s)(,.*)">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop7">
                            <xsl:with-param name="superchop7" select="concat(regex-group(1), regex-group(2))"/>
                        </xsl:call-template>                                        
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:when test="matches($superchop7, ',\w')">
                <xsl:analyze-string select="$superchop7" regex="(.*,)(\w.*)">
                    <xsl:matching-substring>
                        <xsl:call-template name="superchop7">
                            <xsl:with-param name="superchop7" select="concat(regex-group(1), ' ', regex-group(2))"/>
                        </xsl:call-template>                                        
                    </xsl:matching-substring>
                </xsl:analyze-string>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="superchopLast">
                    <xsl:with-param name="superchopLast" select="$superchop7"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="superchopLast">
        <xsl:param name="superchopLast"/>
        <!-- add ual: namespace prefix to element name when finalizing -->
        <xsl:element name="supervisor">
            <xsl:value-of select="$superchopLast"/>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
