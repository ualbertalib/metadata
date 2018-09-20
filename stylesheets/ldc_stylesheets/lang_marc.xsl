<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
    exclude-result-prefixes="xs dc"
    version="2.0">
    <xsl:template name="langMarc">
        <xsl:param name="lang"/>
        <xsl:choose>
            <xsl:when test="$lang='als'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Tosk Albanian -->
                <!-- marc: Albanian -->
                <xsl:call-template name="marc041alb"/>
            </xsl:when>
            <xsl:when test="$lang='sqi'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Albanian -->
                <!-- marc: Albanian -->
                <xsl:call-template name="marc041alb"/>
            </xsl:when>
            <xsl:when test="$lang='amh'">
                <!-- code match -->
                <!-- iso 639-3: Amharic -->
                <!-- marc: Amharic -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">amh</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='abv'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Baharna Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='acm'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Mesopotamian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='afb'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Gulf Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='apc'">
                <!-- best fit based on label -->
                <!-- iso 639-3: North Levantine Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='ara'">
                <!-- code match -->
                <!-- iso 639-3: Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='arb'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Standard Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='ary'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Moroccan Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='arz'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Egyptian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='ayp'">
                <!-- best fit based on label -->
                <!-- iso 639-3: North Mesopotamian Arabic -->
                <!-- marc: Arabic -->
                <xsl:call-template name="marc041ara"/>
            </xsl:when>
            <xsl:when test="$lang='asm'">
                <!-- code match -->
                <!-- iso 639-3: Assamese -->
                <!-- marc: Assamese -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">asm</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='jgo'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Ngomba -->
                <!-- marc: Bamileke languages -->
                <xsl:call-template name="marc041bai"/>
            </xsl:when>
            <xsl:when test="$lang='ybb'">
                <!-- match based on label, marc assigned collective code -->
                <!-- iso 639-3: Yemba -->
                <!-- marc: Yemba -->
                <xsl:call-template name="marc041bai"/>
            </xsl:when>
            <xsl:when test="$lang='bam'">
                <!-- code match -->
                <!-- iso 639-3: Bambara -->
                <!-- marc: Bambara -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">bam</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='eus'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Basque -->
                <!-- marc: Basque -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">baq</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='ben'">
                <!-- code match -->
                <!-- iso 639-3: Bengali -->
                <!-- marc: Bengali -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">ben</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='bos'">
                <!-- code match -->
                <!-- iso 639-3: Bosnian -->
                <!-- marc: Bosnian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">bos</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='bul'">
                <!-- code match -->
                <!-- iso 639-3: Bulgarian -->
                <!-- marc: Bulgarian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">bul</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='cat'">
                <!-- code match -->
                <!-- iso 639-3: Catalan -->
                <!-- marc: Catalan -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">cat</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='ceb'">
                <!-- code match -->
                <!-- iso 639-3: Cebuano -->
                <!-- marc: Cebuano -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">ceb</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='cmn'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- iso 639-3: Mandarin Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="marc041chi"/>
            </xsl:when>
            <xsl:when test="$lang='lzh'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Literary Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="marc041chi"/>
            </xsl:when>
            <xsl:when test="$lang='nan'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Min Nan Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="marc041chi"/>
            </xsl:when>
            <xsl:when test="$lang='wuu'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Wu Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="marc041chi"/>
            </xsl:when>
            <xsl:when test="$lang='yue'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- iso 639-3: Yue Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="marc041chi"/>
            </xsl:when>
            <xsl:when test="$lang='zho'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Chinese -->
                <!-- marc: Chinese -->
                <xsl:call-template name="marc041chi"/>
            </xsl:when>
            <xsl:when test="$lang='gul'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Sea Island Creole English -->
                <!-- marc: Sea Islands Creole -->
                <xsl:call-template name="marc041cpe"/>
            </xsl:when>
            <xsl:when test="$lang='trf'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Trinidadian Creole English -->
                <!-- marc: Sea Islands Creole -->
                <xsl:call-template name="marc041cpe"/>
            </xsl:when>
            <xsl:when test="$lang='ces'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Czech -->
                <!-- marc: Czech -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">cze</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='dan'">
                <!-- code match -->
                <!-- iso 639-3: Danish -->
                <!-- marc: Danish -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">dan</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='kmj'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- iso 639-3: Kumarbhag Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="marc041dra"/>
            </xsl:when>
            <xsl:when test="$lang='mjt'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- iso 639-3: Sauria Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="marc041dra"/>
            </xsl:when>
            <xsl:when test="$lang='mkb'">
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- iso 639-3: Mal Paharia -->
                <!-- marc: Dravidian (Other) -->
                <xsl:call-template name="marc041dra"/>
            </xsl:when>
            <xsl:when test="$lang='nld'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Dutch -->
                <!-- marc: Dutch -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">dut</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='eng'">
                <!-- code match -->
                <!-- iso 639-3: English -->
                <!-- marc: English -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">eng</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='est'">
                <!-- code match -->
                <!-- iso 639-3: Estonian -->
                <!-- marc: Estonian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">est</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='fra'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: French -->
                <!-- marc: French -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">fre</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='kat'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Georgian -->
                <!-- marc: Georgian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">geo</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='deu'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: German -->
                <!-- marc: German -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">ger</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='gla'">
                <!-- code match -->
                <!-- iso 639-3: Scottish Gaelic -->
                <!-- marc: Scottish Gaelic -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">gla</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='ell'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Modern Greek (1453-) -->
                <!-- marc: Greek, Modern (1453-) -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">gre</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='hat'">
                <!-- code match, though labels differ -->
                <!-- iso 639-3: Haitian -->
                <!-- marc: Haitian French Creole -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">hat</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='hau'">
                <!-- code match -->
                <!-- iso 639-3: Hausa -->
                <!-- marc: Hausa -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">hau</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='hin'">
                <!-- code match -->
                <!-- iso 639-3: Hindi -->
                <!-- marc: Hindi -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">hin</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='hrv'">
                <!-- code match -->
                <!-- iso 639-3: Croatian -->
                <!-- marc: Croatian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">hrv</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='hun'">
                <!-- code match -->
                <!-- iso 639-3: Hungarian -->
                <!-- marc: Hungarian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">hun</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='ind'">
                <!-- code match -->
                <!-- iso 639-3: Indonesian -->
                <!-- marc: Indonesian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">ind</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='ita'">
                <!-- code match -->
                <!-- iso 639-3: Italian -->
                <!-- marc: Italian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">ita</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='jpn'">
                <!-- code match -->
                <!-- iso 639-3: Japanese -->
                <!-- marc: Japanese -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">jpn</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='khm'">
                <!-- code match, though labels differ -->
                <!-- iso 639-3: Central Khmer -->
                <!-- marc: Khmer -->
                <xsl:call-template name="marc041khm"/>
            </xsl:when>
            <xsl:when test="$lang='kxm'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Northern Khmer -->
                <!-- marc: Northern Khmer -->
                <xsl:call-template name="marc041khm"/>
            </xsl:when>
            <xsl:when test="$lang='kor'">
                <!-- code match -->
                <!-- iso 639-3: Korean -->
                <!-- marc: Korean -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">kor</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='kmr'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Northern Kurdish -->
                <!-- marc: Kurdish -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">kur</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='pnb'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- iso 639-3: Western Panjabi -->
                <!-- marc: Lahndā -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">lah</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='lao'">
                <!-- code match -->
                <!-- iso 639-3: Lao -->
                <!-- marc: Lao -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">lao</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='lat'">
                <!-- code match -->
                <!-- iso 639-3: Latin -->
                <!-- marc: Latin -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">lat</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='lit'">
                <!-- code match -->
                <!-- iso 639-3: Lithuanian -->
                <!-- marc: Lithuanian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">lit</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='emk'">
                <!-- marc preferred term ('use'), based on label match -->
                <!-- iso 639-3: Eastern Maninkakan -->
                <!-- marc: Mandingo -->
                <xsl:call-template name="marc041man"/>
            </xsl:when>
            <xsl:when test="$lang='mxx'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Mahou -->
                <!-- marc: Mandingo -->
                <xsl:call-template name="marc041man"/>
            </xsl:when>
            <xsl:when test="$lang='zsm'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Standard Malay -->
                <!-- marc: Malay -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">may</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='nno'">
                <!-- code match -->
                <!-- iso 639-3: Norwegian Nynorsk -->
                <!-- marc: Norwegian (Nynorsk) -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">nno</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='nob'">
                <!-- code match -->
                <!-- iso 639-3: Norwegian Bokmål -->
                <!-- marc: Norwegian (Bokmål) -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">nob</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='nor'">
                <!-- code match -->
                <!-- iso 639-3: Norwegian -->
                <!-- marc: Norwegian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">nor</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='pan'">
                <!-- code match -->
                <!-- iso 639-3: Panjabi -->
                <!-- marc: Panjabi -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">pan</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='fas'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Persian -->
                <!-- marc: Persian -->
                <xsl:call-template name="marc041per"/>
            </xsl:when>
            <xsl:when test="$lang='pes'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Iranian Persian -->
                <!-- marc: Persian -->
                <xsl:call-template name="marc041per"/>
            </xsl:when>
            <xsl:when test="$lang='prs'">
                <!-- match based on label, marc assigned collective code -->
                <!-- iso 639-3: Dari -->
                <!-- marc: Dari -->
                <xsl:call-template name="marc041per"/>
            </xsl:when>
            <xsl:when test="$lang='pol'">
                <!-- code match -->
                <!-- iso 639-3: Polish -->
                <!-- marc: Polish -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">pol</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='por'">
                <!-- code match -->
                <!-- iso 639-3: Portuguese -->
                <!-- marc: Portuguese -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">por</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='pus'">
                <!-- code match -->
                <!-- iso 639-3: Pushto -->
                <!-- marc: Pushto -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">pus</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='ron'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Romanian -->
                <!-- marc: Romanian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">rum</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='rus'">
                <!-- code match -->
                <!-- iso 639-3: Russian -->
                <!-- marc: Russian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">rus</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='san'">
                <!-- code match -->
                <!-- iso 639-3: Sanskrit -->
                <!-- marc: Sanskrit -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">san</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='ajp'">
                <!-- best fit based on label, marc assigned collective code -->
                <!-- iso 639-3: South Levantine Arabic -->
                <!-- marc: South Arabic -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">sem</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='slk'">
                <!-- ISO 239-2/B synonym -->
                <!-- iso 639-3: Slovak -->
                <!-- marc: Slovak -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">slo</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='slv'">
                <!-- code match -->
                <!-- iso 639-3: Slovenian -->
                <!-- marc: Slovenian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">slv</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='som'">
                <!-- code match -->
                <!-- iso 639-3: Somali -->
                <!-- marc: Somali -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">som</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='spa'">
                <!-- code match -->
                <!-- iso 639-3: Spanish -->
                <!-- marc: Spanish -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">spa</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='srp'">
                <!-- code match -->
                <!-- iso 639-3: Serbian -->
                <!-- marc: Serbian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">srp</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='swa'">
                <!-- code match -->
                <!-- iso 639-3: Swahili -->
                <!-- marc: Swahili -->
                <xsl:call-template name="marc041swa"/>
            </xsl:when>
            <xsl:when test="$lang='swc'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Congo Swahili -->
                <!-- marc: Swahili -->
                <xsl:call-template name="marc041swa"/>
            </xsl:when>
            <xsl:when test="$lang='swh'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Swahili (individual language) -->
                <!-- marc: Swahili -->
                <xsl:call-template name="marc041swa"/>
            </xsl:when>
            <xsl:when test="$lang='swe'">
                <!-- code match -->
                <!-- iso 639-3: Swedish -->
                <!-- marc: Swedish -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">swe</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='tam'">
                <!-- code match -->
                <!-- iso 639-3: Tamil -->
                <!-- marc: Tamil -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">tam</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='tgl'">
                <!-- code match -->
                <!-- iso 639-3: Tagalog -->
                <!-- marc: Tagalog -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">tgl</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='tha'">
                <!-- code match -->
                <!-- iso 639-3: Thai -->
                <!-- marc: Thai -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">tha</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='tir'">
                <!-- code match -->
                <!-- iso 639-3: Tigrinya -->
                <!-- marc: Tigrinya -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">tir</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='tpi'">
                <!-- code match -->
                <!-- iso 639-3: Tok Pisin -->
                <!-- marc: Tok Pisin -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">tpi</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='tur'">
                <!-- code match -->
                <!-- iso 639-3: Turkish -->
                <!-- marc: Turkish -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">tur</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='ukr'">
                <!-- code match -->
                <!-- iso 639-3: Ukrainian -->
                <!-- marc: Ukrainian -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">ukr</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='urd'">
                <!-- code match -->
                <!-- iso 639-3: Urdu -->
                <!-- marc: Urdu -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">urd</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='uzb'">
                <!-- code match -->
                <!-- iso 639-3: Uzbek -->
                <!-- marc: Uzbek -->
                <xsl:call-template name="marc041uzb"/>
            </xsl:when>
            <xsl:when test="$lang='uzn'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Northern Uzbek -->
                <!-- marc: Uzbek -->
                <xsl:call-template name="marc041uzb"/>
            </xsl:when>
            <xsl:when test="$lang='vie'">
                <!-- code match -->
                <!-- iso 639-3: Vietnamese -->
                <!-- marc: Vietnamese -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">vie</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='luq'">
                <!-- best fit based on label -->
                <!-- iso 639-3: Lucumi -->
                <!-- marc: Yoruba -->
                <xsl:call-template name="marc041yor"/>
            </xsl:when>
            <xsl:when test="$lang='yor'">
                <!-- code match -->
                <!-- iso 639-3: Yoruba -->
                <!-- marc: Yoruba -->
                <xsl:call-template name="marc041yor"/>
            </xsl:when>
            <xsl:when test="$lang='zul'">
                <!-- code match -->
                <!-- iso 639-3: Zulu -->
                <!-- marc: Zulu -->
                <xsl:call-template name="marc041">
                    <xsl:with-param name="langMarc">zul</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$lang='zxx'">
                <!-- code match, though labels differ -->
                <!-- iso 639-3: Vervet Monkey Calls -->
                <!-- marc: No linguistic content -->
                <xsl:call-template name="marc041zxx"/>
            </xsl:when>
            <xsl:when test="$lang='zxx'">
                <!-- code match -->
                <!-- iso 639-3: No linguistic content -->
                <!-- marc: No linguistic content -->
                <xsl:call-template name="marc041zxx"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="marc041">
        <xsl:param name="langMarc"/>
        <marc:subfield code="a">
            <xsl:value-of select="$langMarc"/>
        </marc:subfield>
    </xsl:template>
    <xsl:template name="marc041alb">
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
    <xsl:template name="marc041ara">
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
    <xsl:template name="marc041bai">
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
    <xsl:template name="marc041chi">
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
    <xsl:template name="marc041cpe">
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
    <xsl:template name="marc041dra">
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
    <xsl:template name="marc041khm">
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
    <xsl:template name="marc041man">
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
    <xsl:template name="marc041per">
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
    <xsl:template name="marc041swa">
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
    <xsl:template name="marc041uzb">
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
    <xsl:template name="marc041yor">
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
    <xsl:template name="marc041zxx">
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