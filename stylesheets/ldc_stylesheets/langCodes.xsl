<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:olac="http://www.language-archives.org/OLAC/1.1/"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:template name="langCodesMarc">
        <xsl:param name="lang"/>
        <xsl:choose>
            <!-- best fit based on label -->
            <xsl:when test="$lang='abv'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='acm'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='afb'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- best fit based on label, marc assigned collective code -->
            <xsl:when test="$lang='ajp'">
                <xsl:text>sem</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='als'">
                <xsl:text>alb</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='amh'">
                <xsl:text>amh</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='apc'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='ara'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='arb'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='ary'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='arz'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='asm'">
                <xsl:text>asm</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='ayp'">
                <xsl:text>ara</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='bam'">
                <xsl:text>bam</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='ben'">
                <xsl:text>ben</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='bos'">
                <xsl:text>bos</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='bul'">
                <xsl:text>bul</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='cat'">
                <xsl:text>cat</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='ces'">
                <xsl:text>cze</xsl:text>
            </xsl:when>
            <!-- marc preferred term ('use'), based on label match -->
            <xsl:when test="$lang='cmn'">
                <xsl:text>chi</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='dan'">
                <xsl:text>dan</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='deu'">
                <xsl:text>ger</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='ell'">
                <xsl:text>gre</xsl:text>
            </xsl:when>
            <!-- marc preferred term ('use'), based on label match -->
            <xsl:when test="$lang='emk'">
                <xsl:text>man</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='eng'">
                <xsl:text>eng</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='est'">
                <xsl:text>est</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='eus'">
                <xsl:text>baq</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='fas'">
                <xsl:text>per</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='fra'">
                <xsl:text>fre</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='gla'">
                <xsl:text>gla</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='gul'">
                <xsl:text>cpe</xsl:text>
            </xsl:when>
            <!-- code match, though labels differ -->
            <xsl:when test="$lang='hat'">
                <xsl:text>hat</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='hau'">
                <xsl:text>hau</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='hin'">
                <xsl:text>hin</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='hrv'">
                <xsl:text>hrv</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='hun'">
                <xsl:text>hun</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='ind'">
                <xsl:text>ind</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='ita'">
                <xsl:text>ita</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='jgo'">
                <xsl:text>bai</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='jpn'">
                <xsl:text>jpn</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='kat'">
                <xsl:text>geo</xsl:text>
            </xsl:when>
            <!-- code match, though labels differ -->
            <xsl:when test="$lang='khm'">
                <xsl:text>khm</xsl:text>
            </xsl:when>
            <!-- marc assigned collective code for Malto (best fit based on label) -->
            <xsl:when test="$lang='kmj'">
                <xsl:text>dra</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='kmr'">
                <xsl:text>kur</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='kor'">
                <xsl:text>kor</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='kxm'">
                <xsl:text>khm</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='lao'">
                <xsl:text>lao</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='lat'">
                <xsl:text>lat</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='lit'">
                <xsl:text>lit</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='luq'">
                <xsl:text>yor</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='lzh'">
                <xsl:text>chi</xsl:text>
            </xsl:when>
            <!-- marc assigned collective code for Malto (best fit based on label) -->
            <xsl:when test="$lang='mjt'">
                <xsl:text>dra</xsl:text>
            </xsl:when>
            <!-- marc assigned collective code for Malto (best fit based on label) -->
            <xsl:when test="$lang='mkb'">
                <xsl:text>dra</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='mxx'">
                <xsl:text>man</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='nan'">
                <xsl:text>chi</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='nld'">
                <xsl:text>dut</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='nno'">
                <xsl:text>nno</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='nob'">
                <xsl:text>nob</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='nor'">
                <xsl:text>nor</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='pan'">
                <xsl:text>pan</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='pes'">
                <xsl:text>per</xsl:text>
            </xsl:when>
            <!-- marc preferred term ('use'), based on label match -->
            <xsl:when test="$lang='pnb'">
                <xsl:text>lah</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='pol'">
                <xsl:text>pol</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='por'">
                <xsl:text>por</xsl:text>
            </xsl:when>
            <!-- match based on label, marc assigned collective code -->
            <xsl:when test="$lang='prs'">
                <xsl:text>per</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='pus'">
                <xsl:text>pus</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='ron'">
                <xsl:text>rum</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='rus'">
                <xsl:text>rus</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='san'">
                <xsl:text>san</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='slv'">
                <xsl:text>slv</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='som'">
                <xsl:text>som</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='spa'">
                <xsl:text>spa</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='sqi'">
                <xsl:text>alb</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='srp'">
                <xsl:text>srp</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='swa'">
                <xsl:text>swa</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='swc'">
                <xsl:text>swa</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='swe'">
                <xsl:text>swe</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='swh'">
                <xsl:text>swa</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='tam'">
                <xsl:text>tam</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='tgl'">
                <xsl:text>tgl</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='tha'">
                <xsl:text>tha</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='tir'">
                <xsl:text>tir</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='tpi'">
                <xsl:text>tpi</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='trf'">
                <xsl:text>cpe</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='tur'">
                <xsl:text>tur</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='ukr'">
                <xsl:text>ukr</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='urd'">
                <xsl:text>urd</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='uzb'">
                <xsl:text>uzb</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='uzn'">
                <xsl:text>uzb</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='vie'">
                <xsl:text>vie</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='wuu'">
                <xsl:text>chi</xsl:text>
            </xsl:when>
            <!-- match based on label, marc assigned collective code -->
            <xsl:when test="$lang='ybb'">
                <xsl:text>bai</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='yor'">
                <xsl:text>yor</xsl:text>
            </xsl:when>
            <!-- marc preferred term ('use'), based on label match -->
            <xsl:when test="$lang='yue'">
                <xsl:text>chi</xsl:text>
            </xsl:when>
            <!-- ISO 239-2/B synonym -->
            <xsl:when test="$lang='zho'">
                <xsl:text>chi</xsl:text>
            </xsl:when>
            <!-- best fit based on label -->
            <xsl:when test="$lang='zsm'">
                <xsl:text>may</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='zul'">
                <xsl:text>zul</xsl:text>
            </xsl:when>
            <!-- code match -->
            <xsl:when test="$lang='zxx'">
                <xsl:text>zxx</xsl:text>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>