<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
    xmlns:marc="http://www.loc.gov/MARC21/slim" exclude-result-prefixes="xs dc" version="2.0">
    <xsl:template name="lang650spoken">
        <!-- The mappings in this stylesheet are maintained in a table at https://docs.google.com/spreadsheets/d/1pJ7QJTH-6qaxAjAlQxVO9cMNgyAmCgUtK8LFAgy7jZ0/edit?usp=sharing -->
        <xsl:param name="langISO"/>
        <xsl:choose>
            <xsl:when test="$langISO = 'als'">
                <!-- ISO 639-3 label: Tosk Albanian -->
                <!-- best fit based on label -->
                <!-- marc code: alb -->
                <!-- marc label: Albanian -->
                <!-- lcsh: Albanian language -->
                <xsl:call-template name="lang650spokenAlb"/>
            </xsl:when>
            <xsl:when test="$langISO = 'sqi'">
                <!-- ISO 639-3 label: Albanian -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: alb -->
                <!-- marc label: Albanian -->
                <!-- lcsh: Albanian language -->
                <xsl:call-template name="lang650spokenAlb"/>
            </xsl:when>
            <xsl:when test="$langISO = 'amh'">
                <!-- ISO 639-3 label: Amharic -->
                <!-- code match -->
                <!-- marc code: amh -->
                <!-- marc label: Amharic -->
                <!-- lcsh: Amharic language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Amharic</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'abv'">
                <!-- ISO 639-3 label: Baharna Arabic -->
                <!-- best fit based on label -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'acm'">
                <!-- ISO 639-3 label: Mesopotamian Arabic -->
                <!-- best fit based on label -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'afb'">
                <!-- ISO 639-3 label: Gulf Arabic -->
                <!-- best fit based on label -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'apc'">
                <!-- ISO 639-3 label: North Levantine Arabic -->
                <!-- best fit based on label -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'ara'">
                <!-- ISO 639-3 label: Arabic -->
                <!-- code match -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'arb'">
                <!-- ISO 639-3 label: Standard Arabic -->
                <!-- best fit based on label -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'ary'">
                <!-- ISO 639-3 label: Moroccan Arabic -->
                <!-- best fit based on label -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'arz'">
                <!-- ISO 639-3 label: Egyptian Arabic -->
                <!-- best fit based on label -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'ayp'">
                <!-- ISO 639-3 label: North Mesopotamian Arabic -->
                <!-- best fit based on label -->
                <!-- marc code: ara -->
                <!-- marc label: Arabic -->
                <!-- lcsh: Arabic language -->
                <xsl:call-template name="lang650spokenAra"/>
            </xsl:when>
            <xsl:when test="$langISO = 'asm'">
                <!-- ISO 639-3 label: Assamese -->
                <!-- code match -->
                <!-- marc code: asm -->
                <!-- marc label: Assamese -->
                <!-- lcsh: Assamese language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Assamese</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'bam'">
                <!-- ISO 639-3 label: Bambara -->
                <!-- code match -->
                <!-- marc code: bam -->
                <!-- marc label: Bambara -->
                <!-- lcsh: Bambara language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Bambara</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'jgo'">
                <!-- ISO 639-3 label: Ngomba -->
                <!-- best fit based on label -->
                <!-- marc code: bai -->
                <!-- marc label: Bamileke languages -->
                <!-- lcsh: Bamileke languages -->
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Bamileke languages</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Bamileke</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:when>
            <xsl:when test="$langISO = 'eus'">
                <!-- ISO 639-3 label: Basque -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: baq -->
                <!-- marc label: Basque -->
                <!-- lcsh: Basque language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Basque</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ben'">
                <!-- ISO 639-3 label: Bengali -->
                <!-- code match -->
                <!-- marc code: ben -->
                <!-- marc label: Bengali -->
                <!-- lcsh: Bengali language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Bengali</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'bos'">
                <!-- ISO 639-3 label: Bosnian -->
                <!-- code match -->
                <!-- marc code: bos -->
                <!-- marc label: Bosnian -->
                <!-- lcsh: Bosnian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Bosnian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'bul'">
                <!-- ISO 639-3 label: Bulgarian -->
                <!-- code match -->
                <!-- marc code: bul -->
                <!-- marc label: Bulgarian -->
                <!-- lcsh: Bulgarian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Bulgarian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'yue'">
                <!-- ISO 639-3 label: Yue Chinese -->
                <!-- marc preferred term ('use'), based on label match -->
                <!-- marc code: chi -->
                <!-- marc label: Chinese -->
                <!-- lcsh: Cantonese dialects -->
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Cantonese dialects</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Chinese</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:when>
            <xsl:when test="$langISO = 'cat'">
                <!-- ISO 639-3 label: Catalan -->
                <!-- code match -->
                <!-- marc code: cat -->
                <!-- marc label: Catalan -->
                <!-- lcsh: Catalan language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Catalan</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ceb'">
                <!-- ISO 639-3 label: Cebuano -->
                <!-- code match -->
                <!-- marc code: ceb -->
                <!-- marc label: Cebuano -->
                <!-- lcsh: Cebuano language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Cebuano</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'lzh'">
                <!-- ISO 639-3 label: Literary Chinese -->
                <!-- best fit based on label -->
                <!-- marc code: chi -->
                <!-- marc label: Chinese -->
                <!-- lcsh: Chinese language -->
                <xsl:call-template name="lang650spokenChi"/>
            </xsl:when>
            <xsl:when test="$langISO = 'zho'">
                <!-- ISO 639-3 label: Chinese -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: chi -->
                <!-- marc label: Chinese -->
                <!-- lcsh: Chinese language -->
                <xsl:call-template name="lang650spokenChi"/>
            </xsl:when>
            <xsl:when test="$langISO = 'hat'">
                <!-- ISO 639-3 label: Haitian -->
                <!-- code match, though labels differ -->
                <!-- marc code: hat -->
                <!-- marc label: Haitian French Creole -->
                <!-- lcsh: Creole dialects, French$zHaiti -->
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Creole dialects, French</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="z">
                        <xsl:text>Haiti</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken French</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:when>
            <xsl:when test="$langISO = 'hrv'">
                <!-- ISO 639-3 label: Croatian -->
                <!-- code match -->
                <!-- marc code: hrv -->
                <!-- marc label: Croatian -->
                <!-- lcsh: Croatian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Croatian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ces'">
                <!-- ISO 639-3 label: Czech -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: cze -->
                <!-- marc label: Czech -->
                <!-- lcsh: Czech language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Czech</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'dan'">
                <!-- ISO 639-3 label: Danish -->
                <!-- code match -->
                <!-- marc code: dan -->
                <!-- marc label: Danish -->
                <!-- lcsh: Danish language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Danish</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'prs'">
                <!-- ISO 639-3 label: Dari -->
                <!-- match based on label, marc assigned collective code -->
                <!-- marc code: per -->
                <!-- marc label: Dari -->
                <!-- lcsh: Dari language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Dari</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'kmj'">
                <!-- ISO 639-3 label: Kumarbhag Paharia -->
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- marc code: dra -->
                <!-- marc label: Dravidian (Other) -->
                <!-- lcsh: Dravidian languages -->
                <xsl:call-template name="lang650spokenDra"/>                
            </xsl:when>
            <xsl:when test="$langISO = 'mjt'">
                <!-- ISO 639-3 label: Sauria Paharia -->
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- marc code: dra -->
                <!-- marc label: Dravidian (Other) -->
                <!-- lcsh: Dravidian languages -->
                <xsl:call-template name="lang650spokenDra"/>                
            </xsl:when>
            <xsl:when test="$langISO = 'mkb'">
                <!-- ISO 639-3 label: Mal Paharia -->
                <!-- marc assigned collective code for Malto (best fit based on label) -->
                <!-- marc code: dra -->
                <!-- marc label: Dravidian (Other) -->
                <!-- lcsh: Dravidian languages -->
                <xsl:call-template name="lang650spokenDra"/>                
            </xsl:when>
            <xsl:when test="$langISO = 'nld'">
                <!-- ISO 639-3 label: Dutch -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: dut -->
                <!-- marc label: Dutch -->
                <!-- lcsh: Dutch language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Dutch</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'eng'">
                <!-- ISO 639-3 label: English -->
                <!-- code match -->
                <!-- marc code: eng -->
                <!-- marc label: English -->
                <!-- lcsh: English language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">English</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'est'">
                <!-- ISO 639-3 label: Estonian -->
                <!-- code match -->
                <!-- marc code: est -->
                <!-- marc label: Estonian -->
                <!-- lcsh: Estonian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Estonian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'fra'">
                <!-- ISO 639-3 label: French -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: fre -->
                <!-- marc label: French -->
                <!-- lcsh: French language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">French</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'kat'">
                <!-- ISO 639-3 label: Georgian -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: geo -->
                <!-- marc label: Georgian -->
                <!-- lcsh: Georgian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Georgian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'deu'">
                <!-- ISO 639-3 label: German -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: ger -->
                <!-- marc label: German -->
                <!-- lcsh: German language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">German</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ell'">
                <!-- ISO 639-3 label: Modern Greek (1453-) -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: gre -->
                <!-- marc label: Greek, Modern (1453-) -->
                <!-- lcsh: Greek language, Modern -->
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Greek language, Modern</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Greek</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:when>
            <xsl:when test="$langISO = 'hau'">
                <!-- ISO 639-3 label: Hausa -->
                <!-- code match -->
                <!-- marc code: hau -->
                <!-- marc label: Hausa -->
                <!-- lcsh: Hausa language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Hausa</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'hin'">
                <!-- ISO 639-3 label: Hindi -->
                <!-- code match -->
                <!-- marc code: hin -->
                <!-- marc label: Hindi -->
                <!-- lcsh: Hindi language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Hindi</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'hun'">
                <!-- ISO 639-3 label: Hungarian -->
                <!-- code match -->
                <!-- marc code: hun -->
                <!-- marc label: Hungarian -->
                <!-- lcsh: Hungarian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Hungarian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ind'">
                <!-- ISO 639-3 label: Indonesian -->
                <!-- code match -->
                <!-- marc code: ind -->
                <!-- marc label: Indonesian -->
                <!-- lcsh: Indonesian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Indonesian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ita'">
                <!-- ISO 639-3 label: Italian -->
                <!-- code match -->
                <!-- marc code: ita -->
                <!-- marc label: Italian -->
                <!-- lcsh: Italian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Italian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'jpn'">
                <!-- ISO 639-3 label: Japanese -->
                <!-- code match -->
                <!-- marc code: jpn -->
                <!-- marc label: Japanese -->
                <!-- lcsh: Japanese language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Japanese</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'khm'">
                <!-- ISO 639-3 label: Central Khmer -->
                <!-- code match, though labels differ -->
                <!-- marc code: khm -->
                <!-- marc label: Khmer -->
                <!-- lcsh: Khmer language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Khmer</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'kor'">
                <!-- ISO 639-3 label: Korean -->
                <!-- code match -->
                <!-- marc code: kor -->
                <!-- marc label: Korean -->
                <!-- lcsh: Korean language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Korean</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'kmr'">
                <!-- ISO 639-3 label: Northern Kurdish -->
                <!-- best fit based on label -->
                <!-- marc code: kur -->
                <!-- marc label: Kurdish -->
                <!-- lcsh: Kurdish language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Kurdish</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'pnb'">
                <!-- ISO 639-3 label: Western Panjabi -->
                <!-- marc preferred term ('use'), based on label match -->
                <!-- marc code: lah -->
                <!-- marc label: Lahndā -->
                <!-- lcsh: Lahndā language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Lahndā</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'lao'">
                <!-- ISO 639-3 label: Lao -->
                <!-- code match -->
                <!-- marc code: lao -->
                <!-- marc label: Lao -->
                <!-- lcsh: Lao language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Lao</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'lat'">
                <!-- ISO 639-3 label: Latin -->
                <!-- code match -->
                <!-- marc code: lat -->
                <!-- marc label: Latin -->
                <!-- lcsh: Latin language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Latin</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'lit'">
                <!-- ISO 639-3 label: Lithuanian -->
                <!-- code match -->
                <!-- marc code: lit -->
                <!-- marc label: Lithuanian -->
                <!-- lcsh: Lithuanian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Lithuanian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'zsm'">
                <!-- ISO 639-3 label: Standard Malay -->
                <!-- best fit based on label -->
                <!-- marc code: may -->
                <!-- marc label: Malay -->
                <!-- lcsh: Malay language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Malay</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'cmn'">
                <!-- ISO 639-3 label: Mandarin Chinese -->
                <!-- marc preferred term ('use'), based on label match -->
                <!-- marc code: chi -->
                <!-- marc label: Chinese -->
                <!-- lcsh: Mandarin dialects -->
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Mandarin dialects</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Chinese</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:when>
            <xsl:when test="$langISO = 'emk'">
                <!-- ISO 639-3 label: Eastern Maninkakan -->
                <!-- marc preferred term ('use'), based on label match -->
                <!-- marc code: man -->
                <!-- marc label: Mandingo -->
                <!-- lcsh: Mandingo language -->
                <xsl:call-template name="lang650spokenMan"/>
            </xsl:when>
            <xsl:when test="$langISO = 'mxx'">
                <!-- ISO 639-3 label: Mahou -->
                <!-- best fit based on label -->
                <!-- marc code: man -->
                <!-- marc label: Mandingo -->
                <!-- lcsh: Mandingo language -->
                <xsl:call-template name="lang650spokenMan"/>
            </xsl:when>
            <xsl:when test="$langISO = 'kxm'">
                <!-- ISO 639-3 label: Northern Khmer -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: khm -->
                <!-- marc label: Northern Khmer -->
                <!-- lcsh: Northern Khmer language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Northern Khmer</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'nob'">
                <!-- ISO 639-3 label: Norwegian Bokmål -->
                <!-- code match -->
                <!-- marc code: nob -->
                <!-- marc label: Norwegian (Bokmål) -->
                <!-- lcsh: Norwegian language -->
                <xsl:call-template name="lang650spokenNor"/>     
            </xsl:when>
            <xsl:when test="$langISO = 'nor'">
                <!-- ISO 639-3 label: Norwegian -->
                <!-- code match -->
                <!-- marc code: nor -->
                <!-- marc label: Norwegian -->
                <!-- lcsh: Norwegian language -->
                <xsl:call-template name="lang650spokenNor"/>    
            </xsl:when>
            <xsl:when test="$langISO = 'nno'">
                <!-- ISO 639-3 label: Norwegian Nynorsk -->
                <!-- code match -->
                <!-- marc code: nno -->
                <!-- marc label: Norwegian (Nynorsk) -->
                <!-- lcsh: Norwegian language (Nynorsk) -->
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Norwegian language (Nynorsk)</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Norwegian (Nynorsk)</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:when>
            <xsl:when test="$langISO = 'pan'">
                <!-- ISO 639-3 label: Panjabi -->
                <!-- code match -->
                <!-- marc code: pan -->
                <!-- marc label: Panjabi -->
                <!-- lcsh: Panjabi language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Panjabi</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'fas'">
                <!-- ISO 639-3 label: Persian -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: per -->
                <!-- marc label: Persian -->
                <!-- lcsh: Persian language -->
                <xsl:call-template name="lang650spokenPer"/>                
            </xsl:when>
            <xsl:when test="$langISO = 'pes'">
                <!-- ISO 639-3 label: Iranian Persian -->
                <!-- best fit based on label -->
                <!-- marc code: per -->
                <!-- marc label: Persian -->
                <!-- lcsh: Persian language -->
                <xsl:call-template name="lang650spokenPer"/>
            </xsl:when>
            <xsl:when test="$langISO = 'pol'">
                <!-- ISO 639-3 label: Polish -->
                <!-- code match -->
                <!-- marc code: pol -->
                <!-- marc label: Polish -->
                <!-- lcsh: Polish language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Polish</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'por'">
                <!-- ISO 639-3 label: Portuguese -->
                <!-- code match -->
                <!-- marc code: por -->
                <!-- marc label: Portuguese -->
                <!-- lcsh: Portuguese language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Portuguese</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'pus'">
                <!-- ISO 639-3 label: Pushto -->
                <!-- code match -->
                <!-- marc code: pus -->
                <!-- marc label: Pushto -->
                <!-- lcsh: Pushto language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Pushto</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ron'">
                <!-- ISO 639-3 label: Romanian -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: rum -->
                <!-- marc label: Romanian -->
                <!-- lcsh: Romanian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Romanian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'rus'">
                <!-- ISO 639-3 label: Russian -->
                <!-- code match -->
                <!-- marc code: rus -->
                <!-- marc label: Russian -->
                <!-- lcsh: Russian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Russian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'san'">
                <!-- ISO 639-3 label: Sanskrit -->
                <!-- code match -->
                <!-- marc code: san -->
                <!-- marc label: Sanskrit -->
                <!-- lcsh: Sanskrit language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Sanskrit</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'gla'">
                <!-- ISO 639-3 label: Scottish Gaelic -->
                <!-- code match -->
                <!-- marc code: gla -->
                <!-- marc label: Scottish Gaelic -->
                <!-- lcsh: Scottish Gaelic language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Scottish Gaelic</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'gul'">
                <!-- ISO 639-3 label: Sea Island Creole English -->
                <!-- best fit based on label -->
                <!-- marc code: cpe -->
                <!-- marc label: Sea Islands Creole -->
                <!-- lcsh: Sea Islands Creole dialect -->
                <xsl:call-template name="lang650spokenCpe"/>
            </xsl:when>
            <xsl:when test="$langISO = 'trf'">
                <!-- ISO 639-3 label: Trinidadian Creole English -->
                <!-- best fit based on label -->
                <!-- marc code: cpe -->
                <!-- marc label: Sea Islands Creole -->
                <!-- lcsh: Sea Islands Creole dialect -->
                <xsl:call-template name="lang650spokenCpe"/>
            </xsl:when>
            <xsl:when test="$langISO = 'srp'">
                <!-- ISO 639-3 label: Serbian -->
                <!-- code match -->
                <!-- marc code: srp -->
                <!-- marc label: Serbian -->
                <!-- lcsh: Serbian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Serbian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'slk'">
                <!-- ISO 639-3 label: Slovak -->
                <!-- ISO 639-2/B synonym -->
                <!-- marc code: slo -->
                <!-- marc label: Slovak -->
                <!-- lcsh: Slovak language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Slovak</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'slv'">
                <!-- ISO 639-3 label: Slovenian -->
                <!-- code match -->
                <!-- marc code: slv -->
                <!-- marc label: Slovenian -->
                <!-- lcsh: Slovenian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Slovenian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'som'">
                <!-- ISO 639-3 label: Somali -->
                <!-- code match -->
                <!-- marc code: som -->
                <!-- marc label: Somali -->
                <!-- lcsh: Somali language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Somali</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ajp'">
                <!-- ISO 639-3 label: South Levantine Arabic -->
                <!-- best fit based on label, marc assigned collective code -->
                <!-- marc code: sem -->
                <!-- marc label: South Arabic -->
                <!-- lcsh: South Arabic language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">South Arabic</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'nan'">
                <!-- ISO 639-3 label: Min Nan Chinese -->
                <!-- best fit based on label -->
                <!-- marc code: chi -->
                <!-- marc label: Chinese -->
                <!-- lcsh: Southern Min dialects -->
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Southern Min dialects</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Chinese</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:when>
            <xsl:when test="$langISO = 'spa'">
                <!-- ISO 639-3 label: Spanish -->
                <!-- code match -->
                <!-- marc code: spa -->
                <!-- marc label: Spanish -->
                <!-- lcsh: Spanish language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Spanish</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'swa'">
                <!-- ISO 639-3 label: Swahili -->
                <!-- code match -->
                <!-- marc code: swa -->
                <!-- marc label: Swahili -->
                <!-- lcsh: Swahili language -->
                <xsl:call-template name="lang650spokenSwa"/>                
            </xsl:when>
            <xsl:when test="$langISO = 'swc'">
                <!-- ISO 639-3 label: Congo Swahili -->
                <!-- best fit based on label -->
                <!-- marc code: swa -->
                <!-- marc label: Swahili -->
                <!-- lcsh: Swahili language -->
                <xsl:call-template name="lang650spokenSwa"/>
            </xsl:when>
            <xsl:when test="$langISO = 'swh'">
                <!-- ISO 639-3 label: Swahili (individual language) -->
                <!-- best fit based on label -->
                <!-- marc code: swa -->
                <!-- marc label: Swahili -->
                <!-- lcsh: Swahili language -->
                <xsl:call-template name="lang650spokenSwa"/>
            </xsl:when>
            <xsl:when test="$langISO = 'swe'">
                <!-- ISO 639-3 label: Swedish -->
                <!-- code match -->
                <!-- marc code: swe -->
                <!-- marc label: Swedish -->
                <!-- lcsh: Swedish language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Swedish</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tgl'">
                <!-- ISO 639-3 label: Tagalog -->
                <!-- code match -->
                <!-- marc code: tgl -->
                <!-- marc label: Tagalog -->
                <!-- lcsh: Tagalog language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Tagalog</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tam'">
                <!-- ISO 639-3 label: Tamil -->
                <!-- code match -->
                <!-- marc code: tam -->
                <!-- marc label: Tamil -->
                <!-- lcsh: Tamil language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Tamil</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tha'">
                <!-- ISO 639-3 label: Thai -->
                <!-- code match -->
                <!-- marc code: tha -->
                <!-- marc label: Thai -->
                <!-- lcsh: Thai language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Thai</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tir'">
                <!-- ISO 639-3 label: Tigrinya -->
                <!-- code match -->
                <!-- marc code: tir -->
                <!-- marc label: Tigrinya -->
                <!-- lcsh: Tigrinya language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Tigrinya</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tpi'">
                <!-- ISO 639-3 label: Tok Pisin -->
                <!-- code match -->
                <!-- marc code: tpi -->
                <!-- marc label: Tok Pisin -->
                <!-- lcsh: Tok Pisin language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Tok Pisin</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'tur'">
                <!-- ISO 639-3 label: Turkish -->
                <!-- code match -->
                <!-- marc code: tur -->
                <!-- marc label: Turkish -->
                <!-- lcsh: Turkish language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Turkish</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'ukr'">
                <!-- ISO 639-3 label: Ukrainian -->
                <!-- code match -->
                <!-- marc code: ukr -->
                <!-- marc label: Ukrainian -->
                <!-- lcsh: Ukrainian language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Ukrainian</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'urd'">
                <!-- ISO 639-3 label: Urdu -->
                <!-- code match -->
                <!-- marc code: urd -->
                <!-- marc label: Urdu -->
                <!-- lcsh: Urdu language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Urdu</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'uzb'">
                <!-- ISO 639-3 label: Uzbek -->
                <!-- code match -->
                <!-- marc code: uzb -->
                <!-- marc label: Uzbek -->
                <!-- lcsh: Uzbek language -->
                <xsl:call-template name="lang650spokenUzb"/>
            </xsl:when>
            <xsl:when test="$langISO = 'uzn'">
                <!-- ISO 639-3 label: Northern Uzbek -->
                <!-- best fit based on label -->
                <!-- marc code: uzb -->
                <!-- marc label: Uzbek -->
                <!-- lcsh: Uzbek language -->
                <xsl:call-template name="lang650spokenUzb"/>
            </xsl:when>
            <xsl:when test="$langISO = 'vie'">
                <!-- ISO 639-3 label: Vietnamese -->
                <!-- code match -->
                <!-- marc code: vie -->
                <!-- marc label: Vietnamese -->
                <!-- lcsh: Vietnamese language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Vietnamese</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'wuu'">
                <!-- ISO 639-3 label: Wu Chinese -->
                <!-- best fit based on label -->
                <!-- marc code: chi -->
                <!-- marc label: Chinese -->
                <!-- lcsh: Wu dialects -->
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Wu dialects</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Chinese</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Data processing</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="v">
                        <xsl:text>Databases.</xsl:text>
                    </marc:subfield>
                </marc:datafield>
            </xsl:when>
            <xsl:when test="$langISO = 'ybb'">
                <!-- ISO 639-3 label: Yemba -->
                <!-- match based on label, marc assigned collective code -->
                <!-- marc code: bai -->
                <!-- marc label: Yemba -->
                <!-- lcsh: Yemba language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Yemba</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'luq'">
                <!-- ISO 639-3 label: Lucumi -->
                <!-- best fit based on label -->
                <!-- marc code: yor -->
                <!-- marc label: Yoruba -->
                <!-- lcsh: Yoruba language -->
                <xsl:call-template name="lang650spokenYor"/>                
            </xsl:when>
            <xsl:when test="$langISO = 'yor'">
                <!-- ISO 639-3 label: Yoruba -->
                <!-- code match -->
                <!-- marc code: yor -->
                <!-- marc label: Yoruba -->
                <!-- lcsh: Yoruba language -->
                <xsl:call-template name="lang650spokenYor"/>
            </xsl:when>
            <xsl:when test="$langISO = 'zul'">
                <!-- ISO 639-3 label: Zulu -->
                <!-- code match -->
                <!-- marc code: zul -->
                <!-- marc label: Zulu -->
                <!-- lcsh: Zulu language -->
                <xsl:call-template name="lang650spokenDefault">
                    <xsl:with-param name="langLCSHroot">Zulu</xsl:with-param>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$langISO = 'zxx'"/>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="lang650spokenDefault">
        <xsl:param name="langLCSHroot"/>
        <marc:datafield tag="650" ind1=" " ind2="0">
            <marc:subfield code="a">
                <xsl:value-of select="$langLCSHroot"/>
                <xsl:text> language</xsl:text>
            </marc:subfield>
            <marc:subfield code="x">
                <xsl:text>Spoken </xsl:text>
                <xsl:value-of select="$langLCSHroot"/>
            </marc:subfield>
            <marc:subfield code="x">
                <xsl:text>Data processing</xsl:text>
            </marc:subfield>
            <marc:subfield code="v">
                <xsl:text>Databases.</xsl:text>
            </marc:subfield>
        </marc:datafield>
    </xsl:template>
    <xsl:template name="lang650spokenAlb">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'als'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'sqi'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Albanian language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Albanian</xsl:text>
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
    <xsl:template name="lang650spokenAra">
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
                        <xsl:text>Spoken Arabic</xsl:text>
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
    <xsl:template name="lang650spokenChi">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'lzh'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'zho'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Chinese language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Chinese</xsl:text>
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
    <xsl:template name="lang650spokenDra">
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
                        <xsl:text>Spoken Dravidian</xsl:text>
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
    <xsl:template name="lang650spokenMan">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'emk'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'mxx'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Mandingo language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Mandingo</xsl:text>
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
    <xsl:template name="lang650spokenNor">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'nob'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'nor'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Norwegian language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Norwegian</xsl:text>
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
    <xsl:template name="lang650spokenPer">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'fas'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'pes'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Persian language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Persian</xsl:text>
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
    <xsl:template name="lang650spokenCpe">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'gul'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'trf'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Sea Islands Creole dialect</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Sea Islands Creole</xsl:text>
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
    <xsl:template name="lang650spokenSwa">
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
                        <xsl:text>Spoken Swahili</xsl:text>
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
    <xsl:template name="lang650spokenUzb">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'uzb'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'uzn'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Uzbek language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Uzbek</xsl:text>
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
    <xsl:template name="lang650spokenYor">
        <xsl:choose>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'luq'"/>
            <xsl:when test="../preceding-sibling::dc:language/@olac:code = 'yor'"/>
            <xsl:otherwise>
                <marc:datafield tag="650" ind1=" " ind2="0">
                    <marc:subfield code="a">
                        <xsl:text>Yoruba language</xsl:text>
                    </marc:subfield>
                    <marc:subfield code="x">
                        <xsl:text>Spoken Yoruba</xsl:text>
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
