#!/bin/bash
var = 0
#'community' 'collection'
for folder in 'generic' #'technical' 'relatedObject' #'thesis'
do
	for file in $(ls -p ~/main-metadata.git/scripts/migration/results/$folder/)
		do
			var=$((var+1))
			echo $var
			echo $folder/$file 
			curl -X POST -H "Content-Type:application/n-triples" -T results/$folder/$file http://206.167.181.124:7200/repositories/generic-feb-16/statements
		done
done