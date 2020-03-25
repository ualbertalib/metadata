#!/bin/bash
#
#
source /home/ubuntu/passWords.sh
OUTFILE=`date --iso-8601`
echo "Dump started at `date`" > /var/www/html/downloads/footer.html
echo "dump_one_graph ('http://canlink.library.ualberta.ca/canlink', '/home/ubuntu/dataset/canlink-${OUTFILE}-',1000000000000);" | isql -U dba -P "${VIRTUOSO_PASSWORD}"
rm -f /home/ubuntu/dataset/canlink-${OUTFILE}-*.graph
mv -f /home/ubuntu/dataset/canlink-${OUTFILE}-*.gz /var/www/html/downloads/.
ln -s -f /var/www/html/downloads/canlink-${OUTFILE}-*.gz /var/www/html/downloads/canlink-current.gz
# Keep files for 7 days, unless they are from the first of the month, in which case we keep them as a long term backup.
find /var/www/html/downloads/. -type f -mtime +7  -not -name "canlink-*-*-01-000001.ttl.gz" -not -name ".htaccess" -not -name "new_csh.nt.gz" -not -name "*.html" -exec rm -rf {} \;
echo "Dump complete at `date`" > /var/www/html/downloads/footer.html
