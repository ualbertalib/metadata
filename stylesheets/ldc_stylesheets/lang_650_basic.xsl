<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
    xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs dc" version="2.0">
    <xsl:template name="lang650basic">
        <!-- The mappings in this stylesheet are maintained in a table at https://docs.google.com/spreadsheets/d/1pJ7QJTH-6qaxAjAlQxVO9cMNgyAmCgUtK8LFAgy7jZ0/edit?usp=sharing -->
        <xsl:param name="langISO"/>
        <xsl:choose>
            <xsl:when test="$langISO = 'als'">
                <!-- match with macrolanguage, ISO 639-2/B synonym -->
                <!-- ISO 639-3: Tosk Albanian -->
                <!-- marc: Albanian -->
                <xsl:call-template name="lang650basicAlb"/>
            </xsl:when>
            <xsl:when test="$langISO = 'sqi'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Albanian -->
                <!-- marc: Albanian -->
                <xsl:call-template name="lang650basicAlb"/>
            </xsl:when>
            <xsl:when test="$langISO = 'amh'">
                <!-- code match -->
                <!-- ISO 639-3: Amharic -->
                <!-- marc: Amharic -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Amharic language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'abv'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Baharna Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'acm'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Mesopotamian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'afb'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Gulf Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'apc'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: North Levantine Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'ara'">
                <!-- code match -->
                <!-- ISO 639-3: Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'arb'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Standard Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'ary'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Moroccan Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'arz'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Egyptian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'ayp'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: North Mesopotamian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'asm'">
                <!-- code match -->
                <!-- ISO 639-3: Assamese -->
                <!-- marc: Assamese -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Assamese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'bam'">
                <!-- code match -->
                <!-- ISO 639-3: Bambara -->
                <!-- marc: Bambara -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Bambara language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'jgo'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Ngomba -->
                <!-- marc: Bamileke languages -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Bamileke languages</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'eus'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Basque -->
                <!-- marc: Basque -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Basque language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ben'">
                <!-- code match -->
                <!-- ISO 639-3: Bengali -->
                <!-- marc: Bengali -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Bengali language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'bos'">
                <!-- code match -->
                <!-- ISO 639-3: Bosnian -->
                <!-- marc: Bosnian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Bosnian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'bul'">
                <!-- code match -->
                <!-- ISO 639-3: Bulgarian -->
                <!-- marc: Bulgarian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Bulgarian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'yue'">
                <!-- match with macrolanguage; ISO 639-2/B synonym -->
                <!-- ISO 639-3: Yue Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Cantonese dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'cat'">
                <!-- code match -->
                <!-- ISO 639-3: Catalan -->
                <!-- marc: Catalan -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Catalan language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ceb'">
                <!-- code match -->
                <!-- ISO 639-3: Cebuano -->
                <!-- marc: Cebuano -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Cebuano language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'lzh'">
                <!-- match with macrolanguage; ISO 639-2/B synonym -->
                <!-- ISO 639-3: Literary Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang650basicChi"/>
            </xsl:when>
            <xsl:when test="$langISO = 'zho'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang650basicChi"/>
            </xsl:when>
            <xsl:when test="$langISO = 'hat'">
                <!-- code match, though labels differ -->
                <!-- ISO 639-3: Haitian -->
                <!-- marc: Haitian French Creole -->
                <xsl:call-template name="lang650basicHat"/>
            </xsl:when>
            <xsl:when test="$langISO = 'hrv'">
                <!-- code match -->
                <!-- ISO 639-3: Croatian -->
                <!-- marc: Croatian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Croatian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ces'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Czech -->
                <!-- marc: Czech -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Czech language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'dan'">
                <!-- code match -->
                <!-- ISO 639-3: Danish -->
                <!-- marc: Danish -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Danish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'prs'">
                <!-- match with macrolanguage; ISO 639-2/B synonym; also, MARC language name Dari assigned to collective code per -->
                <!-- ISO 639-3: Dari -->
                <!-- marc: Dari -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Dari language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'kmj'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- ISO 639-3: Kumarbhag Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="lang650basicDra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'mjt'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- ISO 639-3: Sauria Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="lang650basicDra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'mkb'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- ISO 639-3: Mal Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="lang650basicDra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'nld'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Dutch -->
                <!-- marc: Dutch -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Dutch language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'eng'">
                <!-- code match -->
                <!-- ISO 639-3: English -->
                <!-- marc: English -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">English language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'est'">
                <!-- code match -->
                <!-- ISO 639-3: Estonian -->
                <!-- marc: Estonian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Estonian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'fra'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: French -->
                <!-- marc: French -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">French language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'kat'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Georgian -->
                <!-- marc: Georgian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Georgian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'deu'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: German -->
                <!-- marc: German -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">German language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ell'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Modern Greek (1453-) -->
                <!-- marc: Greek, Modern (1453-) -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Greek language, Modern</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'hau'">
                <!-- code match -->
                <!-- ISO 639-3: Hausa -->
                <!-- marc: Hausa -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Hausa language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'hin'">
                <!-- code match -->
                <!-- ISO 639-3: Hindi -->
                <!-- marc: Hindi -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Hindi language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'hun'">
                <!-- code match -->
                <!-- ISO 639-3: Hungarian -->
                <!-- marc: Hungarian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Hungarian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ind'">
                <!-- code match -->
                <!-- ISO 639-3: Indonesian -->
                <!-- marc: Indonesian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Indonesian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ita'">
                <!-- code match -->
                <!-- ISO 639-3: Italian -->
                <!-- marc: Italian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Italian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'jpn'">
                <!-- code match -->
                <!-- ISO 639-3: Japanese -->
                <!-- marc: Japanese -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Japanese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'khm'">
                <!-- code match, though labels differ -->
                <!-- ISO 639-3: Central Khmer -->
                <!-- marc: Khmer -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Khmer language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'kor'">
                <!-- code match -->
                <!-- ISO 639-3: Korean -->
                <!-- marc: Korean -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Korean language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'kmr'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Northern Kurdish -->
                <!-- marc: Kurdish -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Kurdish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'pnb'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Western Panjabi -->
                <!-- marc: Lahndā -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Lahndā language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'lao'">
                <!-- code match -->
                <!-- ISO 639-3: Lao -->
                <!-- marc: Lao -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Lao language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'lat'">
                <!-- code match -->
                <!-- ISO 639-3: Latin -->
                <!-- marc: Latin -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Latin language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'lit'">
                <!-- code match -->
                <!-- ISO 639-3: Lithuanian -->
                <!-- marc: Lithuanian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Lithuanian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'zsm'">
                <!-- match with macrolanguage; ISO 639-2/B synonym -->
                <!-- ISO 639-3: Standard Malay -->
                <!-- marc: Malay -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Malay language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'cmn'">
                <!-- match with macrolanguage; ISO 639-2/B synonym -->
                <!-- ISO 639-3: Mandarin Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Mandarin dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'emk'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Eastern Maninkakan -->
                <!-- marc: Mandingo -->
                <xsl:call-template name="lang650basicMan"/>
            </xsl:when>
            <xsl:when test="$langISO = 'mxx'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Mahou -->
                <!-- marc: Mandingo -->
                <xsl:call-template name="lang650basicMan"/>
            </xsl:when>
            <xsl:when test="$langISO = 'kxm'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Northern Khmer -->
                <!-- marc: Northern Khmer -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Northern Khmer language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'nob'">
                <!-- code match -->
                <!-- ISO 639-3: Norwegian Bokmål -->
                <!-- marc: Norwegian (Bokmål) -->
                <xsl:call-template name="lang650basicNor"/>
            </xsl:when>
            <xsl:when test="$langISO = 'nor'">
                <!-- code match -->
                <!-- ISO 639-3: Norwegian -->
                <!-- marc: Norwegian -->
                <xsl:call-template name="lang650basicNor"/>
            </xsl:when>
            <xsl:when test="$langISO = 'nno'">
                <!-- code match -->
                <!-- ISO 639-3: Norwegian Nynorsk -->
                <!-- marc: Norwegian (Nynorsk) -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Norwegian language (Nynorsk)</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'pan'">
                <!-- code match -->
                <!-- ISO 639-3: Panjabi -->
                <!-- marc: Panjabi -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Panjabi language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'fas'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Persian -->
                <!-- marc: Persian -->
                <xsl:call-template name="lang650basicPer"/>
            </xsl:when>
            <xsl:when test="$langISO = 'pes'">
                <!-- match with macrolanguage; ISO 639-2/B synonym -->
                <!-- ISO 639-3: Iranian Persian -->
                <!-- marc: Persian -->
                <xsl:call-template name="lang650basicPer"/>
            </xsl:when>
            <xsl:when test="$langISO = 'pol'">
                <!-- code match -->
                <!-- ISO 639-3: Polish -->
                <!-- marc: Polish -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Polish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'por'">
                <!-- code match -->
                <!-- ISO 639-3: Portuguese -->
                <!-- marc: Portuguese -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Portuguese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'pus'">
                <!-- code match -->
                <!-- ISO 639-3: Pushto -->
                <!-- marc: Pushto -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Pushto language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ron'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Romanian -->
                <!-- marc: Romanian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Romanian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'rus'">
                <!-- code match -->
                <!-- ISO 639-3: Russian -->
                <!-- marc: Russian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Russian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'san'">
                <!-- code match -->
                <!-- ISO 639-3: Sanskrit -->
                <!-- marc: Sanskrit -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Sanskrit language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'gla'">
                <!-- code match -->
                <!-- ISO 639-3: Scottish Gaelic -->
                <!-- marc: Scottish Gaelic -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Scottish Gaelic language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'gul'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Sea Island Creole English -->
                <!-- marc: Sea Islands Creole -->
                <xsl:call-template name="lang650basicCpe"/>
            </xsl:when>
            <xsl:when test="$langISO = 'trf'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Trinidadian Creole English -->
                <!-- marc: Sea Islands Creole -->
                <xsl:call-template name="lang650basicCpe"/>
            </xsl:when>
            <xsl:when test="$langISO = 'srp'">
                <!-- code match -->
                <!-- ISO 639-3: Serbian -->
                <!-- marc: Serbian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Serbian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'slk'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Slovak -->
                <!-- marc: Slovak -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Slovak language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'slv'">
                <!-- code match -->
                <!-- ISO 639-3: Slovenian -->
                <!-- marc: Slovenian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Slovenian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'som'">
                <!-- code match -->
                <!-- ISO 639-3: Somali -->
                <!-- marc: Somali -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Somali language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ajp'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: South Levantine Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang650basicAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'nan'">
                <!-- match with macrolanguage; ISO 639-2/B synonym -->
                <!-- ISO 639-3: Min Nan Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Southern Min dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'spa'">
                <!-- code match -->
                <!-- ISO 639-3: Spanish -->
                <!-- marc: Spanish -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Spanish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'swa'">
                <!-- code match -->
                <!-- ISO 639-3: Swahili -->
                <!-- marc: Swahili -->
                <xsl:call-template name="lang650basicSwa"/>
            </xsl:when>
            <xsl:when test="$langISO = 'swc'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Congo Swahili -->
                <!-- marc: Swahili -->
                <xsl:call-template name="lang650basicSwa"/>
            </xsl:when>
            <xsl:when test="$langISO = 'swh'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Swahili (individual language) -->
                <!-- marc: Swahili -->
                <xsl:call-template name="lang650basicSwa"/>
            </xsl:when>
            <xsl:when test="$langISO = 'swe'">
                <!-- code match -->
                <!-- ISO 639-3: Swedish -->
                <!-- marc: Swedish -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Swedish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tgl'">
                <!-- code match -->
                <!-- ISO 639-3: Tagalog -->
                <!-- marc: Tagalog -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Tagalog language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tam'">
                <!-- code match -->
                <!-- ISO 639-3: Tamil -->
                <!-- marc: Tamil -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Tamil language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tha'">
                <!-- code match -->
                <!-- ISO 639-3: Thai -->
                <!-- marc: Thai -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Thai language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tir'">
                <!-- code match -->
                <!-- ISO 639-3: Tigrinya -->
                <!-- marc: Tigrinya -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Tigrinya language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tpi'">
                <!-- code match -->
                <!-- ISO 639-3: Tok Pisin -->
                <!-- marc: Tok Pisin -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Tok Pisin language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tur'">
                <!-- code match -->
                <!-- ISO 639-3: Turkish -->
                <!-- marc: Turkish -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Turkish language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ukr'">
                <!-- code match -->
                <!-- ISO 639-3: Ukrainian -->
                <!-- marc: Ukrainian -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Ukrainian language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'urd'">
                <!-- code match -->
                <!-- ISO 639-3: Urdu -->
                <!-- marc: Urdu -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Urdu language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'uzb'">
                <!-- code match -->
                <!-- ISO 639-3: Uzbek -->
                <!-- marc: Uzbek -->
                <xsl:call-template name="lang650basicUzb"/>
            </xsl:when>
            <xsl:when test="$langISO = 'uzn'">
                <!-- match with macrolanguage -->
                <!-- ISO 639-3: Northern Uzbek -->
                <!-- marc: Uzbek -->
                <xsl:call-template name="lang650basicUzb"/>
            </xsl:when>
            <xsl:when test="$langISO = 'vie'">
                <!-- code match -->
                <!-- ISO 639-3: Vietnamese -->
                <!-- marc: Vietnamese -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Vietnamese language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'wuu'">
                <!-- match with macrolanguage; ISO 639-2/B synonym -->
                <!-- ISO 639-3: Wu Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Wu dialects</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ybb'">
                <!-- match based on label, marc assigned collective code -->
                <!-- ISO 639-3: Yemba -->
                <!-- marc: Yemba -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Yemba language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'luq'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Lucumi -->
                <!-- marc: Yoruba -->
                <xsl:call-template name="lang650basicYor"/>
            </xsl:when>
            <xsl:when test="$langISO = 'yor'">
                <!-- code match -->
                <!-- ISO 639-3: Yoruba -->
                <!-- marc: Yoruba -->
                <xsl:call-template name="lang650basicYor"/>
            </xsl:when>
            <xsl:when test="$langISO = 'zul'">
                <!-- code match -->
                <!-- ISO 639-3: Zulu -->
                <!-- marc: Zulu -->
                <xsl:call-template name="lang650basicDefault">
                    <xsl:with-param name="langLCSH">Zulu language</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'zxx'"/>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang650basicDefault">
        <xsl:param name="langLCSH"/>
        <marc:datafield tag="650" ind1=" " ind2="0">
            <marc:subfield code="a">
                <xsl:value-of select="$langLCSH"/>
            </marc:subfield>
            <marc:subfield code="x">
                <xsl:text>Data processing</xsl:text>
            </marc:subfield>
            <marc:subfield code="v">
                <xsl:text>Databases.</xsl:text>
            </marc:subfield>
        </marc:datafield>
    </xsl:template>
    <xsl:template name="lang650basicAlb">
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
    <xsl:template name="lang650basicAra">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'abv'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'acm'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'afb'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'ajp'"/>
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
    <xsl:template name="lang650basicChi">
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
    <xsl:template name="lang650basicDra">
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
    <xsl:template name="lang650basicHat">
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
    <xsl:template name="lang650basicMan">
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
    <xsl:template name="lang650basicNor">
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
    <xsl:template name="lang650basicPer">
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
    <xsl:template name="lang650basicCpe">
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
    <xsl:template name="lang650basicSwa">
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
    <xsl:template name="lang650basicUzb">
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
    <xsl:template name="lang650basicYor">
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
