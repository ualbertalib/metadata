#!/bin/sh
#
#
for THEURLPATH in `echo "person manifestation degree runtime subject thesisDegree void"`
do

echo "--"
echo "-- Rule list for path ${THEURLPATH}."
echo "--
"
echo "DB.DBA.VHOST_REMOVE (
lhost=>'*ini*',
vhost=>'*ini*',
lpath=>'/${THEURLPATH}'
);"
#exit 0;
echo "DB.DBA.VHOST_DEFINE (
lhost=>'*ini*',
vhost=>'*ini*',
lpath=>'/${THEURLPATH}',
ppath=>'/DAV/',
is_dav=>1,
def_page=>'',
vsp_user=>'dba',
ses_vars=>0,
opts=>vector ('browse_sheet', '', 'url_rewrite', 'http_rule_list_${THEURLPATH}'),
is_default_host=>0
);"

echo "DB.DBA.URLREWRITE_CREATE_RULELIST (
'http_rule_list_${THEURLPATH}', 1,
vector ('http_rule_8_${THEURLPATH}','http_rule_7_${THEURLPATH}','http_rule_6_${THEURLPATH}','http_rule_5_${THEURLPATH}','http_rule_4_${THEURLPATH}','http_rule_3_${THEURLPATH}', 'http_rule_2_${THEURLPATH}', 'http_rule_1_${THEURLPATH}'));"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_1_${THEURLPATH}', 1,
'^/${THEURLPATH}/(.*)\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2F${THEURLPATH}%%2F%U%%3E&format=%U',
vector ('par_1', '*accept*'),
NULL,
'(text/rdf.n3)|(application/rdf.xml)|(text/turtle)|(text/rdf.ttl)|(application/turtle)|(text/csv)|(application/json)|(application/ld.json)',
2,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_2_${THEURLPATH}', 1,
'^/${THEURLPATH}/(.*)\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/describe/?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2F${THEURLPATH}%%2F%s',
vector ('par_1'),
NULL,
'(text/html)|(\\\\\\*/\\\\\\*)',
0,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_3_${THEURLPATH}', 1,
'^/${THEURLPATH}/(.*)\\\\.rdf\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2F${THEURLPATH}%%2F%U%%3E&format=application/rdf%%2Bxml',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_4_${THEURLPATH}', 1,
'^/${THEURLPATH}/(.*)\\\\.ttl\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2F${THEURLPATH}%%2F%U%%3E&format=text/turtle',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_5_${THEURLPATH}', 1,
'^/${THEURLPATH}/(.*)\\\\.nt\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2F${THEURLPATH}%%2F%U%%3E&format=text/plain',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_6_${THEURLPATH}', 1,
'^/${THEURLPATH}/(.*)\\\\.jsonld\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2F${THEURLPATH}%%2F%U%%3E&format=application/ld%%2Bjson',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_7_${THEURLPATH}', 1,
'^/${THEURLPATH}/(.*)\\\\.json\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2F${THEURLPATH}%%2F%U%%3E&format=application/ld%%2Bjson',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_8_${THEURLPATH}', 1,
'^/${THEURLPATH}/(.*)\\\\.html\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/describe/?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2F${THEURLPATH}%%2F%s',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

done

#
# Additional rules are needed for /thesis exports to bibtex and ris
#

echo "--"
echo "-- Rule list for path thesis."
echo "--
"
echo "DB.DBA.VHOST_REMOVE (
lhost=>'*ini*',
vhost=>'*ini*',
lpath=>'/thesis'
);"
#exit 0;
echo "DB.DBA.VHOST_DEFINE (
lhost=>'*ini*',
vhost=>'*ini*',
lpath=>'/thesis',
ppath=>'/DAV/',
is_dav=>1,
def_page=>'',
vsp_user=>'dba',
ses_vars=>0,
opts=>vector ('browse_sheet', '', 'url_rewrite', 'http_rule_list_thesis'),
is_default_host=>0
);"

echo "DB.DBA.URLREWRITE_CREATE_RULELIST (
'http_rule_list_thesis', 1,
vector ('http_rule_13_thesis','http_rule_12_thesis','http_rule_11_thesis','http_rule_10_thesis','http_rule_9_thesis','http_rule_8_thesis','http_rule_7_thesis','http_rule_6_thesis','http_rule_5_thesis','http_rule_4_thesis','http_rule_3_thesis', 'http_rule_2_thesis', 'http_rule_1_thesis'));"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_1_thesis', 1,
'^/thesis/(.*)\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%U%%3E&format=%U',
vector ('par_1', '*accept*'),
NULL,
'(text/rdf.n3)|(application/rdf.xml)|(text/turtle)|(text/rdf.ttl)|(application/turtle)|(text/csv)|(application/json)|(application/ld.json)',
2,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_2_thesis', 1,
'^/thesis/(.*)\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/describe/?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%s',
vector ('par_1'),
NULL,
'(text/html)|(\\\\\\*/\\\\\\*)',
0,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_3_thesis', 1,
'^/thesis/(.*)\\\\.rdf\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%U%%3E&format=application/rdf%%2Bxml',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_4_thesis', 1,
'^/thesis/(.*)\\\\.ttl\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%U%%3E&format=text/turtle',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_5_thesis', 1,
'^/thesis/(.*)\\\\.nt\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%U%%3E&format=text/plain',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_6_thesis', 1,
'^/thesis/(.*)\\\\.jsonld\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%U%%3E&format=application/ld%%2Bjson',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_7_thesis', 1,
'^/thesis/(.*)\\\\.json\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/sparql?query=DESCRIBE%%20%%3Chttp%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%U%%3E&format=application/ld%%2Bjson',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_8_thesis', 1,
'^/thesis/(.*)\\\\.html\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/describe/?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%s',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_9_thesis', 1,
'^/thesis/(.*)\\\\.bibtex\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/exportBibtex?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%s',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_10_thesis', 1,
'^/thesis/(.*)\\\\.bib\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/exportBibtex?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%s',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_11_thesis', 1,
'^/thesis/(.*)\\\\.ris\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/exportRIS?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%s',
vector ('par_1'),
NULL,
NULL,
1,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_12_thesis', 1,
'^/thesis/(.*)\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/exportBibtex?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%s',
vector ('par_1', '*accept*'),
NULL,
'(application/x-bibtex)',
2,
303,
''
);"

echo "DB.DBA.URLREWRITE_CREATE_REGEX_RULE (
'http_rule_13_thesis', 1,
'^/thesis/(.*)\\\$',
vector ('par_1'),
1,
'http://canlink.library.ualberta.ca/exportRIS?url=http%%3A%%2F%%2Fcanlink.library.ualberta.ca%%2Fthesis%%2F%s',
vector ('par_1', '*accept*'),
NULL,
'(application/x-research-info-systems)',
2,
303,
''
);"
