**LDC METADATA TRANSFORMATION STEPS**

[format used below:]\
#. **Transformation step**\
input_file\
(stylesheet or tool)\
=> output_file

1\. **Extract LDC OLAC records from OLAC source**\
olac_source_olacdc.xml\
(extract_ldc_olac_from_source_v2.xsl)\
=> olac_ldc_extract_olacdc.xml

2\. **Convert LDC OLAC records to MARCXML**\
olac_ldc_extract_olacdc.xml\
[or alternate file name]\
(convert_ldc_olac_to_marcxml.xsl)\
(lang_041.xsl)\
(lang_650_basic.xsl)\
(lang_650_spoken.xsl)\
=> olac_ldc_extract_marcxml.xml

3\. **[onetime] Add 650s from UAL LDC MARC records**\
olac_ldc_extract_marcxml.xml\
ual_ldc_marc_650s_corrected_marcxml.xml\
(combine_ldc_marcxml_with_650.xsl)\
=> combined_olac_ual_ldc_marcxml.xml

4\. **Derive HTML formatted MARC**\
olac_ldc_extract_marcxml.xml\
(MARC21slim2English_revised.xsl)\
=> combined_olac_ual_ldc_marc_html.html

5\. **Derive MARC format records**\
combined_olac_ual_ldc_marcxml.xml\
(MarcEdit tool)\
=> combined_olac_ual_ldc_marc.mrc


**SOURCES FOR LDC METADATA**

1\. **OLAC OAI Calls**

1.1 Retrieve all LDC records with a given issue date (e.g., 2018-09-17):\
(New corpora are released once a month, usually around the 15th)

http://www.language-archives.org/cgi-bin/olaca3.pl?verb=Query&elements=2&sql=e1.TagName%3D'Publisher'+and+e1.Content%3D'Linguistic+Data+Consortium'+and+e2.TagName%3D'issued'+and+e2.Content%3D'2018-09-17'

1.2 Retrieve all LDC records:

http://www.language-archives.org/cgi-bin/olaca3.pl?verb=Query&elements=2&sql=e1.TagName%3D'Publisher'+and+e1.Content%3D'Linguistic+Data+Consortium'

2\. **Nightly dump of all OLAC records**

http://www.language-archives.org/tools.html
