<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
    xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs dc" version="2.0">
    <xsl:template name="lang650">
        <xsl:param name="lang"/>
        <xsl:choose>
            <xsl:when test="$lang = 'als'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Tosk Albanian -->
                <!-- marc: Albanian -->
                <xsl:call-template name="langAlb"/>
            </xsl:when>
            <xsl:when test="$lang = 'sqi'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Albanian -->
                <!-- marc: Albanian -->
                <xsl:call-template name="langAlb"/>
            </xsl:when>
            <xsl:when test="$lang = 'amh'">
                <!-- code match -->
                <!-- iso 639-3: Amharic -->
                <!-- marc: Amharic -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Amharic language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'abv'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Baharna Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'acm'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Mesopotamian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'afb'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Gulf Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'apc'">
                <!-- best fit based on label -->
                <!-- iso 639-3: North Levantine Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'ara'">
                <!-- code match -->
                <!-- iso 639-3: Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'arb'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Standard Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'ary'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Moroccan Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'arz'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Egyptian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'ayp'">
                <!-- best fit based on label -->
                <!-- iso 639-3: North Mesopotamian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="langAra"/>
            </xsl:when>
            <xsl:when test="$lang = 'asm'">
                <!-- code match -->
                <!-- iso 639-3: Assamese -->
                <!-- marc: Assamese -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Assamese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'bam'">
                <!-- code match -->
                <!-- iso 639-3: Bambara -->
                <!-- marc: Bambara -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bambara language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'jgo'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Ngomba -->
                <!-- marc: Bamileke languages -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bamileke languages</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'eus'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Basque -->
                <!-- marc: Basque -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Basque language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ben'">
                <!-- code match -->
                <!-- iso 639-3: Bengali -->
                <!-- marc: Bengali -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bengali language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'bos'">
                <!-- code match -->
                <!-- iso 639-3: Bosnian -->
                <!-- marc: Bosnian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bosnian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'bul'">
                <!-- code match -->
                <!-- iso 639-3: Bulgarian -->
                <!-- marc: Bulgarian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Bulgarian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'yue'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- iso 639-3: Yue Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Cantonese dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'cat'">
                <!-- code match -->
                <!-- iso 639-3: Catalan -->
                <!-- marc: Catalan -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Catalan language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ceb'">
                <!-- code match -->
                <!-- iso 639-3: Cebuano -->
                <!-- marc: Cebuano -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Cebuano language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'lzh'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Literary Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="langChi"/>
            </xsl:when>
            <xsl:when test="$lang = 'zho'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="langChi"/>
            </xsl:when>
            <xsl:when test="$lang = 'hat'">
                <!-- code match, though labels differ -->
                <!-- iso 639-3: Haitian -->
                <!-- marc: Haitian French Creole -->
                <xsl:call-template name="langHat"/>
            </xsl:when>
            <xsl:when test="$lang = 'hrv'">
                <!-- code match -->
                <!-- iso 639-3: Croatian -->
                <!-- marc: Croatian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Croatian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ces'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Czech -->
                <!-- marc: Czech -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Czech language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'dan'">
                <!-- code match -->
                <!-- iso 639-3: Danish -->
                <!-- marc: Danish -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Danish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'prs'">
                <!-- match based on label, marc assigned collective code -->
                <!-- iso 639-3: Dari -->
                <!-- marc: Dari -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Dari language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'kmj'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- iso 639-3: Kumarbhag Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="langDra"/>
            </xsl:when>
            <xsl:when test="$lang = 'mjt'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- iso 639-3: Sauria Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="langDra"/>
            </xsl:when>
            <xsl:when test="$lang = 'mkb'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- iso 639-3: Mal Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="langDra"/>
            </xsl:when>
            <xsl:when test="$lang = 'nld'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Dutch -->
                <!-- marc: Dutch -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Dutch language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'eng'">
                <!-- code match -->
                <!-- iso 639-3: English -->
                <!-- marc: English -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">English language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'est'">
                <!-- code match -->
                <!-- iso 639-3: Estonian -->
                <!-- marc: Estonian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Estonian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'fra'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: French -->
                <!-- marc: French -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">French language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'kat'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Georgian -->
                <!-- marc: Georgian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Georgian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'deu'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: German -->
                <!-- marc: German -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">German language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ell'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Modern Greek (1453-) -->
                <!-- marc: Greek, Modern (1453-) -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Greek language, Modern</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'hau'">
                <!-- code match -->
                <!-- iso 639-3: Hausa -->
                <!-- marc: Hausa -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Hausa language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'hin'">
                <!-- code match -->
                <!-- iso 639-3: Hindi -->
                <!-- marc: Hindi -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Hindi language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'hun'">
                <!-- code match -->
                <!-- iso 639-3: Hungarian -->
                <!-- marc: Hungarian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Hungarian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ind'">
                <!-- code match -->
                <!-- iso 639-3: Indonesian -->
                <!-- marc: Indonesian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Indonesian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ita'">
                <!-- code match -->
                <!-- iso 639-3: Italian -->
                <!-- marc: Italian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Italian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'jpn'">
                <!-- code match -->
                <!-- iso 639-3: Japanese -->
                <!-- marc: Japanese -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Japanese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'khm'">
                <!-- code match, though labels differ -->
                <!-- iso 639-3: Central Khmer -->
                <!-- marc: Khmer -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Khmer language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'kor'">
                <!-- code match -->
                <!-- iso 639-3: Korean -->
                <!-- marc: Korean -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Korean language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'kmr'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Northern Kurdish -->
                <!-- marc: Kurdish -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Kurdish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'pnb'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- iso 639-3: Western Panjabi -->
                <!-- marc: Lahndā -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Lahndā language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'lao'">
                <!-- code match -->
                <!-- iso 639-3: Lao -->
                <!-- marc: Lao -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Lao language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'lat'">
                <!-- code match -->
                <!-- iso 639-3: Latin -->
                <!-- marc: Latin -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Latin language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'lit'">
                <!-- code match -->
                <!-- iso 639-3: Lithuanian -->
                <!-- marc: Lithuanian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Lithuanian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'zsm'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Standard Malay -->
                <!-- marc: Malay -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Malay language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'cmn'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- iso 639-3: Mandarin Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Mandarin dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'emk'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- iso 639-3: Eastern Maninkakan -->
                <!-- marc: Mandingo -->
                <xsl:call-template name="langMan"/>
            </xsl:when>
            <xsl:when test="$lang = 'mxx'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Mahou -->
                <!-- marc: Mandingo -->
                <xsl:call-template name="langMan"/>
            </xsl:when>
            <xsl:when test="$lang = 'kxm'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Northern Khmer -->
                <!-- marc: Northern Khmer -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Northern Khmer language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'nob'">
                <!-- code match -->
                <!-- iso 639-3: Norwegian Bokmål -->
                <!-- marc: Norwegian (Bokmål) -->
                <xsl:call-template name="langNor"/>
            </xsl:when>
            <xsl:when test="$lang = 'nor'">
                <!-- code match -->
                <!-- iso 639-3: Norwegian -->
                <!-- marc: Norwegian -->
                <xsl:call-template name="langNor"/>
            </xsl:when>
            <xsl:when test="$lang = 'nno'">
                <!-- code match -->
                <!-- iso 639-3: Norwegian Nynorsk -->
                <!-- marc: Norwegian (Nynorsk) -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Norwegian language (Nynorsk)</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'pan'">
                <!-- code match -->
                <!-- iso 639-3: Panjabi -->
                <!-- marc: Panjabi -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Panjabi language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'fas'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Persian -->
                <!-- marc: Persian -->
                <xsl:call-template name="langPer"/>
            </xsl:when>
            <xsl:when test="$lang = 'pes'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Iranian Persian -->
                <!-- marc: Persian -->
                <xsl:call-template name="langPer"/>
            </xsl:when>
            <xsl:when test="$lang = 'pol'">
                <!-- code match -->
                <!-- iso 639-3: Polish -->
                <!-- marc: Polish -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Polish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'por'">
                <!-- code match -->
                <!-- iso 639-3: Portuguese -->
                <!-- marc: Portuguese -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Portuguese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'pus'">
                <!-- code match -->
                <!-- iso 639-3: Pushto -->
                <!-- marc: Pushto -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Pushto language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ron'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Romanian -->
                <!-- marc: Romanian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Romanian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'rus'">
                <!-- code match -->
                <!-- iso 639-3: Russian -->
                <!-- marc: Russian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Russian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'san'">
                <!-- code match -->
                <!-- iso 639-3: Sanskrit -->
                <!-- marc: Sanskrit -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Sanskrit language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'gla'">
                <!-- code match -->
                <!-- iso 639-3: Scottish Gaelic -->
                <!-- marc: Scottish Gaelic -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Scottish Gaelic language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'gul'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Sea Island Creole English -->
                <!-- marc: Sea Islands Creole -->
                <xsl:call-template name="langCpe"/>
            </xsl:when>
            <xsl:when test="$lang = 'trf'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Trinidadian Creole English -->
                <!-- marc: Sea Islands Creole -->
                <xsl:call-template name="langCpe"/>
            </xsl:when>
            <xsl:when test="$lang = 'srp'">
                <!-- code match -->
                <!-- iso 639-3: Serbian -->
                <!-- marc: Serbian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Serbian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'slk'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Slovak -->
                <!-- marc: Slovak -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Slovak language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'slv'">
                <!-- code match -->
                <!-- iso 639-3: Slovenian -->
                <!-- marc: Slovenian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Slovenian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'som'">
                <!-- code match -->
                <!-- iso 639-3: Somali -->
                <!-- marc: Somali -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Somali language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ajp'">
                <!-- best fit based on label, marc assigned collective code -->
                <!-- iso 639-3: South Levantine Arabic -->
                <!-- marc: South Arabic -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">South Arabic language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'nan'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Min Nan Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Southern Min dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'spa'">
                <!-- code match -->
                <!-- iso 639-3: Spanish -->
                <!-- marc: Spanish -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Spanish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'swa'">
                <!-- code match -->
                <!-- iso 639-3: Swahili -->
                <!-- marc: Swahili -->
                <xsl:call-template name="langSwa"/>
            </xsl:when>
            <xsl:when test="$lang = 'swc'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Congo Swahili -->
                <!-- marc: Swahili -->
                <xsl:call-template name="langSwa"/>
            </xsl:when>
            <xsl:when test="$lang = 'swh'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Swahili (individual language) -->
                <!-- marc: Swahili -->
                <xsl:call-template name="langSwa"/>
            </xsl:when>
            <xsl:when test="$lang = 'swe'">
                <!-- code match -->
                <!-- iso 639-3: Swedish -->
                <!-- marc: Swedish -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Swedish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'tgl'">
                <!-- code match -->
                <!-- iso 639-3: Tagalog -->
                <!-- marc: Tagalog -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Tagalog language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'tam'">
                <!-- code match -->
                <!-- iso 639-3: Tamil -->
                <!-- marc: Tamil -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Tamil language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'tha'">
                <!-- code match -->
                <!-- iso 639-3: Thai -->
                <!-- marc: Thai -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Thai language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'tir'">
                <!-- code match -->
                <!-- iso 639-3: Tigrinya -->
                <!-- marc: Tigrinya -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Tigrinya language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'tpi'">
                <!-- code match -->
                <!-- iso 639-3: Tok Pisin -->
                <!-- marc: Tok Pisin -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Tok Pisin language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'tur'">
                <!-- code match -->
                <!-- iso 639-3: Turkish -->
                <!-- marc: Turkish -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Turkish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ukr'">
                <!-- code match -->
                <!-- iso 639-3: Ukrainian -->
                <!-- marc: Ukrainian -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Ukrainian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'urd'">
                <!-- code match -->
                <!-- iso 639-3: Urdu -->
                <!-- marc: Urdu -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Urdu language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'uzb'">
                <!-- code match -->
                <!-- iso 639-3: Uzbek -->
                <!-- marc: Uzbek -->
                <xsl:call-template name="langUzb"/>
            </xsl:when>
            <xsl:when test="$lang = 'uzn'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Northern Uzbek -->
                <!-- marc: Uzbek -->
                <xsl:call-template name="langUzb"/>
            </xsl:when>
            <xsl:when test="$lang = 'vie'">
                <!-- code match -->
                <!-- iso 639-3: Vietnamese -->
                <!-- marc: Vietnamese -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Vietnamese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'wuu'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Wu Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Wu dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'ybb'">
                <!-- match based on label, marc assigned collective code -->
                <!-- iso 639-3: Yemba -->
                <!-- marc: Yemba -->
                <xsl:call-template name="basic650">
                    <xsl:with-param name="langLcsh">Yemba language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang = 'luq'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Lucumi -->
                <!-- marc: Yoruba -->
                <xsl:call-template name="langYor"/>
            </xsl:when>
            <xsl:when test="$lang = 'yor'">
                <!-- code match -->
                <!-- iso 639-3: Yoruba -->
                <!-- marc: Yoruba -->
                <xsl:call-template name="langYor"/>
            </xsl:when>
            <xsl:when test="$lang = 'zul'">
                <!-- code match -->
                <!-- iso 639-3: Zulu -->
                <!-- marc: Zulu -->
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
