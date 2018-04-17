#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "Text read from file: $line"

	curl "http://tottenham.library.ualberta.ca:8080/solr/hydranorth_shard1_replica3/select?q=accessTo_ssim%3A$line&&fl=id&wt=csv&indent=true" >> "cperms.txt"
done < "clist.txt"