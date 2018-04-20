#!/bin/bash
#python Migration.py
var = 0

for folder in 'community' 'collection' 'generic' 'thesis' #'technical' 'relatedObject'
do
	for file in $(ls -p ~/git/remote/metadata/scripts/migration/results/inJupiter/$folder/)
		do
			var=$((var+1))
			echo $var
			echo $folder/$file 
			curl -X POST -H "Content-Type:application/n-triples" -T results/inJupiter/$folder/$file http://206.167.181.124:7200/repositories/migration_complete/statements
			#curl -X POST -H "Content-Type:application/n-triples" -T results/inJupiter/$folder/$file http://206.167.181.124:7200/repositories/migration_mar_29/statements
		done
	for file1 in $(ls -p ~/git/remote/metadata/scripts/migration/results/$folder/)
		do
			var=$((var+1))
			echo $var
			echo $folder/$file1 
			curl -X POST -H "Content-Type:application/n-triples" -T results/$folder/$file1 http://206.167.181.124:7200/repositories/migration_complete/statements
		done
done