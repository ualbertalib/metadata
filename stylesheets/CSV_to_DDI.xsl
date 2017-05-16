<xsl:stylesheet xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:fn="fn" xmlns:xs="http://www.w3.org/2001/XMLSchema" version="2.0"
    exclude-result-prefixes="fn xsl xs">

    <!-- stylesheet to transform peel postcard csv/tsv template to MODS/XML -->
    <xsl:output indent="yes" encoding="UTF-8"/>

    <!-- location of the tsv/csv file -->
    <xsl:param name="doc" select="'file:///home/mparedes/local-peel.git/test3_DDI.tsv'"/>

    <xsl:function name="fn:rows" as="xs:string+">
        <xsl:param name="str" as="xs:string"/>
        <xsl:analyze-string select="concat($str, ',')" regex="([^\t][^\t]*)\t?|\t">
            <xsl:matching-substring>
                <xsl:sequence select="regex-group(1)"/>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:function>

    <!-- list for who_access field -->
    <xsl:variable name="access_condition" as="element()*">
        <Item>Access is limited to selected members of the research team</Item>
        <Item>Access is limited to selected institution employees</Item>
        <Item>Access is limited to "Deemed employees" or trusted third parties, subject to the same
            undertaking of confidentiality as the data holder (e.g. institution employees)</Item>
        <Item>Access is limited to the research team</Item>
        <Item>Access is limited to collaborators at local sites of a multi-site study</Item>
        <Item>Access is permitted for external researchers, with limitations</Item>
        <Item>Access is permitted for external researchers, without limitations</Item>
        <Item>Access is permitted to the general public, without limitations</Item>
        <Item>Other/Not listed</Item>
    </xsl:variable>

    <!-- list for eq_app field -->
    <xsl:variable name="restrictions" as="element()*">
        <Item>Author determines access on a case-by-case basis</Item>
        <Item>Appropriate training</Item>
        <Item>Data-sharing agreement, including undertaking of confidentiality</Item>
        <Item>Disclosure of enough data to answer the intended research question</Item>
        <Item>No direct access for researchers external to the research team</Item>
        <Item>No restrictions on use</Item>
        <Item>Access only for REB-approved projects</Item>
        <Item>Review by institution data privacy committees</Item>
        <Item>Other/Not listed</Item>
    </xsl:variable>

    <!-- list for avlstatus field -->
    <xsl:variable name="avlStatus" as="element()*">
        <Item>Available: Data is openly available</Item>
        <Item>Restricted: Data may be available but requires the user to request permission before
            access can be granted.</Item>
        <Item>Not yet available: Data may be unavailable because it is still being collected,
            because it is embargoed for a period of time, because it has been superseded,
            etc.</Item>
        <Item>Not available: Data will not be shared because of sensitivity or other issues.</Item>
    </xsl:variable>

    <!-- list for collectionmode field -->
    <xsl:variable name="collection_mode" as="element()*">
        <Item>Face-to-face interview</Item>
        <Item>Computer assisted face-to-face interview</Item>
        <Item>Pen and paper face-to-face interview</Item>
        <Item>Telephone interview</Item>
        <Item>E-mail interview</Item>
        <Item>Web-based interview</Item>
        <Item>Self-administered questionnaire: E-mail</Item>
        <Item>Self-administered questionnaire: Paper</Item>
        <Item>Self-administered questionnaire: SMS/MMS</Item>
        <Item>Self-administered questionnaire: Web-based</Item>
        <Item>Self-administered writings and/or diaries</Item>
        <Item>Focus group</Item>
        <Item>Observation</Item>
        <Item>Experiment</Item>
        <Item>Recording</Item>
        <Item>Educational measurements and tests</Item>
        <Item>Physical measurements and tests</Item>
        <Item>Psychological measurements and tests</Item>
        <Item>Other</Item>
    </xsl:variable>

    <!-- list for kindofdata field -->
    <xsl:variable name="data_kind" as="element()*">
        <Item>Administrative data</Item>
        <Item>Anthropometric data</Item>
        <Item>Audiovisual data</Item>
        <Item>Biosamples</Item>
        <Item>Clinical data</Item>
        <Item>Descriptive (textual) data</Item>
        <Item>Experimental data</Item>
        <Item>Focus group data</Item>
        <Item>Interview data</Item>
        <Item>Observational data</Item>
        <Item>Physical measurements</Item>
        <Item>Physiological measurements</Item>
        <Item>Qualitative data</Item>
        <Item>Questionnaire data</Item>
        <Item>Survey data</Item>
        <Item>Usage tracking data</Item>
        <Item>Other</Item>
    </xsl:variable>

    <!-- list for otheridagency field -->
    <xsl:variable name="reg_agency" as="element()*">
        <Item>ClinicalTrials.gov</Item>
        <Item>EU register</Item>
        <Item>ISRCTN</Item>
        <Item>Other</Item>
    </xsl:variable>

    <!-- list for pubidtype1 field -->
    <xsl:variable name="pub_type" as="element()*">
        <Item>DOI</Item>
        <Item>arXiv</Item>
    </xsl:variable>

    <!-- list for unitofanalysis field -->
    <xsl:variable name="unit_anly" as="element()*">
        <Item>Individuals</Item>
        <Item>Maternal/infant child dyad</Item>
        <Item>Parent/child dyad</Item>
        <Item>Families/households </Item>
        <Item>Institutions/organizations</Item>
        <Item>Literature</Item>
        <Item>Other</Item>
    </xsl:variable>

    <xsl:template match="/">
        <xsl:param name="index" select="4"/>
        <xsl:choose>
            <xsl:when test="unparsed-text-available($doc)">
                <xsl:variable name="tsv" select="unparsed-text($doc)"/>
                <xsl:variable name="lines" select="tokenize($tsv, '&#xa;')" as="xs:string+"/>
                <xsl:variable name="cell"
                    select="tokenize(translate($lines[1], '?)''(,/=:;', ''), '&#x9;')"
                    as="xs:string+"/>

                <xsl:element name="root">
                    <xsl:for-each select="$lines[position() &gt; 1]">
                        <xsl:element name="codeBook">
                            <!-- 1.0 Document Description -->
                            <xsl:element name="docDscr">
                                <!-- 1.1 Bibliographic Citation -->
                                <xsl:element name="citation">
                                    <xsl:variable name="lineItems" select="fn:rows(.)"
                                        as="xs:string+"/>
                                    <xsl:for-each select="$cell">
                                        <xsl:variable name="pos" select="position()"/>
                                        <xsl:variable name="cellValue">
                                            <xsl:value-of select="$cell[$pos]"/>
                                        </xsl:variable>
                                        <xsl:if test="$lineItems[$pos] != ''">
                                            <xsl:choose>
                                                <xsl:when test="$cellValue = 'title'">
                                                  <!-- 1.1.1 Title Statement -->
                                                  <xsl:element name="titlStmt">
                                                  <!-- 1.1.1.1 Title -->
                                                  <xsl:element name="titl">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  <xsl:if test="$lineItems[$pos + 1] != ''">
                                                  <!-- 1.1.1.3 Alternative Title -->
                                                  <xsl:element name="altTitl">
                                                  <xsl:value-of select="$lineItems[$pos + 1]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:element>
                                                </xsl:when>
                                            </xsl:choose>
                                        </xsl:if>
                                    </xsl:for-each>
                                </xsl:element>
                            </xsl:element>
                            <!-- 2.0 Study Description -->
                            <xsl:element name="stdyDscr">
                                <!-- 2.1 Bibliographic Citation -->
                                <xsl:element name="citation">
                                    <!-- 2.1.1 Title Statement -->
                                    <xsl:element name="titlStmt">
                                        <xsl:variable name="lineItems" select="fn:rows(.)"
                                            as="xs:string+"/>
                                        <xsl:for-each select="$cell">
                                            <xsl:variable name="pos" select="position()"/>
                                            <xsl:variable name="cellValue">
                                                <xsl:value-of select="$cell[$pos]"/>
                                            </xsl:variable>
                                            <xsl:if test="$lineItems[$pos] != ''">
                                                <xsl:choose>
                                                    <!-- 2.1.1.1 Title -->
                                                  <xsl:when test="$cellValue = 'title'">
                                                  <xsl:element name="titl">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  <xsl:if test="$lineItems[$pos + 1] != ''">
                                                      <!-- 2.1.1.3 Alternative Title -->
                                                  <xsl:element name="altTitl">
                                                  <xsl:value-of select="$lineItems[$pos + 1]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:when>
                                                    <!-- 2.1.1.5 Identification Number -->
                                                  <xsl:when test="$cellValue = 'otheridagency'">
                                                  <xsl:if test="$lineItems[$pos] != ''">
                                                  <xsl:variable name="count">
                                                  <xsl:value-of
                                                  select="number($lineItems[$pos - 1]) - 1"/>
                                                  </xsl:variable>
                                                  <xsl:for-each select="0 to $count">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="2 * ."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != ''">
                                                  <xsl:element name="IDNo">
                                                  <xsl:attribute name="agency">
                                                  <xsl:value-of select="$reg_agency[$altpos + 1]"/>
                                                  </xsl:attribute>
                                                  <xsl:value-of
                                                  select="$lineItems[$pos + $altpos + 1]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  </xsl:if>
                                                  </xsl:when>
                                                </xsl:choose>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:element>
                                    <!-- 2.1.2 Responsibility Statement -->
                                    <xsl:element name="rspStmt">
                                        <xsl:variable name="lineItems" select="fn:rows(.)"
                                            as="xs:string+"/>
                                        <xsl:for-each select="$cell">
                                            <xsl:variable name="pos" select="position()"/>
                                            <xsl:variable name="cellValue">
                                                <xsl:value-of select="$cell[$pos]"/>
                                            </xsl:variable>
                                            <xsl:if test="$lineItems[$pos] != ''">
                                                <xsl:choose>
                                                    <!-- 2.1.2.1 Authoring Entity/Primary Investigator -->
                                                  <xsl:when test="$cellValue = 'authorname1'">
                                                  <xsl:variable name="count">
                                                  <xsl:value-of
                                                  select="number($lineItems[$pos - 1]) - 1"/>
                                                  </xsl:variable>
                                                  <xsl:for-each select="0 to $count">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="4 * ."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != ''">
                                                  <xsl:element name="AuthEnty">
                                                  <xsl:attribute name="affiliation">
                                                  <xsl:value-of
                                                  select="$lineItems[$pos + $altpos + 1]"/>
                                                  </xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos + $altpos]"
                                                  />
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  </xsl:when>
                                                </xsl:choose>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:element>
                                    <!-- 2.1.3 Production Statement -->
                                    <xsl:element name="prodStmt">
                                        <xsl:variable name="lineItems" select="fn:rows(.)"
                                            as="xs:string+"/>
                                        <xsl:for-each select="$cell">
                                            <xsl:variable name="pos" select="position()"/>
                                            <xsl:variable name="cellValue">
                                                <xsl:value-of select="$cell[$pos]"/>
                                            </xsl:variable>
                                            <xsl:if test="$lineItems[$pos] != ''">
                                                <xsl:choose>
                                                    <!-- 2.1.3.1 Producer -->
                                                  <xsl:when test="$cellValue = 'producer1'">
                                                  <xsl:variable name="count">
                                                  <xsl:value-of
                                                  select="number($lineItems[$pos - 1]) - 1"/>
                                                  </xsl:variable>
                                                  <xsl:for-each select="0 to $count">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="3 * ."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != ''">
                                                  <xsl:element name="producer">
                                                  <xsl:attribute name="affiliation">
                                                  <xsl:value-of
                                                  select="$lineItems[$pos + $altpos + 1]"/>
                                                  </xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos + $altpos]"/>
                                                  <xsl:if
                                                  test="$lineItems[$pos + $altpos + 2] != ''">
                                                  <xsl:element name="ExtLink">
                                                  <xsl:attribute name="URI">
                                                  <xsl:value-of
                                                  select="$lineItems[$pos + $altpos + 2]"/>
                                                  </xsl:attribute>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  </xsl:when>
                                                    <!-- 2.1.3.3 Date of Production / 2.1.3.4 Place of Production / 2.1.3.7 Grant Number -->
                                                  <xsl:when test="$cellValue = 'productiondate'">
                                                  <xsl:if test="$lineItems[$pos] != ''">
                                                  <xsl:element name="prodDate">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  <xsl:if test="$lineItems[$pos + 1] != ''">
                                                  <xsl:element name="prodPlac">
                                                  <xsl:value-of select="$lineItems[$pos + 1]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if test="$lineItems[$pos + 2] != ''">
                                                  <xsl:element name="grantNo">
                                                  <xsl:attribute name="agency">
                                                  <xsl:value-of select="$lineItems[$pos + 2]"/>
                                                  </xsl:attribute>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:if>
                                                  </xsl:when>
                                                    <!-- 2.1.3.5 Software -->
                                                  <xsl:when test="$cellValue = 'softwarename1'">
                                                  <xsl:variable name="count">
                                                  <xsl:value-of
                                                  select="number($lineItems[$pos - 1]) - 1"/>
                                                  </xsl:variable>
                                                  <xsl:for-each select="0 to $count">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="2 * ."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != ''">
                                                  <xsl:element name="software">
                                                  <xsl:if
                                                  test="$lineItems[$pos + $altpos + 1] != ''">
                                                  <xsl:attribute name="version">
                                                  <xsl:value-of
                                                  select="$lineItems[$pos + $altpos + 1]"/>
                                                  </xsl:attribute>
                                                  </xsl:if>
                                                  <xsl:value-of select="$lineItems[$pos + $altpos]"
                                                  />
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  </xsl:when>
                                                </xsl:choose>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:element>
                                    <!-- 2.1.4 Distributor Statement -->
                                    <xsl:element name="distStmt">
                                        <xsl:variable name="lineItems" select="fn:rows(.)"
                                            as="xs:string+"/>
                                        <xsl:for-each select="$cell">
                                            <xsl:variable name="pos" select="position()"/>
                                            <xsl:variable name="cellValue">
                                                <xsl:value-of select="$cell[$pos]"/>
                                            </xsl:variable>
                                            <xsl:if test="$lineItems[$pos] != ''">
                                                <xsl:choose>
                                                    <!-- 2.1.4.2 Contact Persons -->
                                                  <xsl:when test="$cellValue = 'contactname'">
                                                  <xsl:element name="contact">
                                                  <xsl:attribute name="affiliation">
                                                  <xsl:value-of select="$lineItems[$pos + 1]"/>
                                                  </xsl:attribute>
                                                  <xsl:attribute name="email">
                                                  <xsl:value-of select="$lineItems[$pos + 2]"/>
                                                  </xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:when>
                                                    <!-- 2.1.4.1 Distributor -->
                                                  <xsl:when test="$cellValue = 'distributor'">
                                                      <xsl:if test="$lineItems[$pos] != '0'">
                                                  <xsl:element name="distrbtr">
                                                      <xsl:if test="$lineItems[$pos + 3] != ''">
                                                  <xsl:attribute name="abbr">
                                                  <xsl:value-of select="$lineItems[$pos + 3]"/>
                                                  </xsl:attribute>
                                                      </xsl:if>
                                                      <xsl:if test="$lineItems[$pos + 2] != ''">
                                                  <xsl:attribute name="affiliation">
                                                  <xsl:value-of select="$lineItems[$pos + 2]"/>
                                                  </xsl:attribute>
                                                      </xsl:if>
                                                  <xsl:value-of select="$lineItems[$pos + 1]"/>
                                                  <xsl:if test="$lineItems[$pos + 4] != ''">
                                                  <xsl:element name="ExtLink">
                                                  <xsl:attribute name="URI">
                                                  <xsl:value-of select="$lineItems[$pos + 4]"/>
                                                  </xsl:attribute>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:element>
                                                      </xsl:if>
                                                  </xsl:when>
                                                </xsl:choose>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:element>
                                    <!-- 2.1.5 Series Statement -->
                                    <xsl:element name="serStmt">
                                        <xsl:variable name="lineItems" select="fn:rows(.)"
                                            as="xs:string+"/>
                                        <xsl:for-each select="$cell">
                                            <xsl:variable name="pos" select="position()"/>
                                            <xsl:variable name="cellValue">
                                                <xsl:value-of select="$cell[$pos]"/>
                                            </xsl:variable>
                                            <xsl:if test="$lineItems[$pos] != ''">
                                                <xsl:choose>
                                                    <!-- 2.1.5.1 Series Name -->
                                                  <xsl:when test="$cellValue = 'seriesname'">
                                                  <xsl:element name="serName">
                                                  <xsl:value-of select="$lineItems[$pos + 9]"/>
                                                  </xsl:element>
                                                  </xsl:when>
                                                    <!-- 2.1.5.2 Series Information -->
                                                  <xsl:when test="$cellValue = 'seriesinformation'">
                                                  <xsl:element name="serInfo">
                                                  <xsl:value-of select="$lineItems[$pos + 9]"/>
                                                  </xsl:element>
                                                  </xsl:when>
                                                </xsl:choose>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:element>

                                    <!-- <xsl:element name="{replace(normalize-space($cell[$pos]), ' ' , '_')}" >
                                    <xsl:value-of select="$lineItems[$pos]"/>
                                </xsl:element> -->
                                    
                                </xsl:element>
                                <!-- 2.4 Data Access -->
                                <xsl:element name="dataAccs">
                                    <xsl:variable name="lineItems" select="fn:rows(.)"
                                        as="xs:string+"/>
                                    <xsl:for-each select="$cell">
                                        <xsl:variable name="pos" select="position()"/>
                                        <xsl:variable name="cellValue">
                                            <xsl:value-of select="$cell[$pos]"/>
                                        </xsl:variable>
                                        <xsl:if test="$lineItems[$pos] != ''">
                                            <xsl:choose>
                                                <xsl:when test="$cellValue = 'who_access___1'">
                                                  <xsl:element name="useStmt">
                                                  <xsl:for-each select="0 to 7">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != '0'">
                                                  <xsl:element name="conditions">
                                                  <xsl:value-of
                                                  select="$access_condition[$altpos + 1]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if
                                                  test="$lineItems[$pos + $altpos + 10] != '0'">
                                                  <xsl:element name="restrctn">
                                                  <xsl:value-of select="$restrictions[$altpos + 1]"
                                                  />
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  <xsl:if test="$lineItems[$pos + 8] != '0'">
                                                  <xsl:element name="conditions">
                                                  <xsl:value-of select="$lineItems[$pos + 9]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if test="$lineItems[$pos + 18] != '0'">
                                                  <xsl:element name="restrctn">
                                                  <xsl:value-of select="$lineItems[$pos + 19]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if test="$lineItems[$pos + 20] != ''">
                                                  <xsl:element name="conditions">
                                                  <xsl:value-of select="$lineItems[$pos + 20]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:element>
                                                </xsl:when>
                                                <xsl:when test="$cellValue = 'accsplav'">
                                                  <xsl:if
                                                  test="$lineItems[$pos] or $lineItems[$pos + 1] != ''">
                                                  <xsl:element name="setAvail">
                                                  <xsl:if test="$lineItems[$pos] != ''">
                                                  <xsl:element name="accsPlac">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if test="$lineItems[$pos + 1] != ''">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="$lineItems[$pos + 1]"/>
                                                  </xsl:variable>
                                                  <xsl:element name="avlStatus">
                                                  <xsl:value-of select="$avlStatus[$altpos + 0]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:element>
                                                  </xsl:if>
                                                </xsl:when>
                                            </xsl:choose>
                                        </xsl:if>
                                    </xsl:for-each>
                                </xsl:element>
                                <!-- 2.2 Study Scope -->
                                <xsl:element name="stdyInfo">
                                    <xsl:variable name="lineItems" select="fn:rows(.)"
                                        as="xs:string+"/>
                                    <xsl:for-each select="$cell">
                                        <xsl:variable name="pos" select="position()"/>
                                        <xsl:variable name="cellValue">
                                            <xsl:value-of select="$cell[$pos]"/>
                                        </xsl:variable>
                                        <xsl:if test="$lineItems[$pos] != ''">
                                            <xsl:choose>
                                                <!-- 2.2.2 Abstract -->
                                                <xsl:when test="$cellValue = 'studydesc'">
                                                  <xsl:element name="abstract">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                </xsl:when>
                                                <!-- 2.2.1.1 Keywords -->
                                                <xsl:when test="$cellValue = 'keyword1'">
                                                  <xsl:element name="subject">
                                                  <xsl:variable name="count">
                                                  <xsl:value-of
                                                  select="number($lineItems[$pos - 1]) - 1"/>
                                                  </xsl:variable>
                                                  <xsl:for-each select="0 to $count">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="4 * ."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != ''">
                                                  <xsl:element name="keyword">
                                                  <xsl:if
                                                  test="$lineItems[$pos + $altpos + 1] = '1'">
                                                  <xsl:attribute name="vocab">
                                                  <xsl:value-of
                                                  select="$lineItems[$pos + $altpos + 2]"/>
                                                  </xsl:attribute>
                                                  </xsl:if>
                                                  <xsl:value-of select="$lineItems[$pos + $altpos]"
                                                  />
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  </xsl:element>
                                                </xsl:when>
                                            </xsl:choose>
                                        </xsl:if>
                                    </xsl:for-each>
                                    <!-- 2.2.3 Summary Data Description -->
                                    <xsl:element name="sumDscr">
                                        <xsl:for-each select="$cell">
                                            <xsl:variable name="pos" select="position()"/>
                                            <xsl:variable name="cellValue">
                                                <xsl:value-of select="$cell[$pos]"/>
                                            </xsl:variable>
                                            <xsl:if test="$lineItems[$pos] != ''">
                                                <xsl:choose>
                                                  <xsl:when
                                                  test="$cellValue = 'timeperiodcoveredstart'">
                                                      <!-- 2.2.3.1 Time Period Covered -->
                                                  <xsl:if test="$lineItems[$pos] != ''">
                                                  <xsl:element name="timePrd">
                                                  <xsl:attribute name="event">start</xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if test="$lineItems[$pos + 1] != ''">
                                                  <xsl:element name="timePrd">
                                                  <xsl:attribute name="event">end</xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos + 1]"/>
                                                  </xsl:element>
                                                      <!-- 2.2.3.2 Date of Collection -->
                                                  </xsl:if>
                                                  <xsl:if test="$lineItems[$pos + 2] != ''">
                                                  <xsl:element name="collDate">
                                                  <xsl:attribute name="event">start</xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos + 2]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if test="$lineItems[$pos + 3] != ''">
                                                  <xsl:element name="collDate">
                                                  <xsl:attribute name="event">end</xsl:attribute>
                                                  <xsl:value-of select="$lineItems[$pos + 3]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:when>
                                                    <!-- 2.2.3.3 Country / 2.2.3.4 Geographic Coverage -->
                                                  <xsl:when test="$cellValue = 'country'">
                                                  <xsl:if test="$lineItems[$pos] != ''">
                                                  <xsl:variable name="count">
                                                  <xsl:value-of
                                                  select="number($lineItems[$pos - 1]) - 1"/>
                                                  </xsl:variable>
                                                  <xsl:for-each select="0 to $count">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="4 * ."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != ''">
                                                  <xsl:element name="nation">
                                                  <xsl:if test="$lineItems[$pos + $altpos] != ''">
                                                  <xsl:value-of select="$lineItems[$pos + $altpos]"
                                                  />
                                                  </xsl:if>
                                                  </xsl:element>
                                                  <xsl:if
                                                  test="$lineItems[$pos + $altpos + 1] != ''">
                                                  <xsl:element name="geogCover">
                                                  <xsl:value-of
                                                  select="concat($lineItems[$pos + $altpos + 1], ',', ' ', $lineItems[$pos + $altpos + 2], ',', ' ', $lineItems[$pos + $altpos + 3])"
                                                  />
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  </xsl:if>
                                                  </xsl:when>
                                                    <!-- 2.2.3.9 Universe -->
                                                  <xsl:when test="$cellValue = 'universe'">
                                                  <xsl:if test="$lineItems[$pos] != ''">
                                                  <xsl:element name="universe">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:when>
                                                    <!-- 2.2.3.10 Kind of Data -->
                                                  <xsl:when test="$cellValue = 'kindofdata___1'">
                                                  <xsl:for-each select="0 to 15">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != '0'">
                                                  <xsl:element name="dataKind">
                                                  <xsl:value-of select="$data_kind[$altpos + 1]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  <xsl:if test="$lineItems[$pos + 16] != '0'">
                                                  <xsl:element name="datakind">
                                                  <xsl:value-of select="$lineItems[$pos + 17]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:when>
                                                    <!-- 2.2.3.8 Unit of Analysis -->
                                                  <xsl:when test="$cellValue = 'unitofanalysis___1'">
                                                  <xsl:for-each select="0 to 5">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != '0'">
                                                  <xsl:element name="anlyUnit">
                                                  <xsl:value-of select="$unit_anly[$altpos + 1]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  <xsl:if test="$lineItems[$pos + 6] != '0'">
                                                  <xsl:element name="anlyUnit">
                                                  <xsl:value-of select="$lineItems[$pos + 7]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:when>
                                                </xsl:choose>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:element>
                                </xsl:element>
                                <!-- 2.3 Methodology and Processing -->
                                <xsl:element name="method">
                                    <!-- 2.3.1 Data Collection Methdology -->
                                    <xsl:element name="dataColl">
                                        <xsl:variable name="lineItems" select="fn:rows(.)"
                                            as="xs:string+"/>
                                        <xsl:for-each select="$cell">
                                            <xsl:variable name="pos" select="position()"/>
                                            <xsl:variable name="cellValue">
                                                <xsl:value-of select="$cell[$pos]"/>
                                            </xsl:variable>
                                            <xsl:if test="$lineItems[$pos] != ''">
                                                <xsl:choose>
                                                    <!-- 2.3.1.3 frequenc -->
                                                    <xsl:when test="$cellValue = 'freqdata'">
                                                        <xsl:element name="frequenc">
                                                            <xsl:value-of select="$lineItems[$pos]"/>
                                                        </xsl:element>
                                                    </xsl:when>
                                                    <!-- 2.3.1.4 Sampling Procedure -->
                                                  <xsl:when test="$cellValue = 'samplingprocedure'">
                                                  <xsl:element name="sampProc">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:when>
                                                    <!-- 2.3.1.6 Mode of Data Collection -->
                                                  <xsl:when test="$cellValue = 'collectionmode___1'">
                                                  <xsl:for-each select="0 to 17">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != '0'">
                                                  <xsl:element name="collMode">
                                                  <xsl:value-of
                                                  select="$collection_mode[$altpos + 1]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                  <xsl:if test="$lineItems[$pos + 18] != '0'">
                                                  <xsl:element name="collMode">
                                                  <xsl:value-of select="$lineItems[$pos + 19]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:when>
                                                    <!-- 2.3.1.8 Sources Statement / 2.3.1.8.1 Data Sources -->
                                                  <xsl:when test="$cellValue = 'datasources'">
                                                  <xsl:element name="source">
                                                  <xsl:element name="dataSrc">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:element>
                                                  </xsl:when>
                                                    <!-- 2.3.1.9 Characteristics of Data Collection Situation -->
                                                  <xsl:when
                                                  test="$cellValue = 'datacollectionsituation'">
                                                  <xsl:element name="collSitu">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:when>
                                                    <!-- 2.3.1.10 Actions to Minimize Losses -->
                                                  <xsl:when
                                                  test="$cellValue = 'actionstominimizeloss'">
                                                  <xsl:element name="actMin">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:when>
                                                    <!-- 2.3.1.11 Control Operations -->
                                                  <xsl:when test="$cellValue = 'controloperations'">
                                                  <xsl:element name="ConOps">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:when>
                                                    <!-- 2.3.1.13 Cleaning Operations -->
                                                  <xsl:when test="$cellValue = 'cleaningoperations'">
                                                  <xsl:element name="cleanOps">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:when>
                                                </xsl:choose>
                                            </xsl:if>
                                        </xsl:for-each>
                                    </xsl:element>
                                </xsl:element>
                                <!-- 2.5 Other Study Description Materials -->
                                <xsl:element name="othrStdyMat">
                                    <xsl:variable name="lineItems" select="fn:rows(.)"
                                        as="xs:string+"/>
                                    <xsl:for-each select="$cell">
                                        <xsl:variable name="pos" select="position()"/>
                                        <xsl:variable name="cellValue">
                                            <xsl:value-of select="$cell[$pos]"/>
                                        </xsl:variable>
                                        <xsl:if test="$lineItems[$pos] != ''">
                                            <xsl:choose>
                                                <!-- 2.5.3 Related Publications -->
                                                <xsl:when test="$cellValue = 'publication1'">
                                                  <xsl:variable name="count">
                                                  <xsl:value-of
                                                  select="number($lineItems[$pos - 1]) - 1"/>
                                                  </xsl:variable>
                                                  <xsl:for-each select="0 to $count">
                                                  <xsl:variable name="altpos">
                                                  <xsl:value-of select="4 * ."/>
                                                  </xsl:variable>
                                                  <xsl:if test="$lineItems[$pos + $altpos] != ''">
                                                  <xsl:element name="relPubl">
                                                  <xsl:value-of select="$lineItems[$pos + $altpos]"
                                                  />
                                                  </xsl:element>
                                                  <xsl:if
                                                  test="$lineItems[$pos + $altpos + 1] != ''">
                                                  <xsl:variable name="pub">
                                                  <xsl:value-of
                                                  select="number($lineItems[$pos + $altpos + 1])"/>
                                                  </xsl:variable>
                                                  <xsl:element name="relPubl">
                                                  <xsl:value-of select="$pub_type[$pub + 0]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if
                                                  test="$lineItems[$pos + $altpos + 2] != ''">
                                                  <xsl:element name="relPubl">
                                                  <xsl:value-of
                                                  select="$lineItems[$pos + $altpos + 2]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  <xsl:if
                                                  test="$lineItems[$pos + $altpos + 3] != ''">
                                                  <xsl:element name="relPubl">
                                                  <xsl:value-of
                                                  select="$lineItems[$pos + $altpos + 3]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                  </xsl:if>
                                                  </xsl:for-each>
                                                </xsl:when>
                                                <!-- 2.5.2 Related Studies -->
                                                <xsl:when test="$cellValue = 'relateddatasets'">
                                                  <xsl:if test="$lineItems[$pos] != ''">
                                                  <xsl:element name="relStdy">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                </xsl:when>
                                                <!-- 2.5.4 Other References Notes -->
                                                <xsl:when test="$cellValue = 'otherreferences'">
                                                  <xsl:if test="$lineItems[$pos] != ''">
                                                  <xsl:element name="othRefs">
                                                  <xsl:value-of select="$lineItems[$pos]"/>
                                                  </xsl:element>
                                                  </xsl:if>
                                                </xsl:when>
                                            </xsl:choose>
                                        </xsl:if>
                                    </xsl:for-each>
                                </xsl:element>
                            </xsl:element>
                        </xsl:element>
                    </xsl:for-each>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>Cannot locate : </xsl:text>
                <xsl:value-of select="$doc"/>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>

</xsl:stylesheet>
