#!/bin/bash
#
#
echo "Trying to load [$1] in [$0]." >> /tmp/crap
#source /home/danydvd/passWords.sh
#mv -f $1 /home/www-data/ingest/.
MYFILE=`echo $1 | rev | cut -d "/" -f 1 | rev`
curl -X POST -H "Content-Type:application/xml" -u "admin:4Metadata!" -T $1 http://206.167.181.124:7200/repositories/cldi-test-9/statements
#echo "ld_dir('/home/www-data/ingest', '${MYFILE}','http://206.167.181.124:7200/repositories/cldi-test/statements');" | isql -U dba -P "${VIRTUOSO_PASSWORD}"
#echo "rdf_loader_run();"  | isql -U dba -P "${VIRTUOSO_PASSWORD}"
