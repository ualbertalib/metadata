#!/bin/bash
#python Migration.py

curl -X POST -H "Content-Type:application/n-triples" -T results/inJupiter/$folder/$file http://206.167.181.124:7200/repositories/migration_complete/statements
#curl -X POST -H "Content-Type:application/n-triples" -T results/inJupiter/$folder/$file http://206.167.181.124:7200/repositories/migration_mar_29/statements