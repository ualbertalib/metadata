#!/bin/bash
var = 0
#'community' 'collection'
for folder in 'generic' 'technical' 'relatedObject' #'thesis'
do
	for file in $(ls -p ~/metadata/scripts/migration/results/$folder/)
		do
			var=$((var+1))
			echo $var
			echo $folder/$file 
			curl -X POST -H "Content-Type:application/n-triples" -T $folder/$file http://localhost:7200/repositories/ERA/statements
		done
done
