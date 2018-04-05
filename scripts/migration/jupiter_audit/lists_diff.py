package = set(open('migration_20120222-noidsfrompackage.txt').read().split())
migrated = set(open('jupiternoids.txt').read().split())

rejected = package.difference(migrated)
notinpackage = migrated.difference(package)

print(rejected)
print(notinpackage)


f_rejected = open('results_rejected.txt','w') 
f_rejected.write(repr(rejected))
f_rejected.close

f_notinpackage = open('results_notinpackage.txt','w') 
f_notinpackage.write(repr(notinpackage))
f_notinpackage.close