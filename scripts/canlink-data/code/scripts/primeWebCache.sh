#!/bin/sh
#
#
#
MAX_QUERIES=10
# Pick out sparql queries from the web log and pull out the top-n occuring MAX_QUERIES for priming the cache when data is added to the dataset.
#
#
#

(
  # Wait for lock on /var/lock/.myscript.exclusivelock (fd 200) for 10 seconds
  flock -x -w 10 200 || exit 1

  # Do stuff

) 200>/var/lock/.myscript.exclusivelock

grep "GET /sparql?query=" /var/log/apache2/access.log | cut -d "?" -f 2- | cut -d " " -f 1 | sort | uniq -c | sort -k 1 -n -r | head - -n ${MAX_QUERIES} | cut -d " " -f 2- > /tmp/queries.$$
IFS=\n
for QUERY in `cat /tmp/queries.$$`
do
 curl "http://localhost/parql?${QUERY}" > /dev/null
done

# util-linux