#!/bin/bash
python Migration.py
var = 0
#'community' 'collection'
for folder in 'generic' #'thesis' #'technical' 'relatedObject'
do
	for file in $(ls -p ~/git/remote/metadata/scripts/migration/results/$folder/)
		do
			var=$((var+1))
			echo $var
			echo $folder/$file 
			curl -X POST -H "Content-Type:application/n-triples" -T results/$folder/$file http://206.167.181.124:7200/repositories/mar_8_generic/statements
		done
done