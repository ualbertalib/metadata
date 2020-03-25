#!/bin/sh
#
OUTFILE=`date --iso-8601`
#
# Roundabout way prevents query injections
cut -d "\"" -f 2 < /var/log/apache2/access.log | grep 'GET /typeahead.php?term' | cut -d " " -f 2 > ~/queryCache/typeahead-${OUTFILE}.log
cut -d "\"" -f 2 < /var/log/apache2/access.log | grep 'GET /sparql?query' | cut -d " " -f 2 > ~/queryCache/query-${OUTFILE}.log
find ~/queryCache/. -type f -mtime +8



 
