<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
    xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs dc" version="2.0">
    <xsl:template name="lang650">
        <xsl:param name="lang"/>
        <xsl:choose>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'als'">
                <xsl:call-template name="langAlb"/>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'sqi'">
                <xsl:call-template name="langAlb"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'amh'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Amharic language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'abv'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'acm'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'afb'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'apc'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'ara'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'arb'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'ary'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'arz'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'ayp'">
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'asm'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Assamese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'bam'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bambara language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'jgo'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bamileke languages</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'eus'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Basque language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'ben'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bengali language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'bos'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bosnian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'bul'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bulgarian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- marc preferred term ('use'), based on label match -->
            <xsl:when test="$lang = 'yue'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Cantonese dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'cat'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Catalan language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'ceb'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Cebuano language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'lzh'">
                <xsl:call-template name="langChi"/>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'zho'">
                <xsl:call-template name="langChi"/>
            </xsl:when>
            <!-- code match, though labels differ -->
            <xsl:when test="$lang = 'hat'">
                <xsl:call-template name="langHat"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'hrv'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Croatian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'ces'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Czech language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'dan'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Danish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- match based on label, marc assigned collective code -->
            <xsl:when test="$lang = 'prs'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Dari language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- marc assigned collective code for Malto (best fit based on label) -->
            <xsl:when test="$lang = 'kmj'">
                <xsl:call-template name="langDra"/>
            </xsl:when>
            <!-- marc assigned collective code for Malto (best fit based on label) -->
            <xsl:when test="$lang = 'mjt'">
                <xsl:call-template name="langDra"/>
            </xsl:when>
            <!-- marc assigned collective code for Malto (best fit based on label) -->
            <xsl:when test="$lang = 'mkb'">
                <xsl:call-template name="langDra"/>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'nld'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Dutch language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'eng'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">English language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'est'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Estonian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'fra'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">French language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'kat'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Georgian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'deu'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">German language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'ell'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Greek language, Modern</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'hau'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Hausa language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'hin'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Hindi language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'hun'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Hungarian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'ind'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Indonesian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'ita'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Italian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'jpn'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Japanese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match, though labels differ -->
            <xsl:when test="$lang = 'khm'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Khmer language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'kor'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Korean language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'kmr'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Kurdish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- marc preferred term ('use'), based on label match -->
            <xsl:when test="$lang = 'pnb'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Lahndā language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'lao'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Lao language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'lat'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Latin language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'lit'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Lithuanian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'zsm'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Malay language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- marc preferred term ('use'), based on label match -->
            <xsl:when test="$lang = 'cmn'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Mandarin dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- marc preferred term ('use'), based on label match -->
            <xsl:when test="$lang = 'emk'">
                <xsl:call-template name="langMan"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'mxx'">
                <xsl:call-template name="langMan"/>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'kxm'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Northern Khmer language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'nob'">
                <xsl:call-template name="langNor"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'nor'">
                <xsl:call-template name="langNor"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'nno'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Norwegian language (Nynorsk)</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'pan'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Panjabi language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'fas'">
                <xsl:call-template name="langPer"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'pes'">
                <xsl:call-template name="langPer"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'pol'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Polish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'por'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Portuguese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'pus'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Pushto language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'ron'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Romanian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'rus'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Russian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'san'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Sanskrit language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'gla'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Scottish Gaelic language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'gul'">
                <xsl:call-template name="langCpe"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'trf'">
                <xsl:call-template name="langCpe"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'srp'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Serbian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang = 'slk'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Slovak language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'slv'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Slovenian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'som'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Somali language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label, marc assigned collective code -->
            <xsl:when test="$lang = 'ajp'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">South Arabic language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'nan'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Southern Min dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'spa'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Spanish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'swa'">
                <xsl:call-template name="langSwa"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'swc'">
                <xsl:call-template name="langSwa"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'swh'">
                <xsl:call-template name="langSwa"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'swe'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Swedish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'tgl'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Tagalog language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'tam'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Tamil language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'tha'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Thai language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'tir'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Tigrinya language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'tpi'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Tok Pisin language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'tur'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Turkish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'ukr'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Ukrainian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'urd'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Urdu language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'uzb'">
                <xsl:call-template name="langUzb"/>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'uzn'">
                <xsl:call-template name="langUzb"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'vie'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Vietnamese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'wuu'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Wu dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- match based on label, marc assigned collective code -->
            <xsl:when test="$lang = 'ybb'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Yemba language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang = 'luq'">
                <xsl:call-template name="langYor"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'yor'">
                <xsl:call-template name="langYor"/>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang = 'zul'">
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Zulu language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'zxx'"/>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="basic650">
        <xsl:param name="langLcsh"/>
        <marc:datafield tag="650" ind1=" " ind2="0">
            <marc:subfield code="a">
                <xsl:value-of select="$langLcsh"/>
            </marc:subfield>
            <marc:subfield code="x">
                <xsl:text>Data processing</xsl:text>
            </marc:subfield>
            <marc:subfield code="v">
                <xsl:text>Databases.</xsl:text>
            </marc:subfield>
        </marc:datafield>
    </xsl:template>
    <xsl:template name="langAlb">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'als'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'sqi'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Albanian language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langAra">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'abv'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'acm'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'afb'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'apc'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'ara'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'arb'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'ary'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'arz'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'ayp'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Arabic language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langChi">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'lzh'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'zho'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Chinese language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langDra">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'kmj'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'mjt'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'mkb'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Dravidian languages</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langHat">
        <marc:datafield tag="650" ind1=" " ind2="0">
            <marc:subfield code="a">
                <xsl:text>Creole dialects, French</xsl:text>
            </marc:subfield>
            <marc:subfield code="z">
                <xsl:text>Haiti</xsl:text>
            </marc:subfield>
            <marc:subfield code="x">
                <xsl:text>Data processing</xsl:text>
            </marc:subfield>
            <marc:subfield code="v">
                <xsl:text>Databases.</xsl:text>
            </marc:subfield>
        </marc:datafield>
    </xsl:template>
    <xsl:template name="langMan">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'emk'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'mxx'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Mandingo language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langNor">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'nob'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'nor'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Norwegian language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langPer">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'fas'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'pes'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Persian language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langCpe">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'gul'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'trf'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Sea Islands Creole dialect</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langSwa">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'swa'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'swc'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'swh'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Swahili language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langUzb">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'uzb'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'uzn'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Uzbek language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="langYor">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'luq'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'yor'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Yoruba language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
