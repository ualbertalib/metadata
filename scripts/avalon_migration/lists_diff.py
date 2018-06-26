package = set(open('solr_id.txt').read().split())
migrated = set(open('xpath_id_originals.txt').read().split())

rejected = package.difference(migrated)
notinpackage = migrated.difference(package)

print(rejected)
print(notinpackage)


f_rejected = open('results_1.txt','w') 
f_rejected.write(repr(rejected))
f_rejected.close

f_notinpackage = open('results_2.txt','w') 
f_notinpackage.write(repr(notinpackage))
f_notinpackage.close