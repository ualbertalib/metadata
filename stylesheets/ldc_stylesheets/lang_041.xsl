<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
    exclude-result-prefixes="xs dc"
    version="2.0">
    <xsl:template name="lang041">
        <!-- The mappings in this stylesheet are maintained in a table at https://docs.google.com/spreadsheets/d/1pJ7QJTH-6qaxAjAlQxVO9cMNgyAmCgUtK8LFAgy7jZ0/edit?usp=sharing -->
        <xsl:param name="langISO"/>
        <xsl:choose>
            <xsl:when test="$langISO='als'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Tosk Albanian -->
                <!-- marc: Albanian -->
                <xsl:call-template name="lang041alb"/>
            </xsl:when>
            <xsl:when test="$langISO='sqi'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Albanian -->
                <!-- marc: Albanian -->
                <xsl:call-template name="lang041alb"/>
            </xsl:when>
            <xsl:when test="$langISO='amh'">
                <!-- code match -->
                <!-- ISO 639-3: Amharic -->
                <!-- marc: Amharic -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">amh</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='abv'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Baharna Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='acm'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Mesopotamian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='afb'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Gulf Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='apc'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: North Levantine Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='ara'">
                <!-- code match -->
                <!-- ISO 639-3: Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='arb'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Standard Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='ary'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Moroccan Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='arz'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Egyptian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='ayp'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: North Mesopotamian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="lang041ara"/>
            </xsl:when>
            <xsl:when test="$langISO='asm'">
                <!-- code match -->
                <!-- ISO 639-3: Assamese -->
                <!-- marc: Assamese -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">asm</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='jgo'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Ngomba -->
                <!-- marc: Bamileke languages -->
                <xsl:call-template name="lang041bai"/>
            </xsl:when>
            <xsl:when test="$langISO='ybb'">
                <!-- match based on label, marc assigned collective code -->
                <!-- ISO 639-3: Yemba -->
                <!-- marc: Yemba -->
                <xsl:call-template name="lang041bai"/>
            </xsl:when>
            <xsl:when test="$langISO='bam'">
                <!-- code match -->
                <!-- ISO 639-3: Bambara -->
                <!-- marc: Bambara -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">bam</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='eus'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Basque -->
                <!-- marc: Basque -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">baq</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='ben'">
                <!-- code match -->
                <!-- ISO 639-3: Bengali -->
                <!-- marc: Bengali -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">ben</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='bos'">
                <!-- code match -->
                <!-- ISO 639-3: Bosnian -->
                <!-- marc: Bosnian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">bos</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='bul'">
                <!-- code match -->
                <!-- ISO 639-3: Bulgarian -->
                <!-- marc: Bulgarian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">bul</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='cat'">
                <!-- code match -->
                <!-- ISO 639-3: Catalan -->
                <!-- marc: Catalan -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">cat</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='ceb'">
                <!-- code match -->
                <!-- ISO 639-3: Cebuano -->
                <!-- marc: Cebuano -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">ceb</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='cmn'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- ISO 639-3: Mandarin Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang041chi"/>
            </xsl:when>
            <xsl:when test="$langISO='lzh'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Literary Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang041chi"/>
            </xsl:when>
            <xsl:when test="$langISO='nan'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Min Nan Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang041chi"/>
            </xsl:when>
            <xsl:when test="$langISO='wuu'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Wu Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang041chi"/>
            </xsl:when>
            <xsl:when test="$langISO='yue'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- ISO 639-3: Yue Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang041chi"/>
            </xsl:when>
            <xsl:when test="$langISO='zho'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="lang041chi"/>
            </xsl:when>
            <xsl:when test="$langISO='gul'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Sea Island Creole English -->
                <!-- marc: Sea Islands Creole -->
                <xsl:call-template name="lang041cpe"/>
            </xsl:when>
            <xsl:when test="$langISO='trf'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Trinidadian Creole English -->
                <!-- marc: Sea Islands Creole -->
                <xsl:call-template name="lang041cpe"/>
            </xsl:when>
            <xsl:when test="$langISO='ces'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Czech -->
                <!-- marc: Czech -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">cze</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='dan'">
                <!-- code match -->
                <!-- ISO 639-3: Danish -->
                <!-- marc: Danish -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">dan</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='kmj'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- ISO 639-3: Kumarbhag Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="lang041dra"/>
            </xsl:when>
            <xsl:when test="$langISO='mjt'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- ISO 639-3: Sauria Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="lang041dra"/>
            </xsl:when>
            <xsl:when test="$langISO='mkb'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- ISO 639-3: Mal Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="lang041dra"/>
            </xsl:when>
            <xsl:when test="$langISO='nld'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Dutch -->
                <!-- marc: Dutch -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">dut</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='eng'">
                <!-- code match -->
                <!-- ISO 639-3: English -->
                <!-- marc: English -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">eng</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='est'">
                <!-- code match -->
                <!-- ISO 639-3: Estonian -->
                <!-- marc: Estonian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">est</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='fra'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: French -->
                <!-- marc: French -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">fre</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='kat'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Georgian -->
                <!-- marc: Georgian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">geo</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='deu'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: German -->
                <!-- marc: German -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">ger</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='gla'">
                <!-- code match -->
                <!-- ISO 639-3: Scottish Gaelic -->
                <!-- marc: Scottish Gaelic -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">gla</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='ell'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Modern Greek (1453-) -->
                <!-- marc: Greek, Modern (1453-) -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">gre</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='hat'">
                <!-- code match, though labels differ -->
                <!-- ISO 639-3: Haitian -->
                <!-- marc: Haitian French Creole -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">hat</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='hau'">
                <!-- code match -->
                <!-- ISO 639-3: Hausa -->
                <!-- marc: Hausa -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">hau</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='hin'">
                <!-- code match -->
                <!-- ISO 639-3: Hindi -->
                <!-- marc: Hindi -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">hin</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='hrv'">
                <!-- code match -->
                <!-- ISO 639-3: Croatian -->
                <!-- marc: Croatian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">hrv</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='hun'">
                <!-- code match -->
                <!-- ISO 639-3: Hungarian -->
                <!-- marc: Hungarian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">hun</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='ind'">
                <!-- code match -->
                <!-- ISO 639-3: Indonesian -->
                <!-- marc: Indonesian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">ind</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='ita'">
                <!-- code match -->
                <!-- ISO 639-3: Italian -->
                <!-- marc: Italian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">ita</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='jpn'">
                <!-- code match -->
                <!-- ISO 639-3: Japanese -->
                <!-- marc: Japanese -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">jpn</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='khm'">
                <!-- code match, though labels differ -->
                <!-- ISO 639-3: Central Khmer -->
                <!-- marc: Khmer -->
                <xsl:call-template name="lang041khm"/>
            </xsl:when>
            <xsl:when test="$langISO='kxm'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Northern Khmer -->
                <!-- marc: Northern Khmer -->
                <xsl:call-template name="lang041khm"/>
            </xsl:when>
            <xsl:when test="$langISO='kor'">
                <!-- code match -->
                <!-- ISO 639-3: Korean -->
                <!-- marc: Korean -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">kor</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='kmr'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Northern Kurdish -->
                <!-- marc: Kurdish -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">kur</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='pnb'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- ISO 639-3: Western Panjabi -->
                <!-- marc: Lahndā -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">lah</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='lao'">
                <!-- code match -->
                <!-- ISO 639-3: Lao -->
                <!-- marc: Lao -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">lao</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='lat'">
                <!-- code match -->
                <!-- ISO 639-3: Latin -->
                <!-- marc: Latin -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">lat</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='lit'">
                <!-- code match -->
                <!-- ISO 639-3: Lithuanian -->
                <!-- marc: Lithuanian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">lit</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='emk'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- ISO 639-3: Eastern Maninkakan -->
                <!-- marc: Mandingo -->
                <xsl:call-template name="lang041man"/>
            </xsl:when>
            <xsl:when test="$langISO='mxx'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Mahou -->
                <!-- marc: Mandingo -->
                <xsl:call-template name="lang041man"/>
            </xsl:when>
            <xsl:when test="$langISO='zsm'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Standard Malay -->
                <!-- marc: Malay -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">may</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='nno'">
                <!-- code match -->
                <!-- ISO 639-3: Norwegian Nynorsk -->
                <!-- marc: Norwegian (Nynorsk) -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">nno</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='nob'">
                <!-- code match -->
                <!-- ISO 639-3: Norwegian Bokmål -->
                <!-- marc: Norwegian (Bokmål) -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">nob</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='nor'">
                <!-- code match -->
                <!-- ISO 639-3: Norwegian -->
                <!-- marc: Norwegian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">nor</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='pan'">
                <!-- code match -->
                <!-- ISO 639-3: Panjabi -->
                <!-- marc: Panjabi -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">pan</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='fas'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Persian -->
                <!-- marc: Persian -->
                <xsl:call-template name="lang041per"/>
            </xsl:when>
            <xsl:when test="$langISO='pes'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Iranian Persian -->
                <!-- marc: Persian -->
                <xsl:call-template name="lang041per"/>
            </xsl:when>
            <xsl:when test="$langISO='prs'">
                <!-- match based on label, marc assigned collective code -->
                <!-- ISO 639-3: Dari -->
                <!-- marc: Dari -->
                <xsl:call-template name="lang041per"/>
            </xsl:when>
            <xsl:when test="$langISO='pol'">
                <!-- code match -->
                <!-- ISO 639-3: Polish -->
                <!-- marc: Polish -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">pol</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='por'">
                <!-- code match -->
                <!-- ISO 639-3: Portuguese -->
                <!-- marc: Portuguese -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">por</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='pus'">
                <!-- code match -->
                <!-- ISO 639-3: Pushto -->
                <!-- marc: Pushto -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">pus</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='ron'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Romanian -->
                <!-- marc: Romanian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">rum</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='rus'">
                <!-- code match -->
                <!-- ISO 639-3: Russian -->
                <!-- marc: Russian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">rus</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='san'">
                <!-- code match -->
                <!-- ISO 639-3: Sanskrit -->
                <!-- marc: Sanskrit -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">san</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='ajp'">
                <!-- best fit based on label, marc assigned collective code -->
                <!-- ISO 639-3: South Levantine Arabic -->
                <!-- marc: South Arabic -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">sem</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='slk'">
                <!-- ISO 639-2/B synonym -->
                <!-- ISO 639-3: Slovak -->
                <!-- marc: Slovak -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">slo</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='slv'">
                <!-- code match -->
                <!-- ISO 639-3: Slovenian -->
                <!-- marc: Slovenian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">slv</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='som'">
                <!-- code match -->
                <!-- ISO 639-3: Somali -->
                <!-- marc: Somali -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">som</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='spa'">
                <!-- code match -->
                <!-- ISO 639-3: Spanish -->
                <!-- marc: Spanish -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">spa</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='srp'">
                <!-- code match -->
                <!-- ISO 639-3: Serbian -->
                <!-- marc: Serbian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">srp</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='swa'">
                <!-- code match -->
                <!-- ISO 639-3: Swahili -->
                <!-- marc: Swahili -->
                <xsl:call-template name="lang041swa"/>
            </xsl:when>
            <xsl:when test="$langISO='swc'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Congo Swahili -->
                <!-- marc: Swahili -->
                <xsl:call-template name="lang041swa"/>
            </xsl:when>
            <xsl:when test="$langISO='swh'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Swahili (individual language) -->
                <!-- marc: Swahili -->
                <xsl:call-template name="lang041swa"/>
            </xsl:when>
            <xsl:when test="$langISO='swe'">
                <!-- code match -->
                <!-- ISO 639-3: Swedish -->
                <!-- marc: Swedish -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">swe</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='tam'">
                <!-- code match -->
                <!-- ISO 639-3: Tamil -->
                <!-- marc: Tamil -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">tam</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='tgl'">
                <!-- code match -->
                <!-- ISO 639-3: Tagalog -->
                <!-- marc: Tagalog -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">tgl</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='tha'">
                <!-- code match -->
                <!-- ISO 639-3: Thai -->
                <!-- marc: Thai -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">tha</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='tir'">
                <!-- code match -->
                <!-- ISO 639-3: Tigrinya -->
                <!-- marc: Tigrinya -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">tir</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='tpi'">
                <!-- code match -->
                <!-- ISO 639-3: Tok Pisin -->
                <!-- marc: Tok Pisin -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">tpi</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='tur'">
                <!-- code match -->
                <!-- ISO 639-3: Turkish -->
                <!-- marc: Turkish -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">tur</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='ukr'">
                <!-- code match -->
                <!-- ISO 639-3: Ukrainian -->
                <!-- marc: Ukrainian -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">ukr</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='urd'">
                <!-- code match -->
                <!-- ISO 639-3: Urdu -->
                <!-- marc: Urdu -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">urd</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='uzb'">
                <!-- code match -->
                <!-- ISO 639-3: Uzbek -->
                <!-- marc: Uzbek -->
                <xsl:call-template name="lang041uzb"/>
            </xsl:when>
            <xsl:when test="$langISO='uzn'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Northern Uzbek -->
                <!-- marc: Uzbek -->
                <xsl:call-template name="lang041uzb"/>
            </xsl:when>
            <xsl:when test="$langISO='vie'">
                <!-- code match -->
                <!-- ISO 639-3: Vietnamese -->
                <!-- marc: Vietnamese -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">vie</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='luq'">
                <!-- best fit based on label -->
                <!-- ISO 639-3: Lucumi -->
                <!-- marc: Yoruba -->
                <xsl:call-template name="lang041yor"/>
            </xsl:when>
            <xsl:when test="$langISO='yor'">
                <!-- code match -->
                <!-- ISO 639-3: Yoruba -->
                <!-- marc: Yoruba -->
                <xsl:call-template name="lang041yor"/>
            </xsl:when>
            <xsl:when test="$langISO='zul'">
                <!-- code match -->
                <!-- ISO 639-3: Zulu -->
                <!-- marc: Zulu -->
                <xsl:call-template name="lang041default">
                    <xsl:with-param name="langMARC">zul</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO='zxx'">
                <!-- code match, though labels differ -->
                <!-- ISO 639-3: Vervet Monkey Calls -->
                <!-- marc: No linguistic content -->
                <xsl:call-template name="lang041zxx"/>
            </xsl:when>
            <xsl:when test="$langISO='zxx'">
                <!-- code match -->
                <!-- ISO 639-3: No linguistic content -->
                <!-- marc: No linguistic content -->
                <xsl:call-template name="lang041zxx"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041default">
        <xsl:param name="langMARC"/>
        <marc:subfield code="a">
            <xsl:value-of select="$langMARC"/>
        </marc:subfield>
    </xsl:template>
    <xsl:template name="lang041alb">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'als'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'sqi'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>alb</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041ara">
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
                <marc:subfield code="a">
                    <xsl:text>ara</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041bai">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'jgo'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'ybb'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>bai</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041chi">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'cmn'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'lzh'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'nan'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'wuu'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'yue'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'zho'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>chi</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041cpe">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'gul'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'trf'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>cpe</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041dra">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'kmj'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'mjt'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'mkb'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>dra</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041khm">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'khm'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'kxm'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>khm</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041man">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'emk'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'mxx'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>man</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041per">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'fas'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'pes'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'prs'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>per</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041swa">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'swa'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'swc'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'swh'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>swa</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041uzb">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'uzb'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'uzn'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>uzb</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041yor">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'luq'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'yor'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>yor</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang041zxx">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'zxx'"/>
            <xsl:otherwise>
                <marc:subfield code="a">
                    <xsl:text>zxx</xsl:text>
                </marc:subfield> 
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>